from certificari.models import Certificate
from goodies.forms import CrispyBaseModelForm
from django import forms

from goodies.widgets import BootstrapDateInput


class CertificateForm(CrispyBaseModelForm):
    class Meta:
        model = Certificate
        fields = ["certificate_type", "issued_on", "valid_until", "issued_by"]

    issued_on = forms.DateField(label="Emis la data", help_text="", widget=BootstrapDateInput)
    valid_until = forms.DateField(label="Data expirare", help_text="", widget=BootstrapDateInput, required=False)
