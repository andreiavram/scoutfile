# coding: utf-8
'''
Created on Nov 8, 2012

@author: yeti
'''
from documente.models import DocumentCotizatieSociala
from generic.widgets import BootstrapDateTimeInput, BootstrapDateInput
from generic.forms import CrispyBaseModelForm
from documente.models import Document, ChitantaCotizatie
from crispy_forms.layout import Field, Layout, Submit, Button
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton
from django.forms.fields import DateField
from django.forms.widgets import DateInput
import datetime

class DocumentCreateForm(CrispyBaseModelForm):
    class Meta:
        model = Document
        exclude = ("version_number", "root_document", "folder", "locked", "is_folder", "uploader")
        
class FolderCreateForm(CrispyBaseModelForm):
    class Meta:
        model = Document
        fields = ("titlu", )

class CotizatieMembruForm(CrispyBaseModelForm):
    class Meta:
        model = ChitantaCotizatie
        exclude = ("version_number", "titlu", "descriere", "fisier", "url",
                   "root_document", "folder", "locked", "is_folder", "fragment",
                   "uploader", "tip_document", "casier")
        

    data_inregistrare = DateField(input_formats = ['%d.%m.%Y', ], widget = DateInput(format = "%d.%m.%Y"),
                                         label = u"Data",
                                         initial = datetime.datetime.now().strftime("%d.%m.%Y"))
    
    def __init__(self, *args, **kwargs):
        super(CotizatieMembruForm, self).__init__(*args, **kwargs)
    
        self.helper.layout = Layout(Field('numar'),
                                    FieldWithButtons('serie', StrictButton(u"Obține număr și serie")),
                                    Field("data_inregistrare", css_class = "datepicker", template = "fields/datepicker.html"),
                                    Field("suma"))

        
        self.helper.add_input(Button('cancel', u"Renunță", css_class = "btn-danger"))
        
        
class DeclaratieCotizatieSocialaForm(CrispyBaseModelForm):
    class Meta:
        model = DocumentCotizatieSociala
        fields = ['nume_parinte', 'motiv', 'este_valabil', 'fisier', 'numar_inregistrare', 'data_inregistrare']

    data_inregistrare = DateField(widget=BootstrapDateInput, label=u"Data înregistrare")