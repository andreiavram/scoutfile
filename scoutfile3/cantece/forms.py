from goodies.forms import CrispyBaseModelForm
from cantece.models import Cantec, CarteCantece

__author__ = 'andrei'


class CantecForm(CrispyBaseModelForm):
    class Meta:
        model = Cantec


class CarteCanteceForm(CrispyBaseModelForm):
    class Meta:
        model = CarteCantece