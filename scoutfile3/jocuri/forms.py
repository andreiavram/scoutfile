from goodies.forms import CrispyBaseModelForm
from jocuri.models import FisaActivitate

__author__ = 'andrei'


class FisaActivitateForm(CrispyBaseModelForm):
    class Meta:
        model = FisaActivitate
        fields = ("titlu", "descriere_joc", "materiale_necesare", "ramuri_de_varsta",
                    "min_participanti", "max_participanti", "min_durata", "max_durata",
                    "obiective_educative", "categorie", "sursa")