from django.db import models
from documente.models import Document
# Create your models here.
from structuri.models import RamuraDeVarsta


class CategorieFiseActivitate(models.Model):
    nume = models.CharField(max_length=255)
    #   do we need a tree structure here/

    def __unicode__(self):
        return self.nume


class FisaActivitate(Document):
    materiale_necesare = models.TextField(null=True, blank=True)
    ramuri_de_varsta = models.ManyToManyField(RamuraDeVarsta, null=True, blank=True)

    min_participanti = models.PositiveIntegerField(null=True, blank=True)
    max_participanti = models.PositiveIntegerField(null=True, blank=True)
    min_durata = models.PositiveIntegerField(null=True, blank=True)
    max_durata = models.PositiveIntegerField(null=True, blank=True)

    obiective_educative = models.TextField(null=True, blank=True)
    categorie = models.ForeignKey("CategorieFiseActivitate")

    sursa = models.CharField(max_length=255, null=True, blank=True)