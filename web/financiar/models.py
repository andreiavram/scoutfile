import csv
import urllib
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models, IntegrityError
from django.db.models import TextChoices, IntegerChoices
from localflavor.generic.models import IBANField

import logging
log = logging.getLogger()


class Currency(TextChoices):
    RON = "ron", "RON"
    EUR = "eur", "EUR"
    USD = "usd", "USD"


class PaymentDocumentType(TextChoices):
    FACTURA = "factura", "Factura"
    CHITANTA = "chitanta", "Chitanta"
    BON_FISCAL = "bon_fiscal", "Bon Fiscal"
    BILET = "bilet", "Bilet"
    DECONT = "decont", "Decont"
    DISPOZITIE_PLATA = "dispozitie_plata", "Dispoziție de plată"
    DISPOZITIE_INCASARE = "dispoziție_incasare", "Dispoziție de încasare"
    OP = "op", "Ordin de plată"
    OTHER = "other", "Altele"


class LegalEntity(models.Model):
    tax_id = models.CharField(max_length=13, verbose_name="CIF sau CNP")
    address = models.CharField(max_length=255)
    account = IBANField(null=True, blank=True)

    contact_person_name = models.CharField(max_length=255, null=True, blank=True)
    contact_person_number = models.CharField(max_length=255, null=True, blank=True)
    contact_person_email = models.EmailField(null=True, blank=True)


class PaymentDocument(models.Model):
    class RegistrationType(TextChoices):
        PAYMENT_REQUEST = "request", "Obligație de plată"
        PAYMENT = "payment", "Dovadă de plată"

    class RegistrationDirection(IntegerChoices):
        ISSUER = 1, "Noi emitem documentul"
        RECEIVER = 2, "Noi primim documentul"

    document_type = models.CharField(max_length=255, choices=PaymentDocumentType.choices)
    registration_status = models.CharField(max_length=255, choices=RegistrationType.choices, default=RegistrationType.PAYMENT)

    value = models.FloatField()
    currency = models.CharField(choices=Currency.choices, default=Currency.RON, max_length=3)

    document_number = models.CharField(max_length=255)
    document_date = models.DateField()
    internal_reference = models.CharField(max_length=255, null=True, blank=True)

    registered_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    registered_at = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey("proiecte.Project", null=True, blank=True, on_delete=models.SET_NULL)
    project_budget_line = models.ForeignKey("proiecte.ProjectBudgetLine", null=True, blank=True, on_delete=models.SET_NULL)
    project_budget_item = models.ForeignKey("proiecte.ProjectBudgetEntry", null=True, blank=True, on_delete=models.SET_NULL)

    third_party = models.ForeignKey(LegalEntity, null=True, blank=True, on_delete=models.SET_NULL)
    third_party_text = models.CharField(max_length=255, null=True, blank=True)
    direction = models.PositiveSmallIntegerField(choices=RegistrationDirection.choices, default=RegistrationDirection.RECEIVER)

    notes = models.TextField()

    def __str__(self):
        direction = {
            PaymentDocument.RegistrationDirection.RECEIVER: "de la",
            PaymentDocument.RegistrationDirection.ISSUER: "pentru"
        }

        return (
            f"{self.get_document_type_display()} {self.document_number} / {self.document_date.strptime('%d.%m.%Y')} " 
            f"{direction.get(self.direction, '?')} {self.third_party if self.third_party else self.third_party_text}"
            f"în valoare de {self.value} {self.currency}"
        )


class PaymentDocumentFile(models.Model):
    payment_document = models.ForeignKey(PaymentDocument, on_delete=models.CASCADE)
    uploaded_file = models.FileField(upload_to="financiar/document")


class BankAccount(models.Model):
    class BankOptions(TextChoices):
        BT = "bt", "Banca Transilvania"

    centru_local = models.ForeignKey("structuri.CentruLocal", on_delete=models.CASCADE)
    iban = IBANField()
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.RON)
    bank = models.CharField(max_length=5, choices=BankOptions.choices)
    name = models.CharField(max_length=255, blank=True)

    valid_from = models.DateField()
    valid_through = models.DateField(null=True, blank=True)

    added_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        description = f"{self.iban}"
        if self.name:
            description += f"- {self.name}"
        return description


class BankStatement(models.Model):
    class StatementProcessingStatus(IntegerChoices):
        UPLOADED = 1, "Uploaded"
        QUEUED = 2, "Queued"
        PROCESSING = 3, "Processing"
        ERROR = 4, "Error in processing"
        PROCESSED = 5, "Processed"

    import_date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    internal_ref = models.CharField(max_length=255, null=True, blank=True)
    statement_file = models.FileField(upload_to="financiar/statements/")

    processing_status = models.PositiveSmallIntegerField(choices=StatementProcessingStatus.choices, default=StatementProcessingStatus.UPLOADED)
    last_processed_at = models.DateTimeField(null=True, blank=True)

    def update_processing_status(self, status, commit=True):
        self.processing_status = status
        self.last_processed_at = datetime.now()
        if commit:
            self.save()

    def process_bt_bank_statement(self):
        self.update_processing_status(BankStatement.StatementProcessingStatus.PROCESSING)

        response = urllib.request.urlopen(self.statement_file.url)
        lines = [l.decode('utf-8') for l in response.readlines()]
        csv_reader = csv.reader(lines)

        transaction_line_found = False
        header_line_found = False
        for row in csv_reader:
            if not transaction_line_found:
                if row[0].startswith("Cont"):
                    account_number, currency = row[1].strip().split(" ")
                    if self.account.iban != account_number.upper() or self.account.currency != currency.upper():
                        self.update_processing_status(BankStatement.StatementProcessingStatus.ERROR)
                        log.error(f"Wrong account in file, found {account_number.upper()} {currency.upper()}")
                        break
                elif row[0].startswith("Perioada"):
                    start_date, end_date = row[1].strip().split("-")
                    self.start_date = datetime.strptime(start_date, "%d.%m.%Y")
                    self.end_date = datetime.strptime(end_date, "%d.%m.%Y")
                    continue
                elif row[0].startswith("Rezultat cautare"):
                    transaction_line_found = True
                    continue
            elif header_line_found:
                continue

            try:
                BankStatementItem.objects.create(
                    statement=self,
                    account_number=self.account.iban,
                    transaction_date=datetime.strptime(row[0], "%Y-%m-%d"),
                    currency_date=datetime.strptime(row[1], "%Y-%m-%d"),
                    description=row[2],
                    reference=row[3],
                    value=float(row[4]) if row[4] else float(row[5]),
                    balance=row[6]
                )
            except IntegrityError as e:
                log.error(f"Reference {row[3]} duplicated and will not be re-imported")
                print(f"Reference {row[3]} duplicated and will not be re-imported")

        # this also takes care of saving changes to the model up to this point, like start / end dates
        self.update_processing_status(status=BankStatement.StatementProcessingStatus.PROCESSED)


class BankStatementItem(models.Model):
    statement = models.ForeignKey(BankStatement, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()
    currency_date = models.DateTimeField()
    description = models.CharField(max_length=1024)
    reference = models.CharField(max_length=255)
    value = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)

    # here just to enforce uniqueness
    account_number = IBANField()

    class Meta:
        unique_together = ["account_number", "reference"]
