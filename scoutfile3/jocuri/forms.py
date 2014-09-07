from goodies.forms import CrispyBaseModelForm
from jocuri.models import FisaActivitate

__author__ = 'andrei'


class FisaActivitateForm(CrispyBaseModelForm):
    class Meta:
        model = FisaActivitate