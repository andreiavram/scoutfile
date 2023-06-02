from django.contrib.gis.db.models import PointField, PolygonField
from django.db import models


class LocationBaseModel(models.Model):
    name = models.CharField(max_length=1024)
    contact_person = models.CharField(max_length=255, blank=True)
    contact_details = models.CharField(max_length=255, blank=True)
    contact_person_internal = models.ForeignKey("structuri.Membru", null=True, blank=True, on_delete=models.SET_NULL)

    details = models.TextField()

    class Meta:
        abstract = True


class Place(LocationBaseModel):
    name = models.CharField(max_length=1024)
    point = PointField()


class ActivitySite(LocationBaseModel):
    name = models.CharField(max_length=1024)
    space = PolygonField()


class GPXTrack(models.Model):
    title = models.CharField(max_length=255)
    gpx_file = models.FileField(upload_to="locuri/gps/")

    place_start = PointField()
    time_start = models.DateTimeField()

    place_end = PointField()
    time_end = models.DateTimeField()

    positive_altitude = models.IntegerField()
    negative_altitude = models.IntegerField()
