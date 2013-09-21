#coding: utf-8
from django.db import models
from photologue.models import ImageModel
from PIL import Image
import datetime
from scoutfile3.structuri.models import CentruLocal, Membru, TipAsociereMembruStructura
from scoutfile3.settings import MEDIA_ROOT
import os
from zipfile import ZipFile
import logging
import traceback
from scoutfile3.settings import SCOUTFILE_ALBUM_STORAGE_ROOT, STATIC_ROOT
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
from structuri.models import RamuraDeVarsta

logger = logging.getLogger(__name__)


class Eveniment(models.Model):
    centru_local = models.ForeignKey(CentruLocal)
    nume = models.CharField(max_length = 255)
    descriere = models.CharField(max_length = 1024, null = True, blank = True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    slug = models.CharField(max_length = 255)

    custom_cover_photo = models.ForeignKey("Imagine", null=True, blank=True)

    facebook_event_link = models.URLField(null=True, blank=True)
    tags = TaggableManager()

    locatie_text = models.CharField(max_length=1024, null=True, blank=True)
    locatie_lat = models.FloatField(default=0)
    locatie_long = models.FloatField(default=0)

    #TODO: add visibility settings to events

    
    class Meta:
        verbose_name = u"Eveniment"
        verbose_name_plural = u"Evenimente"
        ordering = ["-start_date"]
    
    def __unicode__(self):
        return u"%s" % self.nume
    
    def save(self, *args, **kwargs):
        on_create = False
        if self.id == None:
            on_create = True
        
        retval = super(Eveniment, self).save(*args, **kwargs)

        if on_create:
            #    just on create
            zi_index = 1
            date = self.start_date
            while date <= self.end_date:
                zi_eveniment = ZiEveniment(eveniment = self, date = date, index = zi_index)
                zi_index += 1
                date += datetime.timedelta(days = 1)
                
                zi_eveniment.titlu = u"Ziua %d" % zi_eveniment.index
                zi_eveniment.save()

        return retval

    def get_autori(self):
        autori = []
        for set_poze in self.setpoze_set.all():
            if set_poze.autor not in autori:
                autori.append(set_poze.autor)
                
        return autori
    
    def cover_photo(self):
        if self.custom_cover_photo:
            return self.custom_cover_photo

        if self.setpoze_set.all().count() == 0:
            return None
        
        for set_poze in self.setpoze_set.all():
            if set_poze.imagine_set.all().count():
                return set_poze.imagine_set.all()[0]
        
        return None

    @property
    def total_poze(self):
        return Imagine.objects.filter(set_poze__eveniment = self).count()

    def get_visibility_level(self, user=None):
        if user is None:
            return 4

        #   decide visibility level to go for
        if user is not None and user.is_authenticated():
            visibility_level = 3    #   this means organization level, logged in user
            user_profile = user.get_profile().membru
            if user_profile.centru_local == self.centru_local:
                visibility_level = 2
                if user_profile.are_calitate(TipAsociereMembruStructura.objects.get(nume=u"Păstrător al amintirilor"), self.centru_local):
                    visibility_level = 1

        #   superuser override
        if user.is_superuser:
            visibility_level = 1

        return visibility_level

STATUS_PARTICIPARE = ((1, u"Cu semnul întrebării"), (2, u"Sigur"), (3, u"Avans plătit"), (4, u"Participare efectivă"), (5, u"Participare anulată"))
class ParticipareEveniment(models.Model):
    membru = models.ForeignKey(Membru)
    eveniment = models.ForeignKey(Eveniment)
    data_sosire = models.DateTimeField(null=True, blank=True)
    data_plecare = models.DateTimeField(null=True, blank=True)

    status_participare = models.IntegerField(default=1, choices=STATUS_PARTICIPARE)
    detalii = models.TextField(null=True, blank=True)

    @property
    def is_partiala(self):
        return self.data_sosire.date() != self.eveniment.start_date.date() or self.data_plecare.date() != self.eveniment.end_date.date()

class ZiEveniment(models.Model):
    eveniment = models.ForeignKey(Eveniment)
    date = models.DateField()
    titlu = models.CharField(max_length = 255)
    descriere = models.CharField(max_length = 1024)
    index = models.IntegerField(default = 1)
    
    class Meta:
        verbose_name = u"Zi eveniment"
        verbose_name_plural = u"Zile eveniment"
        ordering = ["date"]
        
    def __unicode__(self):
        if self.titlu != None and self.titlu != "":
            return self.titlu
        return u"Ziua %d" % self.index
    
    def filter_photos(self, autor=None, user=None):
        backward_limit = datetime.datetime.combine(self.date, datetime.time(0, 0, 0)) + datetime.timedelta(hours = 3)
        images = Imagine.objects.filter(set_poze__eveniment = self.eveniment, data__gte = backward_limit, data__lte = self.date + datetime.timedelta(days = 1))
        if autor is not None:
            images = images.filter(set_poze__autor__icontains=autor)

        images = images.exclude(published_status__lt=self.eveniment.get_visibility_level(user))
        images = images.order_by("data")
        return images
    
    def author_distribution(self):
        authors = {}
        for image in self.filter_photos():
            if image.set_poze.autor.strip() in authors.keys():
                authors[image.set_poze.autor.strip()] += 1
            else:
                authors[image.set_poze.autor.strip()] = 1
                
        return authors
            
SET_POZE_STATUSES = ((0, "Initialized"), (1, "Zip Uploaded"), (2, "Zip queued for processing"), (3, "Zip processed OK"), (4, "Zip error"))
class SetPoze(models.Model):
    eveniment = models.ForeignKey(Eveniment)
    autor = models.CharField(max_length = 255, null = True, blank = True, help_text = u"Lăsați gol dacă încărcați pozele proprii")
    autor_user = models.ForeignKey(Membru, null = True, blank = True)
    zip_file = models.FilePathField(null = True, blank = True, path = "/tmp")
    status = models.IntegerField(default = 0, choices = SET_POZE_STATUSES)
    procent_procesat = models.IntegerField()

    date_uploaded = models.DateTimeField(auto_now=True)
    offset_secunde = models.IntegerField(default = 0, help_text = "Numărul de secunde cu care ceasul camerei voastre a fost decalat față de ceasul corect (poate fi și negativ). Foarte util pentru sincronizarea pozelor de la mai mulți fotografi")
    
    class Meta:
        verbose_name = u"Set poze"
        verbose_name_plural = "seturi poze"
        ordering = ["-date_uploaded"]

    def __unicode__(self):
        return u"Set %s (%s)" % (self.autor, self.eveniment) 
    
    def get_autor(self):
        return u"%s" % self.autor.strip()
    
    def process_zip_file(self):
        self.status = 2
        self.save()
        
        try:
            event_path_no_root = os.path.join(SCOUTFILE_ALBUM_STORAGE_ROOT, unicode(self.eveniment.centru_local.id), unicode(self.eveniment.id), self.autor.replace(" ", "_")) 
            event_path = os.path.join(MEDIA_ROOT, event_path_no_root) 
            if not os.path.exists(os.path.join(MEDIA_ROOT, event_path)):
                os.makedirs(os.path.join(MEDIA_ROOT, event_path))

            with ZipFile(self.zip_file) as zf:
                total_count = len(zf.infolist())
                current_count = 0
                for f in zf.infolist():
                    logger.debug("SetPoze: fisier extras %s" % f)
                    if f.filename.endswith("/") or os.path.splitext(f.filename)[1].lower() not in (".jpg", ".jpeg", ".png"):
                        logger.debug("SetPoze skipping %s %s %s" % (f, f.filename, os.path.splitext(f.filename)[1].lower()))
                        continue
                    logger.debug("SetPoze: extracting file %s to %s" % (f.filename, event_path))
                    zf.extract(f, event_path)
                    im = Imagine(set_poze = self, titlu = os.path.basename(f.filename), image = os.path.join(event_path_no_root, f.filename))
                    logger.debug("SetPoze: poza: %s" % im.image)
                    im.save()
                    current_count += 1
                    current_percent = current_count * 100. / total_count
                    if current_percent - 5 > self.procent_procesat:
                        self.procent_procesat = int(current_percent)
                        self.save()
                    
        except Exception, e:
            self.status = 4
            self.save()
            logger.error("SetPoze: error extracting files: %s (%s)" % (e, traceback.format_exc()))
            return
            
        self.status = 3
        self.save()
    
        os.unlink(self.zip_file)

IMAGINE_PUBLISHED_STATUS = ((1, "Secret"), (2, "Centru Local"), (3, "Organizație"), (4, "Public"))
class Imagine(ImageModel):
    set_poze = models.ForeignKey(SetPoze)
    data = models.DateTimeField(null = True, blank = True)
    titlu = models.CharField(max_length = 1024, null = True, blank = True)
    descriere = models.CharField(max_length = 2048, null = True, blank = True)
    resolution_x = models.IntegerField(null = True, blank = True)
    resolution_y = models.IntegerField(null = True, blank = True)
    
    score = models.IntegerField(default = 0)
    is_deleted = models.BooleanField()
    is_flagged = models.BooleanField()
    is_face_processed = models.BooleanField()
    
    published_status = models.IntegerField(default = 2, choices = IMAGINE_PUBLISHED_STATUS)

    tags = TaggableManager()
    
    class Meta:
        verbose_name = u"Imagine"
        verbose_name_plural = u"Imagini"
        ordering = ["date_taken", ]
    
    def rotate(self, direction = "cw"):
        im = Image.open(self.image)
        
        angle = -90
        if direction == "cw":
            angle = -90
        else:
            angle = 90
        
        im = im.rotate(angle)
        im.save("%s%s" % (MEDIA_ROOT, self.image))
        
        if os.path.exists(self.get_large_filename()):
            os.unlink(self.get_large_filename())
        if os.path.exists(self.get_thumbnail_filename()):
            os.unlink(self.get_thumbnail_filename())
        if os.path.exists(self.get_profile_filename()):
            os.unlink(self.get_profile_filename())
        
        return
        
    def get_day(self):
        return self.set_poze.eveniment.zieveniment_set.get(date = self.data)

    def get_next_photo(self, autor = None, user=None):
        photo = Imagine.objects.filter(published_status__gte = self.set_poze.eveniment.get_visibility_level(user=user),
                                       set_poze__eveniment = self.set_poze.eveniment,
                                       data__gt = self.data,
                                       data__lte = self.get_day().date + datetime.timedelta(days = 1))
        if autor != None:
            photo = photo.filter(set_poze__autor__icontains = autor)
            
        photo = photo.order_by("data")
        
        if photo.count():
            return photo[0]
        return None
    
    def get_prev_photo(self, autor = None, user=None):
        backward_limit = datetime.datetime.combine(self.get_day().date, datetime.time(0, 0, 0)) + datetime.timedelta(hours = 3)
        photo = Imagine.objects.filter(published_status__gte = self.set_poze.eveniment.get_visibility_level(user=user),
                                       set_poze__eveniment = self.set_poze.eveniment,
                                       data__lt = self.data, data__gte = backward_limit)
        if autor is not None:
            photo = photo.filter(set_poze__autor__icontains = autor)
        photo = photo.order_by("-data")

        if photo.count():
            return photo[0]
        return None
    
    def interesting_exifdata(self):
        return self.exifdata_set.filter(key__in = ("Model", ))
     
    def save(self, *args, **kwargs):
        im = None
        if self.resolution_x is None or self.resolution_y is None:
            logger.debug("Imagine.save: opening file: %s" % os.path.join(MEDIA_ROOT, "%s" % self.image))
            im = Image.open(os.path.join(MEDIA_ROOT, "%s" % self.image))
            self.resolution_x, self.resolution_y = im.size
        
        on_create = False
        if self.id is None:
            on_create = True
            if im is None:
                im = Image.open(self.image)
            info = im._getexif()
    
            exif_data = {}
            
            #    get current EXIF data
            if info is not None:
                for tag, value in info.items():
                    from PIL import ExifTags
                    decoded = ExifTags.TAGS.get(tag, tag)
                    if decoded == u"Maker Note":
                        continue
                    
                    if decoded == u"DateTimeOriginal":
                        self.data = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    
                    exif_data[decoded] = value
            
        retval = super(Imagine, self).save(*args, **kwargs)
        
        if not self.is_face_processed:
            if not on_create:
                #    delete any existing faces, thus allowing detected face reset by
                #    switching the is_face_processed flag
                self.detectedface_set.all().delete()
            self.find_faces()
            self.is_face_processed = True        

        if on_create:
            #    clear currently EXIF data
            self.exifdata_set.all().delete()
    
            for key, value in exif_data.items():
                exif = EXIFData(imagine = self, key = key, value = value)
                try:
                    exif.save()
                except Exception, e:
                    continue
            
        return retval

    def vote_photo(self, score):
        self.score += score
        self.save()
        
    def find_faces(self):
        import cv
        
        imcolor = cv.LoadImage("%s/%s" % (MEDIA_ROOT, self.image)) #@UndefinedVariable
        detectors = ["haarcascade_frontalface_default.xml", "haarcascade_profileface.xml"]
        for detector in detectors:
            haarFace = cv.Load(os.path.join(STATIC_ROOT, detector))  # @UndefinedVariable
            storage = cv.CreateMemStorage() #@UndefinedVariable
            detectedFaces = cv.HaarDetectObjects(imcolor, haarFace, storage, min_size = (200, 200)) #@UndefinedVariable
            if detectedFaces:
                for face in detectedFaces:
                    fata = DetectedFace(imagine = self, x = face[0][0], y = face[0][1], width = face[0][2], height = face[0][3])
                    fata.save()
                
        self.is_face_processed = True
        self.save()


        
        
# tagging.register(Imagine)

class EXIFData(models.Model):
    imagine = models.ForeignKey(Imagine)
    key = models.CharField(max_length = 255)
    value = models.CharField(max_length = 255)
    
    class Meta:
        verbose_name = u"EXIFData"
        verbose_name_plural = u"EXIFData"
        
    def __unicode__(self):
        return "%s: %s" % (self.key, self.value)
    
FLAG_MOTIVES = (("personal", u"Sunt în poză și nu sunt de acord să apară aici"), 
                ("ofensa", "Consider că poza este ofensatoare"), 
                ("nonscout", "Poza conține un comportament necercetășesc și nu ar trebui listată aici"), 
                ("calitateslaba", u"Poza este de calitate slabă și nu merită păstrată"), 
                ("altul", "Alt motiv"))

class FlagReport(models.Model):
    imagine = models.ForeignKey(Imagine)
    motiv = models.CharField(max_length = 1024, choices = FLAG_MOTIVES)
    alt_motiv = models.CharField(max_length = 1024, null = True, blank = True)
    
    timestamp = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        verbose_name = u"Raport poză"
        verbose_name_plural = u"Rapoarte poze"
        ordering = ["-timestamp", "motiv"]
        
    def __unicode__(self):
        return "Raport de %s la " % self.motiv
    
    
class DetectedFace(models.Model):
    imagine = models.ForeignKey(Imagine)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    
    content_type = models.ForeignKey(ContentType, null = True, blank = True)
    object_id = models.PositiveIntegerField(null = True, blank = True)
    content_object = GenericForeignKey()
    