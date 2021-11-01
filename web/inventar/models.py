# coding: utf-8
from django.db import models

from album.models import Eveniment
from documente.models import Document


class LocatieInventar(models.Model):
    # TODO: imagine pentru locul de inventar?

    centru_local = models.ForeignKey("structuri.CentruLocal", on_delete=models.CASCADE)
    responsabil = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)


class CategorieInventar(models.Model):
    nume = models.CharField(max_length=255)
    responsabil = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)


STARI_OBIECTE_INVENTAR = (("nou", u"Nou"),
                          ("fb", u"Foarte bună"),
                          ("b", u"Bună"),
                          ("u", u"Utilizabil"),
                          ("r", u"Are nevoie de reparații"),
                          ("p", u"Proastă"))


class ObiectInventar(models.Model):
    # TODO: imagine pentru obiectul de inventar?

    denumire = models.CharField(max_length=255)
    descriere = models.TextField(null=True, blank=True)
    cod_inventar = models.CharField(max_length=255)

    responsabil = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)

    multi_part = models.BooleanField(default=False)
    unitate_de_masura = models.CharField(max_length=255)
    cantitate_curenta = models.PositiveIntegerField(default=1)

    categorie = models.ForeignKey(CategorieInventar, on_delete=models.SET_NULL, null=True, blank=True)
    locatie = models.ForeignKey(LocatieInventar, on_delete=models.CASCADE)

    stare = models.CharField(max_length=255, choices=STARI_OBIECTE_INVENTAR)


class IesireInventar(Document):
    ref_obiect_inventar = models.ForeignKey(ObiectInventar, on_delete=models.CASCADE)
    cantitate_scoasa = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField()
    responsabil = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)

    motiv = models.CharField(max_length=255, choices=(("activitate", u"Activitate"), ("imprumut", u"Împrumut"), ("casare", u"Casare"), ("distrugere", u"Distrugere")))
    activitate = models.ForeignKey(Eveniment, on_delete=models.CASCADE)


class IntrareInventar(Document):
    iesire_inventar = models.ForeignKey(IesireInventar, null=True, blank=True, on_delete=models.CASCADE)
    ref_obiect_inventar = models.ForeignKey(ObiectInventar, on_delete=models.CASCADE)
    cantitate_intrata = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField()
    responsabil = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)

    observatii = models.TextField(null=True, blank=True)
