from builtins import object
from django import forms
from django_ace.widgets import AceWidget
from goodies.forms import CrispyBaseModelForm, CrispyBaseForm
from goodies.widgets import TaggitTagsInput

from cantece.models import Cantec, CarteCantece

__author__ = 'andrei'


class CantecForm(CrispyBaseModelForm):
    class Meta(object):
        model = Cantec
        exclude = ("nume_fisier", "owner")

    tags = forms.CharField(label=u"Tag-uri", required=False, widget=TaggitTagsInput)


class CantecFileForm(CrispyBaseForm):
    song_content = forms.CharField(widget=AceWidget(mode='latex', theme='twilight', height="800px"))


class CarteCanteceForm(CrispyBaseModelForm):
    class Meta(object):
        model = CarteCantece
        exclude = []
