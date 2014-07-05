from django.db import models

# Create your models here.
from album.models import Eveniment
from documente.models import Document
from structuri.models import CentruLocal, Membru


class LocateiInventar(models.Model):
    # TODO: imagine pentru locul de inventar?

    centru_local = models.ForeignKey(CentruLocal)
    responsabil = models.ForeignKey(Membru)


class CategorieInventar(models.Model):
    nume = models.CharField(max_length=255)
    responsabil = models.ForeignKey(Membru)


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

    responsabil = models.ForeignKey(Membru)

    multi_part = models.BooleanField()
    unitate_de_masura = models.CharField(max_length=255)
    cantitate_curenta = models.PositiveIntegerField(default=1)

    categorie = models.ForeignKey(CategorieInventar, null=True, blank=True)
    locatie = models.ForeignKey(LocateiInventar)

    stare = models.CharField(max_length=255, choices=STARI_OBIECTE_INVENTAR)


class IesireInventar(Document):
    ref_obiect_inventar = models.ForeignKey(ObiectInventar)
    cantitate_scoasa = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField()
    responsabil = models.ForeignKey(Membru)

    motiv = models.CharField(max_length=255, choices=(("activitate", u"Activitate"), ("imprumut", u"Împrumut"), ("casare", u"Casare"), ("distrugere", u"Distrugere")))
    activitate = models.ForeignKey(Eveniment)


class IntrareInventar(Document):
    iesire_inventar = models.ForeignKey(IesireInventar, null=True, blank=True)
    ref_obiect_inventar = models.ForeignKey(ObiectInventar)
    cantitate_intrata = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField()
    responsabil = models.ForeignKey(Membru)

    observatii = models.TextField(null=True, blank=True)


