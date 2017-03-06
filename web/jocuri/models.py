# coding: utf-8
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
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


# TODO: remove this override when https://github.com/alex/django-taggit/issues/282 is closed
class FixedTaggableManager(TaggableManager):
    def get_joining_columns(self, reverse_join=False):
        if reverse_join:
            return ((self.model._meta.pk.column, "object_id"),)
        else:
            return (("object_id", self.model._meta.pk.column),)


class FisaActivitate(Document):
    descriere_joc = models.TextField(null=True, blank=True, verbose_name=u"Descriere")

    materiale_necesare = models.TextField(null=True, blank=True, help_text=u"Câte unul pe linie, fără numerotare adițională")
    ramuri_de_varsta = models.ManyToManyField("structuri.RamuraDeVarsta", blank=True)

    min_participanti = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"Minim participanți")
    max_participanti = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"Maxim participanți")
    min_durata = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"Durata minimă", help_text=u"Folosește expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m")
    max_durata = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"Durata maximă", help_text=u"Folosește expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m")

    obiective_educative = models.TextField(null=True, blank=True, help_text=u"Câte unul pe linie, fără numerotare (se va face automat)")
    categorie = models.ForeignKey("CategorieFiseActivitate")

    sursa = models.CharField(max_length=255, null=True, blank=True, help_text=u"De unde ați adus jocul / activitatea asta în grupul vostru")
    editori = models.ManyToManyField("structuri.Membru")
    is_draft = models.BooleanField(default=True, verbose_name=u"Este incomplet?", help_text=u"Dacă nu ești chiar gata, marchează bifa aici ca să știe și ceilalți")

    tags = FixedTaggableManager()

    def save(self, **kwargs):
        self.tip_document = TipDocument.obtine("fisa_activitate")
        return super(FisaActivitate, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse("jocuri:activitate_detail", kwargs={"pk": self.id})
