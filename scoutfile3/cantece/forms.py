from django_ace.widgets import AceWidget
from goodies.forms import CrispyBaseModelForm, CrispyBaseForm
from cantece.models import Cantec, CarteCantece
from goodies.widgets import TaggitTagsInput
from django import forms

__author__ = 'andrei'


class CantecForm(CrispyBaseModelForm):
    class Meta:
        model = Cantec
        exclude = ("nume_fisier", "owner")

    tags = forms.CharField(label=u"Tag-uri", required=False, widget=TaggitTagsInput)


class CantecFileForm(CrispyBaseForm):
    song_content = forms.CharField(widget=AceWidget(mode='latex', theme='twilight'))


class CarteCanteceForm(CrispyBaseModelForm):
    class Meta:
        model = CarteCantece
