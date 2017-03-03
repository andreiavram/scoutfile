# coding: utf-8
from crispy_forms.layout import Layout, Field, Div
from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput, Textarea
from django_markdown.widgets import MarkdownWidget
from goodies.forms import CrispyBaseModelForm
from goodies.widgets import TaggitTagsInput
from taggit.forms import TagField

from documente import Document
from jocuri import FisaActivitate
from structuri import RamuraDeVarsta

__author__ = 'andrei'

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

class FisaActivitateForm(CrispyBaseModelForm):
    class Meta:
        model = FisaActivitate
        fields = ("titlu", "descriere", "descriere_joc", "materiale_necesare", "ramuri_de_varsta",
                    "min_participanti", "max_participanti",
                    "obiective_educative", "categorie", "sursa", "tags", "is_draft")

    titlu = forms.CharField(required=True, label=u"Titlu", widget=TextInput(attrs={"style": "width: 100%; font-size: 24px; line-height: 28px; padding: 10px 5px"}))
    min_durata_string = forms.CharField(required=False, label=u"Durată minimă", help_text=u"Folosește expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m")
    max_durata_string = forms.CharField(required=False, label=u"Durată maximă", help_text=u"Folosește expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m")
    descriere_joc = forms.CharField(required=True, label=u"Conținut", help_text=u"Format Markdown, descrierea jocului, ce trebuie pregătit, ce trebuie făcut, care este obiectivul, care sunt regulile ...", widget=MarkdownWidget())
    descriere = forms.CharField(required=False, label=u"Descriere pe scurt", help_text=u"Un text de descriere pentru căutare", widget=Textarea(attrs={"style": "width: 100%; height: 80px"}))
    ramuri_de_varsta = forms.ModelMultipleChoiceField(RamuraDeVarsta.objects.all(), required=True, label=u"Ramuri de vârstă", help_text=u"Alegeți mărcar una", widget=forms.CheckboxSelectMultiple)
    tags = TagField(required=False, widget=TaggitTagsInput(attrs={"style": "width: 100%"}), label=u"Tag-uri")
    materiale_necesare = forms.CharField(required=False, label=u"Materiale necesare", help_text=u"Câte unul pe linie, fără numerotare adițională", widget=Textarea(attrs={"style": "width: 100%; height: 80px"}))
    obiective_educative = forms.CharField(required=False, label=u"Obiective educative", help_text=u"Câte unul pe linie, fără numerotare (se va face automat)", widget=Textarea(attrs={"style": "width: 100%; height: 80px"}))


    def __init__(self, **kwargs):
        super(FisaActivitateForm, self).__init__(**kwargs)
        self.helper.form_class = "scoutfile-form"
        self.helper.layout = Layout(Field("titlu", css_class="input-xlarge"), Field("descriere"), Field("descriere_joc"),
                                    Field("obiective_educative"), Field("materiale_necesare"),
                                    Div(
                                        Div(Field("min_durata_string"), Field("max_durata_string"), Field("sursa"), css_class="span4"),
                                        Div(Field("categorie"), Field("min_participanti"), Field("max_participanti"), Field("is_draft"),  css_class="span4"),
                                        Div( Field("ramuri_de_varsta"), Field("tags"), css_class="span4"),
                                        css_class="row-fluid"),
                                    )

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


class DocumentActivitateForm(CrispyBaseModelForm):
    class Meta:
        model = Document
        fields = ("titlu", "descriere", "fisier")

    descriere = forms.CharField(required=False, label=u"Descriere", widget=Textarea)
    fisier = forms.FileField(required=True, label=u"Fișier", help_text=u"Alege un fișier local pentru upload")