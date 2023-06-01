# coding: utf-8
from django.db import models
from django.db.models import TextChoices

from album.models import Eveniment
from documente.models import Document
from inventar.relationships import INVENTORY_RELATIONSHIPS_CHOICES


class LocatieInventar(models.Model):
    # TODO: imagine pentru locul de inventar?

    centru_local = models.ForeignKey("structuri.CentruLocal", on_delete=models.CASCADE)
    responsabil = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)
    adresa_fizica = models.TextField()
    imagine = models.ImageField(upload_to="inventar/locuri/", null=True, blank=True)


class CategorieInventar(models.Model):
    nume = models.CharField(max_length=255)
    responsabil = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)


class ObiectInventar(models.Model):
    class ConditieObiectInventar(TextChoices):
        NEW = "nou", u"Nou"
        VERY_GOOD = "fb", u"Foarte bună"
        GOOD = "b", u"Bună"
        USEABLE = "u", u"Utilizabil"
        NEED_REPAIR = "r", u"Are nevoie de reparații"
        POOR = "p", u"Proastă"
        NEED_REPLACING = "d", "De aruncat"

    titlu = models.CharField(max_length=255)
    descriere = models.TextField(null=True, blank=True)
    cod_inventar = models.CharField(max_length=255, unique=True)

    responsabil = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE, null=True, blank=True)

    is_container = models.BooleanField(default=False)
    is_multi_part = models.BooleanField(default=False)
    unitate_de_masura = models.CharField(max_length=255)
    cantitate_curenta = models.PositiveIntegerField(default=1)

    categorie = models.ForeignKey(CategorieInventar, on_delete=models.SET_NULL, null=True, blank=True)
    locatie = models.ForeignKey(LocatieInventar, on_delete=models.CASCADE)
    imagine = models.ImageField(upload_to="inventar/obiect/", null=True, blank=True)

    stare = models.CharField(max_length=255, choices=ConditieObiectInventar.choices)


class RelatieObiecteInventar(models.Model):
    obiect_inventar_sursa = models.ForeignKey(ObiectInventar, on_delete=models.CASCADE, related_name="targets")
    obiect_inventar_tinta = models.ForeignKey(ObiectInventar, on_delete=models.CASCADE, related_name="sources")
    tip_relatie = models.CharField(choices=INVENTORY_RELATIONSHIPS_CHOICES, null=True, blank=True, max_length=255)


class MentenantaObiectInventar(models.Model):
    obiect_inventar = models.ForeignKey(ObiectInventar, on_delete=models.CASCADE)
    titlu = models.CharField(max_length=255)
    descriere = models.TextField()
    perioada = models.DurationField()  # perioada la care trebuie facuta mentenanta


class ExecutieMentenantaObiectInventar(models.Model):
    mentenanta = models.ForeignKey(MentenantaObiectInventar, on_delete=models.CASCADE, null=True, blank=True)
    planificata_pentru = models.DateTimeField(null=True, blank=True)
    executata_la = models.DateTimeField(null=True, blank=True)
    executata_de = models.ForeignKey("structuri.Membru", on_delete=models.SET_NULL, null=True, blank=True)


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
