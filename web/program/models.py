from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from album.models import Imagine
from structuri.models import RamuraDeVarsta, Membru


DOMENII_DEZVOLTARE = (("intelectual", "Intelectual"),
                      ("fizic", "Fizic"),
                      ("afectiv", "Afectiv"),
                      ("social", "Social"),
                      ("caracter", "Caracter"),
                      ("spiritual", "Spiritual"))


# Create your models here.
class ObiectivEducativProgres(models.Model):
    titlu = models.CharField(max_length=2048)
    descriere = models.TextField(null=True, blank=True)
    domeniu = models.CharField(max_length=255, choices=DOMENII_DEZVOLTARE)
    pista = models.CharField(max_length=1024, null=True, blank=True)


class EtapaProgres(models.Model):
    ramura_de_varsta = models.ForeignKey(RamuraDeVarsta, on_delete=models.CASCADE)
    nume = models.CharField(max_length=255)
    logo = models.ForeignKey(Imagine, on_delete=models.SET_NULL, null=True, blank=True)
    ordine = models.PositiveSmallIntegerField(null=True, blank=True)
    slug = models.SlugField()

    reguli = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.nume


class BadgeMerit(models.Model):
    ramura_de_varsta = models.ForeignKey(RamuraDeVarsta, null=True, blank=True, on_delete=models.CASCADE)
    etapa_progres = models.ForeignKey(EtapaProgres, null=True, blank=True, on_delete=models.CASCADE)
    nume = models.CharField(max_length=255)
    descriere = models.TextField(null=True, blank=True)
    logo = models.ForeignKey(Imagine, null=True, blank=True, on_delete=models.SET_NULL)


class TargetEtapaProgres(models.Model):
    titlu = models.CharField(max_length=2048)
    capitol = models.CharField(max_length=2048)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey()


class EtapaProgresMembru(models.Model):
    etapa_progres = models.ForeignKey(EtapaProgres, on_delete=models.CASCADE)
    membru = models.ForeignKey(Membru, related_name="etape_progres", on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Membru, related_name="etape_progres_evaluate", on_delete=models.CASCADE)
    data = models.DateField()
    detalii = models.TextField(null=True, blank=True)


class BadgeMeritMembru(models.Model):
    badge = models.ForeignKey(BadgeMerit, on_delete=models.CASCADE)
    membru = models.ForeignKey(Membru, related_name="badgeuri_merit", on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Membru, related_name="badgeuri_merit_evaluate", on_delete=models.CASCADE)
    data = models.DateField()
    detalii = models.TextField(null=True, blank=True)


class NoteObiectivProgresMembru(models.Model):
    obiectiv = models.ForeignKey(ObiectivEducativProgres, on_delete=models.CASCADE)
    nota = models.TextField()

    membru = models.ForeignKey(Membru, related_name="note_obiective_progres", on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Membru, related_name="note_obiective_progres_evaluate", on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    activitate = models.ForeignKey("album.Eveniment", null=True, blank=True, on_delete=models.SET_NULL)
    obiectiv_atins = models.BooleanField(default=False)
    etapa_progres = models.ForeignKey(EtapaProgres, on_delete=models.CASCADE)


class NotaTargetEtapaProgres(models.Model):
    target = models.ForeignKey(TargetEtapaProgres, on_delete=models.CASCADE)

    membru = models.ForeignKey(Membru, related_name="note_etape_progres", on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Membru, related_name="note_etape_progres_evaluate", on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
    target_atins = models.BooleanField(default=False)

    activitate = models.ForeignKey("album.Eveniment", on_delete=models.SET_NULL, null=True, blank=True)

