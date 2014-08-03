from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from s3utils import LocalStorage
import os
from django.conf import settings


class Cantec(models.Model):
    nume_fisier = models.FilePathField(os.path.join(settings.LOCAL_MEDIA_ROOT, "cartecantece", "cantece"))
    titlu = models.CharField(max_length=255)
    artist = models.CharField(max_length=1024)
    #   TODO: create a better filename
    cover_photo = models.ImageField(upload_to=lambda instance, fn: os.path.join("cartecantece", "cover", fn), null=True, blank=True)
    album = models.CharField(max_length=255, null=True, blank=True)
    tags = TaggableManager()

    owner = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)


class OptiuniTemplateCarteCantece(models.Model):
    nume = models.CharField(max_length=255)
    descriere = models.CharField(max_length=1024, null=True, blank=True)
    template = models.ForeignKey("TemplateCarteCantece")


class TemplateCarteCantece(models.Model):
    nume = models.CharField(max_length=255)
    template_file = models.FileField(upload_to=lambda instance, fn: os.path.join("cartecantece", "templates", fn), storage=LocalStorage())

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