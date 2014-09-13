# coding: utf-8
from django.db import models
from taggit.managers import TaggableManager
from documente.models import Document, TipDocument
# Create your models here.
# from structuri.models import RamuraDeVarsta


class CategorieFiseActivitate(models.Model):
    nume = models.CharField(max_length=255)
    #   do we need a tree structure here/

    def __unicode__(self):
        return self.nume


class FisaActivitate(Document):
    descriere_joc = models.TextField(null=True, blank=True, verbose_name=u"Descriere")

    materiale_necesare = models.TextField(null=True, blank=True, help_text=u"Câte unul pe linie, fără numerotare adițională")
    ramuri_de_varsta = models.ManyToManyField("structuri.RamuraDeVarsta", null=True, blank=True)

    min_participanti = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"Minim participanți")
    max_participanti = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"Maxim participanți")
    min_durata = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"Durata minimă", help_text=u"Folosește expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m")
    max_durata = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"Durata maximă", help_text=u"Folosește expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m")

    obiective_educative = models.TextField(null=True, blank=True, help_text=u"Câte unul pe linie, fără numerotare (se va face automat)")
    categorie = models.ForeignKey("CategorieFiseActivitate")

    sursa = models.CharField(max_length=255, null=True, blank=True, help_text=u"De unde ați adus jocul / activitatea asta în grupul vostru")

    tags = TaggableManager()

    def save(self, **kwargs):
        self.tip_document = TipDocument.obtine("fisa_activitate")
        return super(FisaActivitate, self).save(**kwargs)