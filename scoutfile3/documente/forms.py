# coding: utf-8
'''
Created on Nov 8, 2012

@author: yeti
'''
from scoutfile3.generic.forms import CrispyBaseModelForm
from scoutfile3.documente.models import Document, ChitantaCotizatie
from crispy_forms.layout import Field, Layout, Submit, Button
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton
from django.forms.fields import DateField
from django.forms.widgets import DateInput
import datetime
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt


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
        
        
