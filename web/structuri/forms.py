# coding: utf-8
'''
Created on Jun 9, 2012

@author: yeti
'''
from builtins import range
from builtins import object
import datetime

from ajax_select.fields import AutoCompleteSelectField
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from crispy_forms.layout import Fieldset, Layout, Submit, Field
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.forms.widgets import Textarea, PasswordInput
from goodies.forms import CrispyBaseModelForm, CrispyBaseForm,\
    CrispyBaseDeleteForm
from goodies.widgets import BootstrapDateInput

from album.models import AsociereEvenimentStructura
from structuri.fields import BetterROCNPField, NonAdminAutoCompleteSelectField
from structuri.models import Membru, CentruLocal, Unitate, Patrula,\
    AsociereMembruStructura, InformatieContact, TipInformatieContact,\
    AsociereMembruFamilie, PersoanaDeContact


class UnitateMembruCreateForm(CrispyBaseModelForm):
    class Meta(object):
        model = Membru
        exclude = ['timestamp_confirmed', "timestamp_registered", "timestamp_accepted", "requested_password_reset",
                   "hash", "user", "sex", "data_nasterii", "poza_profil", "centru_local", "familie", "scout_id", "scor_credit"]

    data_start_membru = forms.DateField(input_formats = ['%d.%m.%Y', ], widget = forms.DateInput(format = "%d.%m.%Y"), 
                                        label = u"Membru Centru Local din", 
                                        help_text = u"Data la care a început să fie membru în acest Centru Local. Alte apartenențe pot fi adăugate ulterior")
    data_start_unitate = forms.DateField(input_formats = ['%d.%m.%Y', ], widget = forms.DateInput(format = "%d.%m.%Y"),
                                         label = u"Membru în unitate din", 
                                         help_text = u"Data la care a intrat în unitate. Calitatea de membru în alte unități anterioare poate fi introdusă ulterior")
    
    cnp = BetterROCNPField(required = True, label = u"CNP")
    adresa = forms.CharField(widget = Textarea, required = True, label = u"Adresa poștală")    
    email = forms.EmailField(required = True, help_text = u"Acest email va deveni numele de utilizator al liderului, și va fi folosit pentru orice comunicare cu ScoutFile.")
    
#    parola = forms.CharField(widget = PasswordInput, label = u"Parolă", help_text = u"Cel puțin 6 caractere")
#    parola_verificare = forms.CharField(widget = PasswordInput, label  = u"Verificare")

    def __init__(self, *args, **kwargs):
        self.centru_local = kwargs.pop("centru_local")
        super(UnitateMembruCreateForm, self).__init__(*args, **kwargs)
        
        self.helper.layout = Layout(Fieldset(u"Date personale", "nume", "prenume", "cnp"),
                                    Fieldset(u"Informații de contact", "email", "telefon", "adresa"),
                                    Fieldset(u"Afilieri", 
                                             Field("data_start_membru", css_class = "datepicker", template = "fields/datepicker.html"), 
                                             Field("data_start_unitate", css_class = "datepicker", template = "fields/datepicker.html"), "lider_asistent"))


