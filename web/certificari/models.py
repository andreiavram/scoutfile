from django.db import models
from django.db.models import TextChoices


class CertificationType(models.Model):
    class SourceOptions(TextChoices):
        INTERNAL = "internal", "Internă"
        EXTERNAL = "external", "Externă"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    icon = models.ImageField(upload_to="certificari/icons/", null=True, blank=True)
    source = models.CharField(max_length=100, choices=SourceOptions.choices, default=SourceOptions.INTERNAL)


class Certificate(models.Model):
    issued_to = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE, related_name="certificari")
    issued_on = models.DateField()

    issued_by = models.CharField(max_length=1024, blank=True)
    certificate_type = models.ForeignKey(CertificationType, on_delete=models.CASCADE)

    event_received = models.ForeignKey("album.Eveniment", null=True, blank=True, on_delete=models.SET_NULL, related_name="issued_certificates")
    events = models.ManyToManyField("album.Eveniment", blank=True, related_name="contributed_certificates")
    document = models.ForeignKey("documente.Document", null=True, blank=True, on_delete=models.SET_NULL)
