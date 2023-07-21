import datetime

import gpxpy
from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PointField, PolygonField
from django.contrib.gis.geos import Point
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import IntegerChoices


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
    class ProcessStatus(IntegerChoices):
        PENDING = 0, "Pending"
        PROCESSED = 1, "Processed"

    title = models.CharField(max_length=255, verbose_name="Nume")
    gpx_file = models.FileField(
        upload_to="locuri/gps/",
        verbose_name="Fișier GPX",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'gpx'
                ]
            )
        ]
    )

    source_url = models.URLField(null=True, blank=True, verbose_name="URL sursă")
    created_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.CASCADE)

    place_start = PointField(null=True, blank=True)
    time_start = models.DateTimeField(null=True, blank=True)

    place_end = PointField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)

    positive_altitude = models.IntegerField(null=True, blank=True)
    negative_altitude = models.IntegerField(null=True, blank=True)
    highest_point = models.IntegerField(null=True, blank=True)
    lowest_point = models.IntegerField(null=True, blank=True)

    moving_time = models.DurationField(null=True, blank=True)
    max_speed = models.FloatField(null=True, blank=True)
    total_distance = models.FloatField(null=True, blank=True)

    duration = models.DurationField(null=True, blank=True)

    process_status = models.PositiveSmallIntegerField(choices=ProcessStatus.choices, default=ProcessStatus.PENDING)

    def __str__(self):
        return self.title

    def process_gpx(self):
        gpx_file = open(self.gpx_file.path, "r")
        gpx = gpxpy.parse(gpx_file)

        uphill_downhill = gpx.get_uphill_downhill()
        self.positive_altitude = uphill_downhill.uphill
        self.negative_altitude = uphill_downhill.downhill

        elevation_extremes = gpx.get_elevation_extremes()
        self.highest_point = elevation_extremes.maximum
        self.lowest_point = elevation_extremes.minimum

        durations_secs = gpx.get_duration()
        self.duration = datetime.timedelta(seconds=durations_secs)

        # as per gpxpy docstrings
        cloned_gpx = gpx.clone()
        cloned_gpx.reduce_points(gpx.get_track_points_no() * .1, min_distance=10)
        cloned_gpx.smooth(vertical=True, horizontal=True)
        cloned_gpx.smooth(vertical=True, horizontal=False)
        moving_time, _, total_distance, _, max_speed_ms = cloned_gpx.get_moving_data()
        self.moving_time = datetime.timedelta(seconds=moving_time)
        self.total_distance = total_distance / 1000.
        self.max_speed = max_speed_ms * 60. ** 2 / 1000.

        self.time_start, self.time_end = gpx.get_time_bounds()

        first = gpx.tracks[0].segments[0].points[0]
        last = gpx.tracks[-1].segments[-1].points[-1]
        self.place_start = Point(first.latitude, first.longitude)
        self.place_end = Point(last.latitude, last.longitude)

        self.process_status = GPXTrack.ProcessStatus.PROCESSED
        self.save()




