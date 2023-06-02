from django.contrib import admin

from financiar.models import BankAccount, BankStatement, BankStatementItem


# Register your models here.


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ["iban", "currency", "centru_local", "bank", "name", "valid_from", "valid_through", "added_by"]


@admin.register(BankStatement)
class BankStatementAdmin(admin.ModelAdmin):
    actions = ["process_statement"]
    list_display = [
        "account", "import_date", "start_date", "end_date", "internal_ref",
        "processing_status", "last_processed_at"
    ]

    @admin.action(description="Process Bank Statement File")
    def process_statement(self, request, queryset):
        for statement in queryset:
            statement.process_bt_bank_statement()


@admin.register(BankStatementItem)
class BankStatementItemAdmin(admin.ModelAdmin):
    list_display = [
        "reference", "statement", "transaction_date", "currency_date", "description", "reference",
        "value", "balance", "created_date"
    ]
