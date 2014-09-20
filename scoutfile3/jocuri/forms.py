# coding: utf-8
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput, Textarea
from django_markdown.widgets import MarkdownWidget
from goodies.forms import CrispyBaseModelForm
from goodies.widgets import TaggitTagsInput
from pagedown.widgets import PagedownWidget
from taggit.forms import TagField
from documente.models import Document
from jocuri.models import FisaActivitate
from django import forms
from structuri.models import RamuraDeVarsta

__author__ = 'andrei'


class FisaActivitateForm(CrispyBaseModelForm):
    class Meta:
        model = FisaActivitate
        fields = ("titlu", "descriere", "descriere_joc", "materiale_necesare", "ramuri_de_varsta",
                    "min_participanti", "max_participanti",
                    "obiective_educative", "categorie", "sursa", "tags")

    min_durata_string = forms.CharField(required=False, label=u"Durată minimă", help_text=u"Folosește expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m")
    max_durata_string = forms.CharField(required=False, label=u"Durată maximă", help_text=u"Folosește expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m")
    descriere_joc = forms.CharField(required=True, label=u"Descriere", help_text=u"Format Markdown, descrierea jocului, ce trebuie pregătit, ce trebuie făcut, care este obiectivul, care sunt regulile ...", widget=MarkdownWidget)
    descriere = forms.CharField(required=False, label=u"Descriere pe scurt", help_text=u"Un text de descriere pentru căutare", widget=Textarea())
    ramuri_de_varsta = forms.ModelMultipleChoiceField(RamuraDeVarsta.objects.all(), required=True, label=u"Ramuri de vârstă", help_text=u"Alegeți mărcar una", widget=forms.CheckboxSelectMultiple)
    tags = TagField(required=False, widget=TaggitTagsInput, label=u"Tag-uri")


    def clean(self):
        if not "max_participanti" in self.cleaned_data and not "min_participanti" in self.cleaned_data:
            raise ValidationError(u"Măcar un număr minim sau un număr maxim de participanți trebuie completat")
        elif self.cleaned_data.get("min_participanti", 0) >= self.cleaned_data.get("max_participanti", 10000):
            raise ValidationError(u"Minimul de participanți nu poate fi mai mare decât maximul")

        if "max_durata_string" in self.cleaned_data and "min_durata_string" in self.cleaned_data:
            if self.cleaned_data.get("min_durata_string") >= self.cleaned_data.get("max_durata_string"):
                self.errors["min_durata_string"] = ["Durata minimă trebuie să fie mai mică decât cea maximă", ]
                raise ValidationError(u"Durata minimă trebuie să fie mai mică decât cea maximă")

        return self.cleaned_data

    def clean_min_durata_string(self):
        return self._clean_time_string(self.cleaned_data.get("min_durata_string", ""))

    def clean_max_durata_string (self):
        return self._clean_time_string(self.cleaned_data.get("max_durata_string", ""))

    @staticmethod
    def _clean_time_string(value):
        return parse_string_to_seconds(value)


def parse_string_to_seconds(value, silent=False):
    string_order = {
        "s": 60 * 60 * 2400 * 7,
        "z": 60 * 60 * 2400,
        "h": 60 * 60,
        "m": 60,
    }

    regex = r"(\d+s){0,1} *(\d+z){0,1} *(\d+h){0,1} *(\d+m){0,1}"
    import re
    results = re.findall(regex, value, re.IGNORECASE)
    if len(results) == 0:
        if silent:
            return 0
        raise ValidationError("String invalid pentru timp. Foloseste s pentru saptamani, z pentru zile, h pentru ore, m pentru minute. 5 ore jumatate ar fi: 5h30m")

    seconds = 0
    for result in results[0]:
        result = result.strip()
        if not result:
            continue
        seconds += int(result[0:-1]) * string_order.get(result[-1], 0)

    return seconds


class DocumentActivitateForm(CrispyBaseModelForm):
    class Meta:
        model = Document
        fields = ("titlu", "descriere", "fisier")

    descriere = forms.CharField(required=False, label=u"Descriere", widget=Textarea)