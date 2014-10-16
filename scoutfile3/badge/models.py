#coding: utf-8
from django.db import models

# Create your models here.


TIPURI_BADGE = (("eveniment", u"Eveniment"), ("progres", u"Progres"), ("merit", u"Merit"), ("altul", u"Alt tip de badge"))
STATUS_BADGE = (("produs", u"Produs"), ("propus", u"Propus"))


class Badge(models.Model):
    nume = models.CharField(max_length=255)
    descriere = models.CharField(max_length=2048, null=True, blank=True)
    tip = models.CharField(max_length=255, choices=TIPURI_BADGE)

    tiraj = models.IntegerField()
    tiraj_exact = models.BooleanField(default=False, help_text=u"Tirajul este cunoscut exact")

    producator = models.CharField(max_length=255, null=True, blank=True, help_text=u"Unde a fost produs badge-ul?")
    designer = models.CharField(max_length=255, null=True, blank=True)
    designer_membru = models.ForeignKey("structuri.Membru", null=True, blank=True)

    data_productie = models.DateField()
    status = models.CharField(max_length=255, default="produs")

    poza_badge = models.ForeignKey("album.Imagine", null=True, blank=True)
    owner = models.ForeignKey("structuri.Membru", related_name="badgeuri")
    timestamp = models.DateTimeField(auto_now=True)

    def resursa_vectoriala(self):
        return

    def resursa_bitmap(self):
        return