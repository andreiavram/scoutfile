# coding: utf-8
from django.core.exceptions import ValidationError
from goodies.forms import CrispyBaseModelForm
from jocuri.models import FisaActivitate
from django import forms

__author__ = 'andrei'


class FisaActivitateForm(CrispyBaseModelForm):
    class Meta:
        model = FisaActivitate
        fields = ("titlu", "descriere_joc", "materiale_necesare", "ramuri_de_varsta",
                    "min_participanti", "max_participanti",
                    "obiective_educative", "categorie", "sursa")

    min_durata_string = forms.CharField(required=False, label=u"Durată minimă", help_text=u"Folosește expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m")
    max_durata_string = forms.CharField(required=False, label=u"Durată maximă", help_text=u"Folosește expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m")

    def clean(self):
        if not "max_participanti" in self.cleaned_data and not "min_participanti" in self.cleaned_data:
            raise ValidationError(u"Măcar un număr minim sau un număr maxim de participanți trebuie completat")
        elif self.cleaned_data.get("min_participanti") >= self.cleaned_data.get("max_participanti"):
            raise ValidationError(u"Minimul de participanți nu poate fi mai mare decât maximul")

        return self.cleaned_data

    def clean_min_durata_string(self):
        return self._clean_time_string(self.cleaned_data.get("min_durata", ""))

    def clean_max_durata_string (self):
        return self._clean_time_string(self.cleaned_data.get("max_durata", ""))

    def _clean_time_string(self, value):
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
            raise ValidationError("String invalid pentru timp. Foloseste s pentru saptamani, z pentru zile, h pentru ore, m pentru minute. 5 ore jumatate ar fi: 5h30m")

        seconds = 0
        for result in results[0]:
            result = result.strip()
            if not result:
                continue
            seconds += int(result[0:-1]) * string_order.get(results[-1])

        return seconds
