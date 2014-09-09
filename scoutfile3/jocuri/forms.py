# coding: utf-8
from boto.beanstalk.exception import ValidationError
from goodies.forms import CrispyBaseModelForm
from jocuri.models import FisaActivitate

__author__ = 'andrei'


class FisaActivitateForm(CrispyBaseModelForm):
    class Meta:
        model = FisaActivitate
        fields = ("titlu", "descriere_joc", "materiale_necesare", "ramuri_de_varsta",
                    "min_participanti", "max_participanti", "min_durata", "max_durata",
                    "obiective_educative", "categorie", "sursa")

    def clean(self):
        if not "max_participanti" in self.cleaned_data and not "min_participanti" in self.cleaned_data:
            raise ValidationError(u"Măcar un număr minim sau un număr maxim de participanți trebuie completat")