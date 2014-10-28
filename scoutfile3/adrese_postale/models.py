from django.db import models


class CodPostal(models.Model):
    cod_postal = models.CharField(max_length=6)
    judet = models.CharField(max_length=255)
    localitate = models.CharField(max_length=255)
    tip_strada = models.CharField(max_length=255, null=True, blank=True)
    strada = models.CharField(max_length=255, null=True, blank=True)
    sector = models.IntegerField(null=True, blank=True)
    descriptor = models.CharField(max_length=255, null=True, blank=True)
