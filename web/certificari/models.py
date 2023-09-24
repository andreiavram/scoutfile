import datetime

from django.db import models
from django.db.models import TextChoices, Q


class CertificationType(models.Model):
    class SourceOptions(TextChoices):
        INTERNAL = "internal", "Internă"
        EXTERNAL = "external", "Externă"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    icon = models.ImageField(upload_to="certificari/icons/", null=True, blank=True)
    source = models.CharField(max_length=100, choices=SourceOptions.choices, default=SourceOptions.INTERNAL)

    validity = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.title


class ValidCertificateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(valid_until__isnull=True) | Q(valid_until__gte=datetime.date.today()))


class Certificate(models.Model):
    issued_to = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE, related_name="certificari", verbose_name="Titluar")
    issued_on = models.DateField()
    valid_until = models.DateField(null=True, blank=True)

    issued_by = models.CharField(max_length=1024, blank=True, verbose_name="Emitent")
    certificate_type = models.ForeignKey(CertificationType, on_delete=models.CASCADE, verbose_name="Tip certificat")

    event_received = models.ForeignKey("album.Eveniment", null=True, blank=True, on_delete=models.SET_NULL, related_name="issued_certificates")
    events = models.ManyToManyField("album.Eveniment", blank=True, related_name="contributed_certificates")
    document = models.ForeignKey("documente.Document", null=True, blank=True, on_delete=models.SET_NULL)

    objects = ValidCertificateManager()
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.id is None and self.certificate_type.validity and self.valid_until is None:
            self.valid_until = self.issued_on + self.certificate_type.validity
        return super().save(*args, **kwargs)

    @property
    def is_valid(self):
        return self.valid_until is None or self.valid_until > datetime.date.today()


