#coding: utf-8
from django.db import models
import tagging
from photologue.models import ImageModel
import Image
import datetime
from scoutfile3.structuri.models import CentruLocal
from scoutfile3.settings import MEDIA_ROOT
import os

class Eveniment(models.Model):
    centru_local = models.ForeignKey(CentruLocal)
    nume = models.CharField(max_length = 255)
    descriere = models.CharField(max_length = 1024, null = True, blank = True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    slug = models.CharField(max_length = 255)
    
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
        if self.setpoze_set.all().count() == 0:
            return None
        
        for set_poze in self.setpoze_set.all():
            if set_poze.imagine_set.all().count():
                return set_poze.imagine_set.all()[0]
        
        return None
    
    def total_poze(self):
        return Imagine.objects.filter(set_poze__eveniment = self).count()
    
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
    
    def filter_photos(self, autor = None):
        backward_limit = datetime.datetime.combine(self.date, datetime.time(0, 0, 0)) + datetime.timedelta(hours = 3)
        images = Imagine.objects.filter(set_poze__eveniment = self.eveniment, data__gte = backward_limit, data__lte = self.date + datetime.timedelta(days = 1))
        if autor != None:
            images = images.filter(set_poze__autor__icontains = autor)
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
            
class SetPoze(models.Model):
    eveniment = models.ForeignKey(Eveniment)
    autor = models.CharField(max_length = 255)
    
    offset_secunde = models.IntegerField(default = 0)
    
    class Meta:
        verbose_name = u"Set poze"
        verbose_name_plural = "seturi poze"

    def __unicode__(self):
        return u"Set %s (%s)" % (self.autor, self.eveniment) 
    
    def get_autor(self):
        return u"%s" % self.autor.strip()
        
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

    def get_next_photo(self, autor = None):
        photo = Imagine.objects.filter(set_poze__eveniment = self.set_poze.eveniment, data__gt = self.data, data__lte = self.get_day().date + datetime.timedelta(days = 1))
        if autor != None:
            photo = photo.filter(set_poze__autor__icontains = autor)
            
        photo = photo.order_by("data")
        
        if photo.count():
            return photo[0]
        return None
    
    def get_prev_photo(self, autor = None):
        backward_limit = datetime.datetime.combine(self.get_day().date, datetime.time(0, 0, 0)) + datetime.timedelta(hours = 3)
        photo = Imagine.objects.filter(set_poze__eveniment = self.set_poze.eveniment, data__lt = self.data, data__gte = backward_limit)
        if autor != None:
            photo = photo.filter(set_poze__autor__icontains = autor)
        photo = photo.order_by("-data")

        if photo.count():
            return photo[0]
        return None
    
    def interesting_exifdata(self):
        return self.exifdata_set.filter(key__in = ("Model", ))
     
    def save(self, *args, **kwargs):
        im = None
        if self.resolution_x == None or self.resolution_y == None:
            im = Image.open(self.image)
            self.resolution_x, self.resolution_y = im.size
        
        on_create = False
        if self.id == None:
            on_create = True
            if im == None:
                im = Image.open(self.image)
            info = im._getexif()
    
            exif_data = {}
            
            #    get current EXIF data
            if info != None:
                for tag, value in info.items():
                    from ExifTags import TAGS
                    decoded = TAGS.get(tag, tag)
                    if decoded == u"Maker Note":
                        continue
                    
                    if decoded == u"DateTimeOriginal":
                        self.data = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    
                    exif_data[decoded] = value
            
        retval = super(Imagine, self).save(*args, **kwargs)

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
        
        
tagging.register(Imagine)

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