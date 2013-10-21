# coding: utf-8
'''
Created on Nov 8, 2012

@author: yeti
'''
from django.core.exceptions import ValidationError
from django.db.models.aggregates import Max
#from django.db.models.fields import CharField
from django.db.models.query_utils import Q
from documente.models import DocumentCotizatieSociala, Registru, DecizieCotizatie, Trimestru, PlataCotizatieTrimestru
from generic.widgets import BootstrapDateInput
from generic.forms import CrispyBaseModelForm, CrispyBaseForm
from documente.models import Document, ChitantaCotizatie
from crispy_forms.layout import Field, Layout, Submit, Button
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton
from django.forms.fields import DateField, CharField
from django.forms.widgets import HiddenInput
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
        fields = ["fisier", "registru", "numar_inregistrare", "suma"]

    def __init__(self, *args, **kwargs):
        self.centru_local = kwargs.pop("centru_local", None)
        self.membru = kwargs.pop("membru", None)
        super(CotizatieMembruForm, self).__init__(*args, **kwargs)
        self.fields['registru'].queryset = Registru.objects.filter(valabil = True,
                                                          tip_registru__in = ChitantaCotizatie.registre_compatibile,
                                                          centru_local = self.centru_local)

    def clean_suma(self):
        plati, suma, status, diff = PlataCotizatieTrimestru.calculeaza_acoperire(membru=self.membru,
                                       suma=self.cleaned_data['suma'],
                                       commit=False)
        if diff < -4:
            raise ValidationError(u"Nu se pot înregistra plăți în avans pentru mai mult de 4 trimestre!")
        return self.cleaned_data['suma']

    def clean(self):
        registru = self.cleaned_data['registru']
        if registru.mod_functionare == "auto":
            if "numar_inregistrare" in self.cleaned_data:
                try:
                    self.cleaned_data['numar_inregistrare'] = registru.get_numar_inregistrare()
                except ValueError, e:
                    raise ValidationError(u"Nu s-a putut obține număr de înregistrare pentru decizie ({0})".format(e))
        else:
            if registru.get_document(self.cleaned_data['numar_inregistrare']):
                raise ValidationError(u"Există deja un document cu acest număr de înregistrare în registrul selectat!")

        return self.cleaned_data
        
class DeclaratieCotizatieSocialaForm(CrispyBaseModelForm):
    class Meta:
        model = DocumentCotizatieSociala
        fields = ['nume_parinte', 'motiv', 'este_valabil', 'fisier', 'numar_inregistrare', 'data_inregistrare']

    data_inregistrare = DateField(widget=BootstrapDateInput, label=u"Data înregistrare")

class RegistruForm(CrispyBaseModelForm):
    def get_intervale(self):
        return Registru.objects.filter(**self.get_search_kwargs())

    def get_search_kwargs(self):
        return {"tip_registru" : self.cleaned_data['tip_registru'],
                 "serie" : self.cleaned_data['serie'],
                 "centru_local" : self.centru_local,}


    def clean(self):
        are_numar_sfarsit = "numar_sfarsit" in self.cleaned_data and self.cleaned_data['numar_sfarsit']
        if are_numar_sfarsit and self.cleaned_data['numar_sfarsit'] <= self.cleaned_data['numar_inceput']:
            raise ValidationError(u"Numărul de sfârșit poate să fie mai mare decât numărul de început")

        intervale = self.get_intervale()
        interval_deschis = intervale.filter(numar_sfarsit__isnull = True)

        if are_numar_sfarsit:
            #   daca exista deja registre cu interval deschis
            if interval_deschis.count() and self.cleaned_data["numar_sfarsit"] >= interval_deschis[0].numar_inceput:
                raise ValidationError(u"Suprapunere de numere cu registrul #%d" % interval_deschis[0].id)

            range_kwargs = {"numar_inceput__range" : (self.cleaned_data['numar_inceput'], self.cleaned_data['numar_sfarsit']),
                            "numar_sfarsit__range" : (self.cleaned_data['numar_inceput'], self.cleaned_data['numar_sfarsit'])}
            intervale_suprapuse = intervale.filter(**range_kwargs)
            if intervale_suprapuse.count():
                raise ValidationError(u"Suprapunere de numere cu %d alte registre, te rog să reverifici" % intervale_suprapuse.count())
        else:
            if interval_deschis.count():
                raise ValidationError(u"Nu se pot defini două registre cu numerotare deschisă (fără număr sfârșit) pe aceeași serie")
            else:
                if intervale.count():
                    if self.cleaned_data['numar_inceput'] <= intervale.aggregate(Max("numar_sfarsit")).get("numar_sfarsit__max"):
                        raise ValidationError(u"Suprapunere de numerotare cu un registru!")

        return self.cleaned_data

