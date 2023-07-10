from django.contrib import admin

from financiar.models import BankAccount, BankStatement, BankStatementItem, PaymentDomain, PaymentDocument


@admin.register(PaymentDocument)
class PaymentDocumentAdmin(admin.ModelAdmin):
    list_display = ["direction", "domain", "document_type", "registration_status", "value", "currency", "registered_by", "registered_at", ]


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ["iban", "currency", "centru_local", "bank", "name", "valid_from", "valid_through", "added_by"]


@admin.register(BankStatement)
class BankStatementAdmin(admin.ModelAdmin):
    actions = ["process_statement"]
    list_display = [
        "account", "import_date", "start_date", "end_date", "internal_ref",
        "item_count", "processing_status", "last_processed_at"
    ]
    list_filter = [
        "account__centru_local",
    ]

    @admin.action(description="Process Bank Statement File")
    def process_statement(self, request, queryset):
        for statement in queryset:
            statement.process_bt_bank_statement()

    @admin.display(description="Items")
    def item_count(self, obj):
        return obj.items.all().count()

@admin.register(BankStatementItem)
class BankStatementItemAdmin(admin.ModelAdmin):
    list_display = [
        "reference", "bank_account", "get_transaction_date", "get_currency_date", "description",
        "order", "value", "balance", "registered", "created_date"
    ]

    list_filter = [
        "statement__account"
    ]

    @admin.display(description="Account", ordering="statement__account")
    def bank_account(self, obj):
        return obj.statement.account

    @admin.display(description="Transaction Date", ordering="transaction_date")
    def get_transaction_date(self, obj):
        return obj.transaction_date.date()

    @admin.display(description="Currency Date", ordering="currency_date")
    def get_currency_date(self, obj):
        return obj.currency_date.date()


@admin.register(PaymentDomain)
class PaymentDomainAdmin(admin.ModelAdmin):
    fields = ["name"]
