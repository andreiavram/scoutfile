from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import TextChoices, IntegerChoices
from localflavor.generic.models import IBANField


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
    month = models.DateField()
    internal_ref = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to="financiar/statements/")

    currency = models.CharField(choices=Currency.choices, default=Currency.RON, max_length=255)

    processing_status = models.PositiveSmallIntegerField(choices=StatementProcessingStatus.choices, default=StatementProcessingStatus.UPLOADED)
    last_processed_at = models.DateTimeField(null=True, blank=True)


class BankStatementItem(models.Model):
    statement = models.ForeignKey(BankStatement, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()
    currency_date = models.DateTimeField()
    description = models.CharField(max_length=1024)
    reference = models.CharField(max_length=255)
    value = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0)
