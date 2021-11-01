#coding: utf-8
from builtins import object
from django.db import models

# Create your models here.


TIPURI_BADGE = (("eveniment", u"Eveniment"), ("progres", u"Progres"), ("merit", u"Merit"), ("altul", u"Alt tip de badge"))
STATUS_BADGE = (("produs", u"Produs"), ("propus", u"Propus"))


class Badge(models.Model):
    class Meta(object):
        ordering = ["-data_productie"]

    nume = models.CharField(max_length=255)
    descriere = models.CharField(max_length=2048, null=True, blank=True)
    tip = models.CharField(max_length=255, choices=TIPURI_BADGE)

    tiraj = models.IntegerField()
    tiraj_exact = models.BooleanField(default=False, help_text=u"Tirajul este cunoscut exact")

    producator = models.CharField(max_length=255, null=True, blank=True, help_text=u"Unde a fost produs badge-ul?")
    designer = models.CharField(max_length=255, null=True, blank=True)
    designer_membru = models.ForeignKey("structuri.Membru", on_delete=models.SET_NULL, null=True, blank=True)

    data_productie = models.DateField()
    status = models.CharField(max_length=255, default="produs")

    disponibil_in = models.TextField(null=True, blank=True, verbose_name=u"Unde se poate găsi", help_text=u"Unde poate fi găsit badge-ul, câte o locație pe linie")

    poza_badge = models.ForeignKey("album.Imagine", null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ForeignKey("structuri.Membru", related_name="badgeuri", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def resursa_vectoriala(self):
        return

    def resursa_bitmap(self):
        return