class UnitateLiderCreateForm(UnitateMembruCreateForm):
    lider_asistent = forms.BooleanField(label = u"Lider asistent", required = False)
    data_start_unitate = forms.DateField(input_formats = ['%d.%m.%Y', ], widget = forms.DateInput(format = "%d.%m.%Y"),
                                         label = u"Lider la unitate din", help_text = u"Data la care a început să fie lider la unitatea la care activează acum (alte unități pot fi adăugate ulteiror)")
    
    def __init__(self, *args, **kwargs):
        super(UnitateLiderCreateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(Fieldset(u"Date personale", "nume", "prenume", "cnp"),
                                    Fieldset(u"Informații de contact", "email", "telefon", "adresa"),
                                    Fieldset(u"Afilieri", 
                                             Field("data_start_membru", css_class = "datepicker", template = "fields/datepicker.html"), 
                                             Field("data_start_unitate", css_class = "datepicker", template = "fields/datepicker.html"), "lider_asistent"))
    

class MembruCreateForm(UnitateMembruCreateForm):
    unitate = forms.ModelChoiceField(Unitate.objects.all(), label = "Unitatea")
    
    def __init__(self, *args, **kwargs):
        super(MembruCreateForm, self).__init__(*args, **kwargs)

        self.fields['unitate'].queryset = Unitate.objects.filter(centru_local = self.centru_local)
        self.helper.layout = Layout(Fieldset(u"Date personale", "nume", "prenume", "cnp"),
                                    Fieldset(u"Informații de contact", "email", "telefon", "adresa"),
                                    Fieldset(u"Afilieri", "unitate", 
                                             Field("data_start_membru", css_class = "datepicker", template = "fields/datepicker.html"), 
                                             Field("data_start_unitate", css_class = "datepicker", template = "fields/datepicker.html")))

        
class LiderCreateForm(UnitateLiderCreateForm):
    unitate = forms.ModelChoiceField(Unitate.objects.all(), label = "Unitatea", required = False)
    
    def __init__(self, *args, **kwargs):    
        super(LiderCreateForm, self).__init__(*args, **kwargs)
        self.fields['data_start_unitate'].required = False
        self.fields['unitate'].queryset = Unitate.objects.filter(centru_local = self.centru_local)
        self.helper.layout = Layout(Fieldset(u"Date personale", "nume", "prenume", "cnp"),
                                    Fieldset(u"Informații de contact", "email", "telefon", "adresa"),
                                    Fieldset(u"Afilieri", 
                                             Field("data_start_membru", css_class = "datepicker", template = "fields/datepicker.html"),
                                             "unitate", 
                                             Field("data_start_unitate", css_class = "datepicker", template = "fields/datepicker.html"), "lider_asistent"))
        
        
class MembruUpdateForm(CrispyBaseModelForm):
    class Meta(object):
        model = Membru
        fields = ["nume", "prenume", "cnp", "email", "scout_id", "scor_credit"]

    email = forms.EmailField(label=u"Email", help_text=u"Schimbarea email-ului aici implicâ schimbarea utilizatorului!")
        
        
class CentruLocalCreateForm(CrispyBaseModelForm):
    class Meta(object):
        model = CentruLocal
        exclude = ["nume", "statut_drepturi", "statut_juridic", "logo", "antet", "moment_initial_cotizatie"]
        
    data_infiintare = forms.DateField(widget=BootstrapDateInput, label = u"Data înființare", required = False)
        
    def __init__(self, *args, **kwargs):
        super(CentruLocalCreateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(Field("localitate"), Field("denumire"), 
                                    Field("data_infiintare"), Field("specific"),
                                    Field("preferinte_corespondenta"))
        
class CentruLocalAdminCreateForm(CentruLocalCreateForm):
    class Meta(object):
        model = CentruLocal
        exclude = ["nume", "statut_drepturi", "logo", "antet", "moment_initial_cotizatie"]
            
    def __init__(self, *args, **kwargs):
        super(CentruLocalAdminCreateForm, self).__init__(*args, **kwargs)
        #self.helper.layout = Layout(Field("localitate"), Field("denumire"),
        #                            Field("data_infiintare"),
        #                            Field("specific"), Field("statut_juridic"), Field("preferinte_corespondenta"),
        #                            Field("moment_initial_cotizatie"))



class CentruLocalAdminUpdateForm(CrispyBaseModelForm):
    class Meta(object):
        model = CentruLocal
        exclude = ["nume", "moment_initial_cotizatie", "statut_drepturi"]

    data_infiintare = forms.DateField(widget=BootstrapDateInput, label = u"Data înființare", required = False)

    #def __init__(self, *args, **kwargs):
    #    super(CentruLocalAdminUpdateForm, self).__init__(*args, **kwargs)


class CentruLocalUpdateForm(CentruLocalAdminUpdateForm):
    class Meta(object):
        model = CentruLocal
        exclude = ["nume", "statut_drepturi", "statut_juridic", "moment_initial_cotizatie"]


class UnitateCreateForm(CrispyBaseModelForm):
    class Meta(object):
        model = Unitate
        exclude = []
        
    data_infiintare = forms.DateField(widget=BootstrapDateInput, label=u"Data înființare", required=False)

    def __init__(self, *args, **kwargs):
        super(UnitateCreateForm, self).__init__(*args, **kwargs)

class CentruLocalUnitateCreateForm(UnitateCreateForm):
    class Meta(object):
        model = Unitate
        exclude = ["centru_local", ]
        
        
class UnitateUpdateForm(UnitateCreateForm):
    class Meta(object):
        model = Unitate
        exclude = ["centru_local", ]
        

class PatrulaCreateForm(CrispyBaseModelForm):
    class Meta(object):
        model = Patrula
        exclude = ("unitate", )
        
    data_infiintare = forms.DateField(widget=BootstrapDateInput, label=u"Data înființare", required=False)


class PatrulaUpdateForm(PatrulaCreateForm):
    class Meta(object):
        model = Patrula
        exclude = ("unitate", )

    moment_inchidere = forms.DateField(widget=BootstrapDateInput, required=False, label=u"Dată la desființare", help_text=u"Dacă patrula nu mai este activă, trece aici data la care s-a închis")


class MembruRegistrationForm(CrispyBaseModelForm):
    class Meta(object):
        model = Membru
        fields = ("nume", "prenume", "cnp", "email", "telefon", "adresa")
        
    centrul_local = forms.ModelChoiceField(CentruLocal.objects.all(), label = u"Centrul Local")
    unitate = forms.ModelChoiceField(Unitate.objects.all(), label = "Unitatea")
    adeziune = forms.BooleanField(label = "Am completat adeziune la înscriere", required = False)
    
    cnp = BetterROCNPField(required = True, label = u"CNP", help_text = u"CNP-ul tău va fi folosit doar în scopuri interne ale ONCR (spre exemplu, pentru a-ți determina data nașterii, sexul, dar și pentru diferite liste necesare pentru campuri). Nu vom furniza niciodată CNP-ul tău altcuiva.")
    adresa = forms.CharField(widget = Textarea, required = True, label = u"Adresa poștală")
    email = forms.EmailField(required = True, help_text = u"Acest email va deveni numele tău de utilizator, și va fi folosit pentru orice comunicare cu ScoutFile.")
    
    parola = forms.CharField(widget = PasswordInput, label = u"Parolă", help_text = u"Cel puțin 6 caractere")
    parola_verificare = forms.CharField(widget = PasswordInput, label  = u"Verificare")
    
    def __init__(self, *args, **kwargs):
        retval = super(MembruRegistrationForm, self).__init__(*args, **kwargs)
        
        self.helper.layout = Layout(Fieldset(u"Date personale", "nume", "prenume", "cnp"),
                                    Fieldset(u"Informații de contact", "email", "telefon", "adresa"),
                                    Fieldset(u"Apartenență la ONCR", "centrul_local", "unitate", "adeziune"),
                                    Fieldset(u"Cont", "parola", "parola_verificare"))
        
        return retval
    
    def clean_parola(self):
        if "parola" not in self.cleaned_data:
            raise ValidationError(u"Specificarea unei parole este obligatorie pentru înregistrare")
        parola = self.cleaned_data['parola']
        if len(parola) < 6:
            raise ValidationError(u"Parola este prea scurtă. Introduceți o parolă de cel puțin 6 caractere")
        
        return parola
    
    def clean(self):
        if "parola" in self.cleaned_data:
            parola = self.cleaned_data['parola']            
            if "parola_verificare" not in self.cleaned_data:
                self._errors['parola_verificare'] = (u"Introduceți parola din nou, pentru verificare.", )
            else:
                if self.cleaned_data['parola_verificare']  != self.cleaned_data['parola']:
                    self._errors['parola'] = u"Parolele introduse nu coincid"
                    self._errors['parola_verificare'] = u"Parolele introduse nu coincid"
                    
                    del self.cleaned_data['parola']
                    del self.cleaned_data['parola_verificare']
                
        
        return self.cleaned_data
    
class ConfirmMembruAdminForm(CrispyBaseModelForm):
    class Meta(object):
        model = Membru
        fields = ()
    
    button_label = u"Confirmă"
    
    
    def __init__(self, *args, **kwargs):
        retval = super(ConfirmMembruAdminForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit("reject", u"Respinge", css_class = "btn btn-danger", css_id = "id_respinge"))
        return retval


class ForgotPasswordForm(CrispyBaseForm):
    button_label = u"Trimite"
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    
class ChangePasswordForm(CrispyBaseForm):
    parola_veche = forms.CharField(widget = PasswordInput, required = True)
    parola = forms.CharField(widget = PasswordInput, required = True)
    parola_verificare = forms.CharField(widget = PasswordInput, required = True)
    
    def clean_parola_veche(self):
        if "parola_veche" not in self.cleaned_data:
            raise ValidationError(u"Trebuie să introduci și parola curentă")
        parola_veche = self.cleaned_data['parola_veche']
        if not self.request.user.check_password(parola_veche):
            raise ValidationError(u"Parola curentă este greșită")

        return parola_veche
    
    def clean_parola(self):
        if "parola" not in self.cleaned_data:
            raise ValidationError(u"Specificarea unei parole este obligatorie pentru înregistrare")
        parola = self.cleaned_data['parola']
        if len(parola) < 6:
            raise ValidationError(u"Parola este prea scurtă. Introduceți o parolă de cel puțin 6 caractere")
        
        return parola
    
    def clean(self):
        if "parola" in self.cleaned_data:
            parola = self.cleaned_data['parola']
            if "parola_veche" in self.cleaned_data:
                if self.cleaned_data['parola'] == self.cleaned_data['parola_veche']:
                    raise ValidationError(u"Parola nouă nu poate fi identică cu parola veche")
                            
            if "parola_verificare" not in self.cleaned_data:
                self._errors['parola_verificare'] = (u"Introduceți parola din nou, pentru verificare.", )
            else:
                
                if self.cleaned_data['parola_verificare']  != self.cleaned_data['parola']:
                    self._errors['parola'] = u"Parolele introduse nu coincid"
                    self._errors['parola_verificare'] = u"Parolele introduse nu coincid"
                    
                    del self.cleaned_data['parola']
                    del self.cleaned_data['parola_verificare']
                
        return self.cleaned_data
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        return super(ChangePasswordForm, self).__init__(*args, **kwargs)


class UtilizatorProfileForm(CrispyBaseModelForm):
    class Meta(object):
        model = Membru
        fields = ("email", "nume", "prenume", "cnp")
        
    # adresa = forms.CharField(widget = Textarea, required = True, label = u"Adresa poștală")
    cnp = BetterROCNPField(label = u"CNP", required = True)
    
    def __init__(self, *args, **kwargs):
        super(UtilizatorProfileForm, self).__init__(*args, **kwargs)
        # self.fields['email'].widget.attrs['readonly'] = True
        self.fields['cnp'].widget.attrs['readonly'] = True
        
class UtilizatorProfilePictureForm(CrispyBaseModelForm):
    class Meta(object):
        model = Membru
        fields = ()
        
    has_cancel = True 
        
    poza_profil = forms.ImageField(required = True, label = u"Noua poză de profil",
                                   help_text = u"Poza de profil va fi folosită peste tot în relație cu contul tău ScoutFile, inclusiv pe cardul de membru la cercetași")
    
    
class AsociereCreateForm(CrispyBaseModelForm):
    class Meta(object):
        model = AsociereMembruStructura
        fields = ("content_type", "object_id", "tip_asociere", "moment_inceput", "moment_incheiere")
    
    object_id = forms.IntegerField(widget = forms.Select(choices = ()), label = u"Structură")
    moment_inceput = forms.DateField(input_formats = ['%d.%m.%Y', ], widget = forms.DateInput(format = "%d.%m.%Y"))
    moment_incheiere = forms.DateField(input_formats = ['%d.%m.%Y', ], widget = forms.DateInput(format = "%d.%m.%Y"), required = False)
    
    def __init__(self, *args, **kwargs):
        super(AsociereCreateForm, self).__init__(*args, **kwargs)
        
        content_type_filter = dict(app_label="structuri", model__in=("centrulocal", "unitate", "patrula"))
        self.fields['content_type'].queryset = ContentType.objects.filter(**content_type_filter)
        
        self.helper.layout = Layout(Field("content_type"), Field("object_id"), Field("tip_asociere"),
                                    Field("moment_inceput", css_class="datepicker", template="fields/datepicker.html"),
                                    Field("moment_incheiere", css_class="datepicker", template="fields/datepicker.html"))
        

class AsociereUpdateForm(AsociereCreateForm):
    pass


class AsociereEvenimentStructuraForm(CrispyBaseModelForm):
    class Meta(object):
        model = AsociereEvenimentStructura
        fields = ("content_type", "object_id")

    object_id = forms.IntegerField(widget = forms.Select(choices = ()), label = u"Structură")

    def __init__(self, *args, **kwargs):
        super(AsociereEvenimentStructuraForm, self).__init__(*args, **kwargs)

        content_type_filter = dict(app_label="structuri", model__in=("centrulocal", "unitate", "patrula"))
        self.fields['content_type'].queryset = ContentType.objects.filter(**content_type_filter)


class InformatieGenericCreateForm(CrispyBaseModelForm):
    tip_informatie_categorie = "Contact" #  default value

    class Meta(object):
        model = InformatieContact
        fields = ["tip_informatie", "valoare", "informatii_suplimentare"]

    informatii_suplimentare = forms.CharField(widget = Textarea, required = False, label = u"Informații adiționale", help_text = u"Folosiți acest câmp dacă este nevoie să explicați informația din câmpul de mai sus (spre exemplu, a cui este adresa de corespondență)")

    def __init__(self, *args, **kwargs):
        filter_by = kwargs.pop("filter_by", None)
        filter_categorie_by = kwargs.pop("filter_categorie_by", None)

        super(InformatieGenericCreateForm, self).__init__(*args, **kwargs)

        if filter_by:
            qs = TipInformatieContact.objects.filter(Q(relevanta__isnull=True) | Q(relevanta__icontains=filter_by))
            qs = qs.filter(categorie__exact=filter_categorie_by)
            self.fields['tip_informatie'].queryset = qs


class InformatieGenericDeleteForm(CrispyBaseDeleteForm):
    class Meta(object):
        model = InformatieContact
        exclude = []

    has_cancel = True


# class InformatieContactCreateForm(InformatieGenericForm):
#     tip_informatie_categorie = "Contact"
#
#
# class InformatieContactUpdateForm(InformatieContactCreateForm):
#     pass
#
#
# class InformatieContactDeleteForm(InformatieGenericDeleteForm):
#     pass
#
#
# class InformatieAlteleCreateForm(InformatieGenericForm):
#     tip_informatie_categorie = "Altele"
#
#
# class InformatieAlteleUpdateForm(InformatieAlteleCreateForm):
#     pass
#
#
# class InformatieAlteleDeleteForm(InformatieGenericDeleteForm):
#     pass


class AsociereMembruFamilieForm(CrispyBaseModelForm):
    class Meta(object):
        model = AsociereMembruFamilie
        fields = ["persoana_destinatie", "tip_relatie"]
    
    persoana_destinatie = NonAdminAutoCompleteSelectField("membri", required = True, help_text = u"Introduceți câteva litere pentru a căuta un membru",
                                            label = u"Persoana")
    
class PersoanaDeContactForm(CrispyBaseModelForm):
    class Meta(object):
        model = PersoanaDeContact
        fields = ["nume", "tip_relatie", "telefon", "email", "job", "note", "implicit"]

    note = forms.CharField(widget = Textarea, required = False)

    def clean(self):
        some_data = False
        fields = ["nume", "tip_relatie", "telefon", "email", "job", "note"]
        for field in fields:
            if field in self.cleaned_data and self.cleaned_data[field]:
                some_data = True
        
        if not some_data:
            raise ValidationError(u"Trebuie completat măcar un câmp!")
        
        return self.cleaned_data
    
class SetariSpecialeCentruLocalForm(CrispyBaseModelForm):
    class Meta(object):
        model = CentruLocal
        fields = []

    trimestru = forms.ChoiceField(choices=(("1", "I"), ("2", "II"), ("3", "III"), ("4", "IV")))
    an = forms.ChoiceField(label="An", choices=((an, an) for an in range(1 + int(datetime.date.today().strftime("%Y")), 2010, -1)))

    def __init__(self, *args, **kwargs):
        super(SetariSpecialeCentruLocalForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(Fieldset(u"Trimestru inițial pentru cotizație în sistem", "trimestru", "an"),)


class PatrulaMembruAsociazaForm(CrispyBaseModelForm):
    class Meta(object):
        model = AsociereMembruStructura
        fields = ['membru']

    membru = NonAdminAutoCompleteSelectField("membri", label=u"Cercetaș")
    asociere_inceput = forms.DateField(widget=BootstrapDateInput, label=u"Moment început")

    def __init__(self, *args, **kwargs):
        self.patrula = kwargs.pop("patrula")
        super(PatrulaMembruAsociazaForm, self).__init__(*args, **kwargs)

        # self.fields['membru'].queryset = Membru.objects.filter(id__in = [m.id for m in self.patrula.unitate.cercetasi()])
