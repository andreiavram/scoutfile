#   based on https://github.com/zokis/django-bootstrap-datetimepicker
from builtins import object

from django import forms
from django.conf import settings
from django.db.models.aggregates import Count
from django.template.loader import render_to_string
from taggit.models import Tag

DATETIME_INPUT_FORMATS = getattr(settings, 'DATETIME_INPUT_FORMATS', None)
if DATETIME_INPUT_FORMATS:
    DATETIME_INPUT_FORMATS = DATETIME_INPUT_FORMATS[0]

class BootstrapDateTimeInput(forms.DateTimeInput):
    """ This is based on the awesome work from http://www.malot.fr/bootstrap-datetimepicker/
    """
    class Media(object):
        js = ("generic/js/bootstrap-datetimepicker.js",
              "generic/js/locales/bootstrap-datetimepicker.ro.js",
              "generic/js/bootstrap-datetimepicker-init.js",
        )

        css = {
            "screen" : (settings.STATIC_URL + "generic/css/datetimepicker.css", )
        }

    def __init__(self, *args, **kwargs):
        self.date_only = kwargs.pop("date_only", False)
        return super(BootstrapDateTimeInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        context_data = {"value": value, "attrs": attrs, "name" : name, "date_only" : self.date_only}
        return render_to_string("generic/bootstrapdatetime_widget.html", context_data)

class BootstrapDateInput(forms.DateInput):
    """ This is based on http://www.eyecon.ro/bootstrap-datepicker/
    """

    class Media(object):
        js = (
            "generic/js/bootstrap-datepicker.js",
            "generic/js/bootstrap-datepicker-init.js",
        )
        css = {
            "screen" : ("generic/css/datepicker.css", )
        }

    def render(self, name, value, attrs=None):
        context_data = {"value": value, "attrs": attrs, "name": name}
        return render_to_string("generic/bootstrapdate_widget.html", context_data)


class GeoCoordinatesInput(forms.TextInput):
    class Media(object):
        js = (
            "http://maps.googleapis.com/maps/api/js?key={0}&sensor=true".format(settings.GOOGLE_API_KEY),
            settings.STATIC_URL + "generic/js/map_widget.js",
        )
        css = {
            "screen" : (settings.STATIC_URL + "generic/css/map_widget.css", )
        }

    def render(self, name, value, attrs=None):
        return render_to_string("generic/map_widget.html", {"value": value, "attrs":
            attrs, "name": name})

class FacebookLinkWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        return render_to_string("generic/facebook_link_widget.html", {"value" : value, "attrs" : attrs, "name" : name})

class TaggitTagsInput(forms.TextInput):
    """ This uses the very awesome http://welldonethings.com/tags/manager/v3
    """
    class Media(object):
        js = (
            "generic/js/typeahead.js", # uses https://github.com/twitter/typeahead.js
            "generic/js/tagmanager.js", # uses https://github.com/max-favilli/tagmanager
            "generic/js/tagmanager-init.js",
        )

        css = {
            "screen": ("generic/css/tagmanager.css", )
        }

    def __init__(self, *args, **kwargs):
        self.show_available_tags = kwargs.pop("show_available_tags", False)
        self.tag_limit = kwargs.pop("tag_limit", 20)
        return super(TaggitTagsInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        tags = None
        if self.show_available_tags:
            tags = Tag.objects.all().annotate(num_times=Count("taggit_taggeditem_items")).order_by("-num_times")[:self.tag_limit]
        context = {"name": name, "value": value, "attrs": attrs, "tags" : tags}
        return render_to_string("generic/tag_input_widget.html", context)
