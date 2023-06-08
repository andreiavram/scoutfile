from django.contrib import admin

from certificari.models import CertificationType, Certificate


@admin.register(CertificationType)
class CertificationTypeAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "source"]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ["issued_to", "issued_on", "issued_by", "certificate_type", "event_received", "document"]
    list_filter = ["certificate_type", "event_received", "issued_to"]
    autocomplete_fields = ["event_received", "issued_to", "events"]