class RegistruCreateForm(RegistruForm):
    class Meta:
        model = Registru
        exclude = ["centru_local", "owner", "document_referinta", "numar_curent", "valabil", "editabil"]

    def __init__(self, *args, **kwargs):
        self.centru_local = kwargs.pop("centru_local", None)
        return super(RegistruCreateForm, self).__init__(*args, **kwargs)


class RegistruUpdateForm(RegistruForm):
    class Meta:
        model = Registru
        exclude = ["centru_local", "owner", "document_referinta", "numar_curent", "numar_inceput", "editabil"]

    def get_intervale(self):
        qs = super(RegistruUpdateForm, self).get_intervale()
        qs = qs.exclude(id = self.instance.id)
        return qs

    def clean_numar_sfarsit(self):
        numar_sfarsit = self.cleaned_data['numar_sfarsit']
        if self.instance:
            if self.instance.numar_curent > numar_sfarsit:
                raise ValidationError(u"Nu se pot da numere de sfârșit mai mici decât cel mai mare număr deja înregistrat")
        return numar_sfarsit


class DecizieCuantumCotizatieForm(CrispyBaseModelForm):
    class Meta:
        model = DecizieCotizatie
        fields = ["registru", "numar_inregistrare", "categorie", "cuantum", "data_inceput", "continut"]

    data_inceput = DateField(widget=BootstrapDateInput, label = u"Data început")

    def __init__(self, *args, **kwargs):
        self.centru_local = kwargs.pop("centru_local", None)
        super(DecizieCuantumCotizatieForm, self).__init__(*args, **kwargs)
        registru_filter = {"valabil" : True,
                           "centru_local" : self.centru_local,
                           "tip_registru__in" : DecizieCotizatie.registre_compatibile}
        self.fields['registru'].queryset = Registru.objects.filter(**registru_filter).order_by("-data_inceput")
        self.fields['registru'].required = True

    def clean(self):
        registru = self.cleaned_data['registru']

        decizie_filter = {"centru_local" : self.centru_local,
                          "categorie" : self.cleaned_data['categorie']}

        if "data_inceput" in self.cleaned_data:
            decizii_existente = DecizieCotizatie.objects.filter(**decizie_filter).filter(
                Q(data_sfarsit__isnull = True, data_inceput__gte = self.cleaned_data['data_inceput']) | Q(data_sfarsit__isnull = False, data_sfarsit__gte = self.cleaned_data['data_inceput']))
            if decizii_existente.count():
                raise ValidationError(u"Decizia contravine unei decizii anterioare ({0})")


            if registru.mod_functionare == "auto":
                if "numar_inregistrare" in self.cleaned_data:
                    try:
                        self.cleaned_data['numar_inregistrare'] = registru.get_numar_inregistrare()
                    except ValueError, e:
                        raise ValidationError(u"Nu s-a putut obține număr de înregistrare pentru decizie ({0})".format(e))
            else:
                if registru.get_document(self.cleaned_data['numar_inregistrare']):
                    raise ValidationError(u"Există deja un document cu acest număr de înregistrare în registrul selectat!")

        return self.cleaned_data

class TransferIncasariForm(CrispyBaseForm):
    plati = CharField(widget=HiddenInput)

    #from structuri.models import Membru
    #lider = ModelChoiceField(queryset=Membru.objects.all())

    def __init__(self, *args, **kwargs):
        self.centru_local = kwargs.pop("centru_local", None)
        super(TransferIncasariForm, self).__init__(*args, **kwargs)
        #self.fields['lider'].queryset = self.centru_local.cercetasi(tip_asociere=u"Lider")

    def clean_plati(self):
        plati = ChitantaCotizatie.objects.filter(id__in=self.cleaned_data['plati'].split("|"))
        return plati


