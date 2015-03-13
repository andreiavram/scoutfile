from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from scoutfile3.s3utils import LocalStorage
import os
from django.conf import settings


def upload_to_cover_photo(instance, fn):
    return os.path.join("cartecantece", "cover", fn)


class Cantec(models.Model):
    nume_fisier = models.FilePathField(os.path.join(settings.LOCAL_MEDIA_ROOT, "cartecantece", "cantece"))
    titlu = models.CharField(max_length=255)
    artist = models.CharField(max_length=1024)

    #   TODO: create a better filename
    cover_photo = models.ImageField(upload_to=upload_to_cover_photo, null=True, blank=True)
    album = models.CharField(max_length=255, null=True, blank=True)
    tags = TaggableManager(blank=True)

    owner = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)

    def delete(self, **kwargs):
        if os.path.exists(self.nume_fisier):
            os.unlink(self.nume_fisier)
        return super(Cantec, self).delete(**kwargs)


class OptiuniTemplateCarteCantece(models.Model):
    nume = models.CharField(max_length=255)
    descriere = models.CharField(max_length=1024, null=True, blank=True)
    template = models.ForeignKey("TemplateCarteCantece")


def upload_to_template_carte_cantece(instance, fn):
    return os.path.join("cartecantece", "templates", fn)


class TemplateCarteCantece(models.Model):
    nume = models.CharField(max_length=255)
    template_file = models.FileField(upload_to=upload_to_template_carte_cantece, storage=LocalStorage)

    def __unicode__(self):
        return self.nume


class CarteCantece(models.Model):
    cantece = models.ManyToManyField(Cantec, through="ConexiuneCantecCarte")
    template = models.ForeignKey(TemplateCarteCantece)
    optiuni_template = models.ManyToManyField(OptiuniTemplateCarteCantece, null=True, blank=True)


class ConexiuneCantecCarte(models.Model):
    cantec = models.ForeignKey(Cantec)
    carte = models.ForeignKey(CarteCantece)

    status = models.CharField(max_length=255, choices=(("propus", u"Propus"), ("aprobat", u"Aprobat"), ("respins", u"Respins")))
    owner = models.ForeignKey(User, null=True, blank=True)