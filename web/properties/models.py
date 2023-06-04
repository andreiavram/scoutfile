import requests
from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PointField
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import IntegerChoices


class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    place = PointField()

    ha_base_url = models.URLField(null=True, blank=True)
    ha_access_token = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        return self.name


class PropertyControlElement(models.Model):
    name = models.CharField(max_length=255)
    ha_id = models.CharField(max_length=255)
    service_action = models.CharField(max_length=255)

    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.property.name} - {self.name}({self.ha_id})"

    def activate(self, actor):
        if self.property.ha_base_url is None:
            raise ImproperlyConfigured(f"{self} doesn't have a Property with HA configured")

        url = f"{self.property.ha_base_url}/{self.ha_id.split('.')[0]}/{self.service_action}"
        headers = {"Authorization": f"Bearer {self.property.ha_access_token}"}
        data = {"entity_id": self.ha_id}
        response = requests.post(url, headers=headers, json=data)
        result = response.status_code == 200

        AccessLog.objects.create(
            control_element=self,
            person=actor,
            control_data=data,
            result=result
        )


class AccessPermission(models.Model):
    control_element = models.ForeignKey(PropertyControlElement, on_delete=models.CASCADE)
    person = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True)

    # TODO: maybe handle this with groups or just use this for one-offs and handle groups somewhere else?


class AccessLog(models.Model):
    class ResultOptions(IntegerChoices):
        SUCCESS = 1, "Success"
        FAILURE = 2, "Failure"

    control_element = models.ForeignKey(PropertyControlElement, on_delete=models.CASCADE)
    person = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    control_data = models.JSONField(default=dict)
    result = models.PositiveSmallIntegerField(choices=ResultOptions.choices, default=ResultOptions.SUCCESS)
