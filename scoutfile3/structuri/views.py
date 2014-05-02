#coding: utf-8
from django.conf.global_settings import SERVER_EMAIL
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView
from goodies.views import TabbedViewMixin, GenericDeleteView
import datetime
import hashlib
import logging
import traceback
from unidecode import unidecode
from album.models import ParticipareEveniment

from documente.models import Trimestru, ChitantaCotizatie, PlataCotizatieTrimestru
from settings import SECRET_KEY, SYSTEM_EMAIL, MEDIA_ROOT, DEBUG, \
    USE_EMAIL_CONFIRMATION
from structuri.decorators import allow_by_afiliere
from structuri.forms import MembruCreateForm, MembruUpdateForm, \
    CentruLocalUpdateForm, UnitateUpdateForm, PatrulaCreateForm, PatrulaUpdateForm, \
    CentruLocalUnitateCreateForm, MembruRegistrationForm, ConfirmMembruAdminForm, \
    ForgotPasswordForm, ChangePasswordForm, UtilizatorProfileForm, \
    UtilizatorProfilePictureForm, LiderCreateForm, UnitateMembruCreateForm, \
    UnitateLiderCreateForm, AsociereCreateForm, AsociereUpdateForm, \
    CentruLocalAdminCreateForm, CentruLocalAdminUpdateForm, \
    InformatieContactCreateForm, InformatieContactUpdateForm, \
    InformatieContactDeleteForm, AsociereMembruFamilieForm, PersoanaDeContactForm, SetariSpecialeCentruLocalForm, \
    PatrulaMembruAsociazaForm
from structuri.models import CentruLocal, AsociereMembruStructura, \
    Membru, Unitate, Patrula, TipAsociereMembruStructura, Utilizator, ImagineProfil, \
    InformatieContact, TipInformatieContact, AsociereMembruFamilie, \
    PersoanaDeContact
from utils.views import FacebookUserConnectView


logger = logging.getLogger(__name__)


#    definitii ctypes
ctype_centrulocal = ContentType.objects.get_for_model(CentruLocal)


class CentruLocalCreate(CreateView):
    model = CentruLocal
    form_class = CentruLocalAdminCreateForm

    @method_decorator(user_passes_test(lambda user: user.groups.filter(name__icontains=u"administrator").count()))
    def dispatch(self, *args, **kwargs):
        return super(CentruLocalCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if self.object.statut_juridic == "gi":
            self.object.statut_drepturi = "gi"

        self.object.save()

        messages.success(self.request,
                         u"Centrul Local a fost adăugat cu succes. Nu uita să adaugi și echipa de conducere!")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:cl_detail", kwargs={"pk": self.object.id})


class CentruLocalUpdate(UpdateView):
    model = CentruLocal

    @allow_by_afiliere([("Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, *args, **kwargs):
        return super(CentruLocalUpdate, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        if self.request.user.is_staff:
            return CentruLocalAdminUpdateForm
        return CentruLocalUpdateForm


class CentruLocalDetail(DetailView, TabbedViewMixin):
    model = CentruLocal

    @allow_by_afiliere([("Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(CentruLocalDetail, self).dispatch(request, *args, **kwargs)

    def get_tabs(self, *args, **kwargs):
        self.tabs = (("brief", u"Sumar", reverse("structuri:cl_tab_brief", kwargs={"pk": self.object.id}), "", 2),
                     ("unitati", u"Unități", reverse("structuri:cl_tab_unitati", kwargs={"pk": self.object.id}), "icon-group", 3),
                     ("contact", u"Contact", reverse("structuri:cl_tab_contact", kwargs={"pk": self.object.id}), "icon-envelope", 1),
                     ("lideri", u"Lideri", reverse("structuri:cl_tab_lideri", kwargs = {"pk" : self.object.id }), "icon-user", 4),
                     ("membri_de_suspendat", u"Membri de suspendat", reverse("structuri:cl_tab_membri_de_suspendat", kwargs = {"pk" : self.object.id }), "icon-remove", 5))
        return super(CentruLocalDetail, self).get_tabs(*args, **kwargs)

    def get_context_menu(self, *args, **kwargs):
        menu_items = {u"Acțiuni": ((reverse("structuri:cl_edit", kwargs={"pk": self.object.id}), "icon-pencil"),
                                   (reverse("structuri:cl_delete", kwargs={"pk": self.object.id}), "icon-trash")),
                      u"Locații": ((reverse("structuri:cl_list"), "icon-list"),),
                      #                     u"Documente" : ((reverse("structuri:cl_cotizatii", kwargs = {"pk" : self.object.id}), "icon-file"),
                      #                                     (reverse("structuri:cl_serii", kwargs = {"pk" : self.object.id }), "icon-file"),
                      #                                     (reverse("structuri:cl_altele", kwargs = {"pk" : self.object.id }), "icon-file"),
                      #                                       )
        }

        return menu_items

    def get_context_data(self, **kwargs):
        current = super(CentruLocalDetail, self).get_context_data(**kwargs)
        current.update(self.get_tabs())
        current.update({"context_menu": self.get_context_menu()})

        return current


class CentruLocalList(ListView):
    model = CentruLocal
    template_name = "structuri/centrulocal_list.html"

    @method_decorator(user_passes_test(lambda user: user.groups.filter(name__icontains=u"administrator").count()))
    def dispatch(self, *args, **kwargs):
        return super(CentruLocalList, self).dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name__iexact=u"Administratori sistem").count() == 0:
            return self.request.user.get_profile().membru.get_centre_locale_permise()
        return super(CentruLocalList, self).get_queryset(*args, **kwargs)


class CentruLocalDelete(GenericDeleteView):
    model = CentruLocal

    @method_decorator(user_passes_test(lambda user: user.groups.filter(name__icontains=u"administrator").count()))
    def dispatch(self, *args, **kwargs):
        return super(CentruLocalDelete, self).dispatch(*args, **kwargs)

    def success_url(self):
        return reverse("structuri:cl_list")


class CentruLocalLiderCreate(CreateView):
    model = Membru
    form_class = LiderCreateForm
    doar_lideri = True

    @allow_by_afiliere([("Centru Local", u"Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, "centru_local") or self.centru_local == None:
            self.centru_local = get_object_or_404(CentruLocal, id=kwargs.pop("pk"))
        return super(CentruLocalLiderCreate, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        current = super(CentruLocalLiderCreate, self).get_form_kwargs()
        current.update({"centru_local": self.get_centru_local()})
        return current

    def get_pozitie(self, *args, **kwargs):
        try:
            form = kwargs.get("form")
        except Exception, e:
            logger.error("%s: %s, %s" % (self.__class__.__name__, e, traceback.format_exc()))
            raise e

        pozitie = u"Lider"
        if "lider_asistent" in form.cleaned_data and form.cleaned_data['lider_asistent'] == True:
            pozitie = u"Lider asistent"

        return pozitie

    def form_valid(self, form):
        self.object = form.save(commit=False)

        import random
        import string

        parola = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))

        self.object.user = User.objects.create_user(self.object.email, self.object.email, parola)
        self.object.user.is_active = True
        self.object.user.save()
        self.object.timestamp_registered = datetime.datetime.now()
        self.object.timestamp_confirmed = datetime.datetime.now()
        self.object.timestamp_accepted = datetime.datetime.now()

        self.object.hash = hashlib.md5("%s%s" % (SECRET_KEY, self.object.email)).hexdigest()
        self.object.save()

        pozitie = self.create_associations(form=form)
        info_kwargs = {
            "tip_informatie": TipInformatieContact.objects.get(nume=u"Email", relevanta__icontains=u"Membru"),
            "valoare": self.object.email,
            "data_start": datetime.datetime.now(),
            "content_type": ContentType.objects.get_for_model(self.object),
            "object_id": self.object.id}

        InformatieContact(**info_kwargs).save()

        info_kwargs.update({"tip_informatie": TipInformatieContact.objects.get(nume=u"Adresă corespondență",
                                                                               relevanta__icontains=u"Membru"),
                            "valoare": self.object.adresa})
        InformatieContact(**info_kwargs).save()

        if self.object.telefon:
            info_kwargs.update(
                {"tip_informatie": TipInformatieContact.objects.get(nume=u"Mobil", relevanta__icontains=u"Membru"),
                 "valoare": self.object.telefon})
            InformatieContact(**info_kwargs).save()

        if not DEBUG:
            self.send_email(parola)

        messages.success(self.request,
                         u"Adăugat cu succes pe %s, %s la %s" % (self.object, pozitie, self.get_unitate(form=form)))
        return HttpResponseRedirect(self.get_success_url())

    def get_unitate(self, *args, **kwargs):
        try:
            form = kwargs.pop("form")
        except Exception, e:
            logger.error("%s: %s, %s" % (self.__class__.__name__, e, traceback.format_exc()))
            raise e

        if "unitate" not in form.cleaned_data or not form.cleaned_data['unitate']:
            return None

        return form.cleaned_data['unitate']

    def get_centru_local(self, *args, **kwargs):
        return self.centru_local

    def create_associations(self, form):
        try:
            asociere = self.object.asociaza(u"Membru", self.get_centru_local(), form.cleaned_data['data_start_membru'])
            asociere.confirma(self.request.user.get_profile())
        except Exception, e:
            logger.error(
                u"%s: asocierea cu centrul local a esuat: %s %s" % (self.__class__.__name__, e, traceback.format_exc()))

        pozitie = self.get_pozitie(form=form)

        try:
            unitate = self.get_unitate(form=form)
            if unitate:
                asociere = self.object.asociaza(pozitie, unitate, form.cleaned_data['data_start_unitate'])
                asociere.confirma(self.request.user.get_profile())
        except Exception, e:
            logger.error(
                u"%s: asocierea cu unitatea a esuat: %s %s" % (self.__class__.__name__, e, traceback.format_exc()))

        return pozitie

    def send_email(self, parola):
        if not DEBUG or USE_EMAIL_CONFIRMATION:
            message = render_to_string("structuri/inregistrare/registration_by_admin.txt",
                                       {"utilizator": self.object,
                                        "parola": parola},
                                       context_instance=RequestContext(self.request))
            send_mail(u"Cont ScoutFile", message, SYSTEM_EMAIL, [self.object.email, ])


    def get_context_data(self, **kwargs):
        if self.doar_lideri:
            kwargs.update({"tip": "lider"})
        kwargs.update({"centru_local": self.get_centru_local()})
        return super(CentruLocalLiderCreate, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("structuri:cl_detail", kwargs={"pk": self.centru_local.id}) + "#lideri"


class CentruLocalMembruCreate(CentruLocalLiderCreate):
    model = Membru
    form_class = MembruCreateForm
    doar_lideri = False

    @allow_by_afiliere([("Centru Local", u"Lider")])
    def dispatch(self, request, *args, **kwargs):
        kwargs.update({"skip_checks": True})
        return super(CentruLocalMembruCreate, self).dispatch(request, *args, **kwargs)

    def get_pozitie(self, *args, **kwargs):
        return u"Membru"

    def get_success_url(self):
        return reverse("structuri:cl_detail", kwargs={"pk": self.centru_local.id}) + "#membri"


class CentruLocalMembruAsociaza(CreateView):
    model = AsociereMembruStructura

class CentruLocalMembriPending(ListView):
    model = Membru
    template_name = "structuri/centrulocal_membri_pending.html"

    @allow_by_afiliere([("Centru Local", u"Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.centru_local = get_object_or_404(CentruLocal, id=kwargs.pop("pk"))

        if not request.user.get_profile().membru.are_calitate(u"Membru Consiliu Centru Local", self.centru_local):
            return HttpResponseRedirect(reverse("login") + "?unauthorized")

        return super(CentruLocalMembriPending, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.model.objects.filter(timestamp_accepted__isnull=True, timestamp_confirmed__isnull=False)
        qs = qs.filter(centru_local=self.centru_local).order_by("timestamp_confirmed")
        return qs

    def get_context_data(self, **kwargs):
        current = super(CentruLocalMembriPending, self).get_context_data(**kwargs)
        current.update({"cl": self.centru_local})
        return current


class CentruLocalTabBrief(DetailView):
    model = CentruLocal
    template_name = "structuri/centrulocal_tab_brief.html"

    @allow_by_afiliere([("Centru Local", u"Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(CentruLocalTabBrief, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        current = super(CentruLocalTabBrief, self).get_context_data(**kwargs)
        qs = AsociereMembruStructura.objects.filter(content_type=ContentType.objects.get_for_model(self.object),
                                                    object_id=self.object.id,
                                                    membru__timestamp_accepted__isnull=True,
                                                    membru__timestamp_confirmed__isnull=False,
                                                    tip_asociere__nume__iexact=u"Membru").order_by(
            "membru__timestamp_confirmed")

        current.update({"membri_spre_aprobare": [a.membru for a in qs]})
        return current


class CentruLocalTabUnitati(ListView):
    model = Unitate
    template_name = "structuri/centrulocal_tab_unitati.html"

    @allow_by_afiliere([("Centru Local", u"Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.centru_local = get_object_or_404(CentruLocal, id=kwargs.pop("pk"))
        return super(CentruLocalTabUnitati, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(CentruLocalTabUnitati, self).get_queryset(*args, **kwargs)
        qs = qs.filter(centru_local=self.centru_local, activa=True)
        return qs

    def get_context_data(self, **kwargs):
        current = super(CentruLocalTabUnitati, self).get_context_data(**kwargs)
        current.update({"centru_local": self.centru_local})
        if self.request.GET.has_key("tab"):
            current.update({"tab": self.request.GET.get("tab")})
        return current


class CentruLocalTabLideri(ListView):
    model = AsociereMembruStructura
    template_name = "structuri/centrulocal_tab_membri.html"

    @allow_by_afiliere([("Centru Local", u"Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.centru_local = get_object_or_404(CentruLocal, id=kwargs.pop("pk"))
        return super(CentruLocalTabLideri, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return self.centru_local.lideri(qs=True)

class ContactTab(ListView):
    model = InformatieContact

    def dispatch(self, request, *args, **kwargs):
        self.target_object = self.get_target_object(kwargs)
        return super(ContactTab, self).dispatch(request, *args, **kwargs)

    def get_target_object(self, kwargs):
        if self.target_model == None:
            raise ImproperlyConfigured

        return get_object_or_404(self.target_model, id=kwargs.pop("pk"))

    def get_queryset(self):
        kwargs = {"content_type": ContentType.objects.get_for_model(self.target_object),
                  "object_id": self.target_object.id}

        return super(ContactTab, self).get_queryset().filter(**kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({"object": self.target_object})
        return super(ContactTab, self).get_context_data(**kwargs)


class CentruLocalTabContact(ContactTab):
    template_name = "structuri/centrulocal_tab_contact.html"
    target_model = CentruLocal

    @allow_by_afiliere([("Centru Local", u"Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(CentruLocalTabContact, self).dispatch(request, *args, **kwargs)


class CentruLocalTabMembri(ListView):
    model = AsociereMembruStructura
    template_name = "structuri/centrulocal_tab_membri.html"

    @allow_by_afiliere([("Centru Local", u"Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.centru_local = get_object_or_404(CentruLocal, id=kwargs.pop("pk"))
        return super(CentruLocalTabMembri, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return self.centru_local.cercetasi(qs=True, tip_asociere=CentruLocal.asocieri_membru).select_related("membru")


class CentruLocalTabMembriDeSuspendat(CentruLocalTabMembri):
    model = AsociereMembruStructura
    template_name = "structuri/centrulocal_tab_membri.html"

    def membru_fits_query(self, membru):
        status_cotizatie = membru._status_cotizatie()
        print status_cotizatie
        return not membru.is_suspendat() and status_cotizatie[0] >= 2

    def get_queryset(self, *args, **kwargs):
        qs = self.centru_local.cercetasi(qs=True, tip_asociere=CentruLocal.asocieri_membru).select_related("membru")
        qs = [a for a in qs if self.membru_fits_query(a.membru)]
        return qs

class MembriFaraAfilieri(ListView):
    model = Membru
    template_name = "structuri/membri_deconectati.html"

    @method_decorator(user_passes_test(lambda x: x.is_staff))
    def dispatch(self, request, *args, **kwargs):
        self.approved = False
        if "approved" in request.GET:
            self.approved = True
        return super(MembriFaraAfilieri, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = self.model.objects.exclude(afilieri__content_type=ContentType.objects.get_for_model(CentruLocal),
                                        afilieri__tip_asociere__nume__iexact=u"Membru",
                                        afilieri__moment_incheiere__isnull=True,
                                        afilieri__confirmata=True)

        return qs


class CentruLocalMembri(CentruLocalTabMembri):
    template_name = "structuri/centrulocal_membri.html"

    @allow_by_afiliere([("Centru Local", u"Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.rdv = None
        if "rdv" in request.GET and request.GET['rdv']:
            self.rdv = request.GET['rdv']

        self.q = None
        if "q" in request.GET and request.GET['q']:
            self.q = request.GET['q']

        self.switches = {"activi": {"filter": lambda m: not m.is_suspendat() and not m.is_aspirant() and not m.is_adult() and not m.is_inactiv()},
                         "inactivi": {"filter": lambda m: m.is_inactiv()},
                         "suspendati": {"filter": lambda m: m.is_suspendat()},
                         "aspiranti": {"filter": lambda m: m.is_aspirant()},
                         "adulti": {"filter": lambda m: m.is_adult()}}

        for switch in self.switches.keys():
            self.switches[switch]["value"] = int(request.GET.get(switch, request.session.get("membri_%s" % switch, 1)))

        #   initialise and maintain session values for current values
        for switch in self.switches.keys():
            request.session["membri_%s" % switch] = self.switches.get(switch).get("value")
        print self.switches

        kwargs.update({"skip_checks": True})
        return super(CentruLocalMembri, self).dispatch(request, *args, **kwargs)

    def check_switches(self, a):
        valid = False
        for s in self.switches.values():
            if s.get("value", 0):
                valid = s.get("filter")(a.membru) or valid
        return valid

    def get_queryset(self, *args, **kwargs):
        qs = super(CentruLocalMembri, self).get_queryset(*args, **kwargs)

        if self.q:
            qs = qs.filter(Q(membru__nume__icontains=self.q) | Q(membru__prenume__icontains=self.q))

        if self.rdv:
            if self.rdv in ("lupisori", "exploratori", "seniori", "temerari", "adulti"):
                membri = [a.membru for a in qs]
                membri_final = []
                for membru in membri:
                    if membru.is_lider():
                        continue
                    unitate = membru.get_unitate()
                    if unitate and unitate.ramura_de_varsta.slug == self.rdv:
                        membri_final.append(membru)

                qs = qs.filter(membru__in=membri_final)
            elif self.rdv in ("lideri", ):
                membri_final = []
                for membru in [a.membru for a in qs]:
                    if membru.is_lider():
                        membri_final.append(membru)

                qs = qs.filter(membru__in=membri_final)
        qs = qs.order_by("membru__nume", "membru__prenume")

        #   verifica daca toate categoriile sunt selectate
        if sum([s.get("value") for s in self.switches.values()]) != len(self.switches.keys()):
            qs = AsociereMembruStructura.objects.filter(id__in=[a.id for a in qs if self.check_switches(a)])
        return qs

    def get_context_data(self, **kwargs):
        kwargs.update({"object": self.centru_local})
        return super(CentruLocalMembri, self).get_context_data(**kwargs)


class CentruLocalUnitateCreate(CreateView):
    model = Unitate
    form_class = CentruLocalUnitateCreateForm

    @allow_by_afiliere([("Centru Local", u"Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        self.centru_local = get_object_or_404(CentruLocal, id=kwargs.pop("pk"))
        return super(CentruLocalUnitateCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.centru_local = self.centru_local
        self.object.activa = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:cl_detail", kwargs={"pk": self.centru_local.id}) + "#unitati"

    def get_context_data(self, **kwargs):
        current = super(CentruLocalUnitateCreate, self).get_context_data(**kwargs)
        current.update({"centru_local": self.centru_local})
        return current


class UnitateUpdate(UpdateView):
    model = Unitate
    form_class = UnitateUpdateForm

    @allow_by_afiliere([("Unitate", u"Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(UnitateUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, u"%s a fost modificată" % self.object)
        return super(UnitateUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("structuri:unitate_detail", kwargs={"pk": self.object.id})


class UnitateDetail(DetailView, TabbedViewMixin):
    model = Unitate

    @allow_by_afiliere([("Unitate, Centru Local", u"Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(UnitateDetail, self).dispatch(request, *args, **kwargs)

    def get_tabs(self, *args, **kwargs):
        self.tabs = [("brief", u"Sumar", reverse("structuri:unitate_tab_brief", kwargs={"pk": self.object.id}), "", 1),
                     ("membri", u"Membri", reverse("structuri:unitate_tab_membri", kwargs={"pk": self.object.id}), "", 3)]
        if self.object.ramura_de_varsta.are_patrule:
            self.tabs.append(("patrule", u"Patrule", reverse("structuri:unitate_tab_patrule", kwargs={"pk": self.object.id}), "", 2))
            self.tabs.append(("membri_fp", u"Membri fără patrulă", reverse("structuri:unitate_tab_membri_fara_patrula", kwargs={"pk": self.object.id}), "", 4))
            self.tabs.append(("patrule_inactive", u"Patrule inactive", reverse("structuri:unitate_tab_patrule_inactive", kwargs={"pk": self.object.id}), "", 5))

        return super(UnitateDetail, self).get_tabs(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        current = super(UnitateDetail, self).get_context_data(*args, **kwargs)
        current.update(self.get_tabs())
        return current


class UnitateMembruCreate(CentruLocalMembruCreate):
    form_class = UnitateMembruCreateForm
    doar_lideri = False

    @allow_by_afiliere([("Unitate", u"Lider"), ("Unitate, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        self.unitate = get_object_or_404(Unitate, id=kwargs.pop("pk"))
        self.centru_local = self.unitate.centru_local

        kwargs.update({"skip_checks": True})
        return super(UnitateMembruCreate, self).dispatch(request, *args, **kwargs)

    def get_unitate(self, *args, **kwargs):
        return self.unitate

    def get_success_url(self):
        return reverse("structuri:unitate_detail", kwargs={"pk": self.unitate.id}) + "#membri"

    def get_context_data(self, **kwargs):
        kwargs.update({"unitate": self.get_unitate()})
        return super(UnitateMembruCreate, self).get_context_data(**kwargs)


class UnitateLiderCreate(UnitateMembruCreate):
    form_class = UnitateLiderCreateForm
    doar_lideri = True

    @allow_by_afiliere([("Unitate, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        kwargs.update({"skip_checks": True})
        return super(UnitateLiderCreate, self).dispatch(request, *args, **kwargs)

    def get_pozitie(self, *args, **kwargs):
        try:
            form = kwargs.get("form")
        except Exception, e:
            logger.error("%s: %s, %s" % (self.__class__.__name__, e, traceback.format_exc()))
            raise e

        pozitie = u"Lider"
        if "lider_asistent" in form.cleaned_data and form.cleaned_data['lider_asistent'] == True:
            pozitie = u"Lider asistent"

        return pozitie

    def get_success_url(self):
        return reverse("structuri:unitate_detail", kwargs={"pk": self.unitate.id}) + "#brief"


class UnitateTabBrief(ListView):
    model = AsociereMembruStructura
    template_name = "structuri/unitate_tab_brief.html"

    @allow_by_afiliere([("Unitate, Centru Local", "Lider")])
    def dispatch(self, *args, **kwargs):
        self.unitate = get_object_or_404(Unitate, id=kwargs.pop("pk"))
        return super(UnitateTabBrief, self).dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return self.unitate.lideri(qs=True)

    def get_context_data(self, **kwargs):
        kwargs.update({"object": self.unitate})
        return super(UnitateTabBrief, self).get_context_data(**kwargs)


class UnitateDelete(GenericDeleteView):
    model = Unitate

    @allow_by_afiliere([("Unitate, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(UnitateDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("structuri:cl_detail", kwargs={"pk": self.object.centru_local.id}) + "#unitati"


class UnitateTabPatrule(ListView):
    model = Patrula
    template_name = "structuri/unitate_tab_patrule.html"

    @allow_by_afiliere([("Unitate, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.unitate = get_object_or_404(Unitate, id=kwargs.pop("pk"))
        return super(UnitateTabPatrule, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return self.unitate.patrule()

    def get_context_data(self, *args, **kwargs):
        data = super(UnitateTabPatrule, self).get_context_data(*args, **kwargs)
        data["unitate"] = self.unitate
        return data


class UnitateTabPatruleInactive(UnitateTabPatrule):
    template_name = "structuri/unitate_tab_patrule_inactive.html"
    def get_queryset(self, *args, **kwargs):
        return self.unitate.patrule_inactive()

    def get_context_data(self, *args, **kwargs):
        data = super(UnitateTabPatruleInactive, self).get_context_data(**kwargs)
        data['inactive'] = True
        return data



class UnitateTabMembri(ListView):
    model = AsociereMembruStructura
    template_name = "structuri/unitate_tab_membri.html"

    @allow_by_afiliere([("Unitate, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.unitate = get_object_or_404(Unitate, id=kwargs.pop("pk"))
        return super(UnitateTabMembri, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        tip_asociere_membru = TipAsociereMembruStructura.objects.get(nume=u"Membru", content_types__in=[ContentType.objects.get_for_model(self.unitate)])
        asocieri = AsociereMembruStructura.objects.filter(content_type=ContentType.objects.get_for_model(Unitate),
                                                          object_id=self.unitate.id,
                                                          tip_asociere=tip_asociere_membru,
                                                          moment_incheiere__isnull=True)

        return asocieri

    def get_context_data(self, **kwargs):
        kwargs.update({"unitate": self.unitate})
        return super(UnitateTabMembri, self).get_context_data(**kwargs)


class UnitateTabMembriFaraPatrula(UnitateTabMembri):
    def get_queryset(self, **kwargs):
        qs = super(UnitateTabMembriFaraPatrula, self).get_queryset(**kwargs)
        return [a for a in qs if a.membru.get_patrula() is None]


class UnitateMembruAsociaza(CreateView):
    model = AsociereMembruStructura


class UnitatePatrulaCreate(CreateView):
    model = Patrula
    form_class = PatrulaCreateForm

    @allow_by_afiliere([("Unitate", "Lider"), ("Unitate, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        self.unitate = get_object_or_404(Unitate, id=kwargs.pop("pk"))
        return super(UnitatePatrulaCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.unitate = self.unitate
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        current = super(UnitatePatrulaCreate, self).get_context_data(*args, **kwargs)
        current.update({"unitate": self.unitate})
        return current

    def get_success_url(self):
        return reverse("structuri:unitate_detail", kwargs={"pk": self.unitate.id}) + "#patrule"


class PatrulaUpdate(UpdateView):
    model = Patrula
    form_class = PatrulaUpdateForm

    @allow_by_afiliere([("Patrula, Unitate", "Lider"), ("Patrula, Unitate, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(PatrulaUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({"unitate": self.object.unitate})
        return super(PatrulaUpdate, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("structuri:unitate_detail", kwargs={"pk": self.object.unitate.id}) + "#patrule"


class PatrulaDetail(DetailView, TabbedViewMixin):
    model = Patrula

    @allow_by_afiliere([("Patrula, Unitate, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(PatrulaDetail, self).dispatch(request, *args, **kwargs)

    def get_tabs(self, *args, **kwargs):
        self.tabs = (("brief", "Sumar", reverse("structuri:patrula_tab_brief", kwargs={"pk": self.object.id}), "", 2),
                     ("membri", u"Membri", reverse("structuri:patrula_tab_membri", kwargs={"pk": self.object.id}), "", 1))

        return super(PatrulaDetail, self).get_tabs(*args, **kwargs)

    def get_context_data(self, **kwargs):
        current = super(PatrulaDetail, self).get_context_data(**kwargs)
        current.update(self.get_tabs())
        return current


class PatrulaTabBrief(DetailView):
    model = Patrula
    template_name = "structuri/patrula_tab_brief.html"

    @allow_by_afiliere([("Patrula, Unitate, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(PatrulaTabBrief, self).dispatch(request, *args, **kwargs)


class PatrulaTabMembri(ListView):
    model = Membru
    template_name = "structuri/patrula_tab_membri.html"


    @allow_by_afiliere([("Patrula, Unitate, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.patrula = get_object_or_404(Patrula, id=kwargs.pop("pk"))
        return super(PatrulaTabMembri, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        tip_asociere_membru = TipAsociereMembruStructura.objects.get(nume=u"Membru", content_types__in=(
            ContentType.objects.get_for_model(Patrula),))
        asocieri = AsociereMembruStructura.objects.filter(content_type=ContentType.objects.get_for_model(Patrula),
                                                          object_id=self.patrula.id,
                                                          tip_asociere=tip_asociere_membru,
                                                          moment_incheiere__isnull=True)

        return asocieri

    def get_context_data(self, **kwargs):
        data = super(PatrulaTabMembri, self).get_context_data(**kwargs)
        data['object'] = self.patrula
        # data['form'] = self.form_class()
        return data

class PatrulaDelete(GenericDeleteView):
    model = Patrula

    @allow_by_afiliere([("Unitate", "Lider"), ("Unitate, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(PatrulaDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("structuri:unitate_detail", kwargs={"pk": self.object.unitate.id}) + "#patrule"


class PatrulaMembruCreate(CreateView):
    model = Membru
    form_class = MembruCreateForm

    @allow_by_afiliere([("Unitate", "Lider"), ("Unitate, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        self.patrula = get_object_or_404(Patrula, id=kwargs.pop("pk"))

        membru = request.user.get_profile().membru
        if not membru.are_calitate(u"Membru Consiliu Centru Local",
                                   self.patrula.unitate.centru_local) and not membru.are_calitate(u"Lider",
                                                                                                  self.patrula.unitate):
            return HttpResponseRedirect(reverse("login") + "?unauthorized")

        return super(PatrulaTabMembri, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        tip_asociere_membru = TipAsociereMembruStructura.objects.get(nume=u"Membru")
        asociere = AsociereMembruStructura(content_type=ContentType.objects.get_for_model(Patrula),
                                           object_id=self.patrula.id,
                                           tip_asociere=tip_asociere_membru,
                                           membru=self.object)
        asociere.save()

        return HttpResponseRedirect(self.get_success_url())


class PatrulaMembruAsociaza(CreateView):
    model = AsociereMembruStructura
    form_class = PatrulaMembruAsociazaForm
    template_name = "structuri/membru_asociere_form.html"

    @allow_by_afiliere([("Patrula, Unitate, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.patrula = get_object_or_404(Patrula, id=kwargs.pop("pk"))
        return super(PatrulaMembruAsociaza, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.content_type = ContentType.objects.get_for_model(Patrula)
        self.object.object_id = self.patrula.id

        #   verifica daca membrul are o alta asociere la o patrula.
        #   daca are, o inceteaza din data in care este mutat la patrula curenta
        asociere_patrula = self.object.membru.get_patrula(qs=True)
        if asociere_patrula:
            asociere_patrula.moment_incheiere = form.cleaned_data['asociere_inceput']
            asociere_patrula.save()

        asociere = self.object.membru.asociaza("membru", self.patrula,
                                               data_start=form.cleaned_data['asociere_inceput'],
                                               confirmata=True,
                                               user=self.request.user.get_profile())
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        data = super(PatrulaMembruAsociaza, self).get_form_kwargs()
        data['patrula'] = self.patrula
        return data

    def get_success_url(self):
        return reverse("structuri:patrula_detail", kwargs={"pk": self.patrula.id}) + "#membri"

    def get_context_data(self, **kwargs):
        data = super(PatrulaMembruAsociaza, self).get_context_data(**kwargs)
        data['target_object'] = self.patrula
        return data

class MembruUpdate(UpdateView):
    model = Membru
    form_class = MembruUpdateForm
    template_name = "structuri/membru_form.html"

    @allow_by_afiliere([("Membru, Unitate", "Lider"), ("Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(MembruUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.email != self.object.user.username:
            self.object.user.email = self.object.email
            self.object.user.username = self.object.email
            self.object.user.save()

            if not DEBUG:
                send_mail(u"Schimbare cont ScoutFile",
                          u"Utilizatorul tau pentru ScoutFile a fost schimbat pe această adresa.\n\nNumai bine,\nyeti",
                          SERVER_EMAIL,
                          [self.object.email, ])

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.object.id})


class MembruEditProfilePicture(UpdateView):
    form_class = UtilizatorProfilePictureForm
    template_name = "structuri/membru_edit_profile_picture.html"
    model = Membru

    @allow_by_afiliere([("Membru, Unitate", "Lider"), ("Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(MembruEditProfilePicture, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        try:
            #    upload the file
            uploaded_file = self.request.FILES['poza_profil']
            with open('%sprofil/%d-%s' % (MEDIA_ROOT, self.object.id, uploaded_file.name), 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        except Exception, e:
            logger.error(
                u"%s: nu am putut să uploades poza. %s : %s" % (self.__class__.__name__, e, traceback.format_exc()))
            messages.error(self.request, u"Nu am putut încărca poza (%s)" % e)
            return HttpResponseRedirect(reverse("structuri:membru_edit_profile_picture"))

        #        if self.object.poza_profil != None:
        #            self.object.poza_profil.delete()

        poza_profil = ImagineProfil(image="profil/%d-%s" % (self.object.id, uploaded_file.name))
        poza_profil.save()
        self.object.poza_profil = poza_profil
        self.object.save()

        messages.success(self.request, u"Poza de profil a fost modificată cu success")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.object.id})


class MembruDetail(DetailView, TabbedViewMixin):
    model = Membru

    @allow_by_afiliere(
        [("Membru, Centru Local", "Lider"), ("Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(MembruDetail, self).dispatch(request, *args, **kwargs)

    def get_tabs(self):
        self.tabs = (("brief", u"Sumar", reverse("structuri:membru_tab_brief", kwargs={"pk": self.object.id}), "", 1),
                     ("afilieri", u"Afilieri", reverse("structuri:membru_tab_afilieri", kwargs={"pk": self.object.id}),"", 2),
                     ("contact", u"Contact", reverse("structuri:membru_tab_contact", kwargs={"pk": self.object.id}), "", 3),
                     ("familie", u"Familie", reverse("structuri:membru_tab_familie", kwargs={"pk": self.object.id}), "", 4),
                     ('documente', u"Documente", reverse("structuri:membru_tab_documente", kwargs={"pk": self.object.id}), "", 5),
                     ('activitati', u"Activități", reverse("structuri:membru_tab_activitati", kwargs={"pk": self.object.id}), "icon-calendar", 6),
        )
        return super(MembruDetail, self).get_tabs()

    def get_context_data(self, **kwargs):
        kwargs.update(self.get_tabs())
        return super(MembruDetail, self).get_context_data(**kwargs)


class MembruCard(DetailView):
    model = Membru


class MembruProgresPersonal(DetailView):
    model = Membru


class MembruTabBrief(DetailView):
    model = Membru
    template_name = "structuri/membru_tab_brief.html"

    @allow_by_afiliere(
        [("Membru, Centru Local", "Lider"), ("Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(MembruTabBrief, self).dispatch(request, *args, **kwargs)


class MembruTabDocumente(ListView):
    model = Membru
    template_name = "structuri/membru_tab_documente.html"

    @allow_by_afiliere([("Membru, Centru Local", "Lider"), ])
    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, id=kwargs.pop("pk"))
        return ListView.dispatch(self, request, *args, **kwargs)

    def get_queryset(self):
        from documente.models import AsociereDocument
        filter_kwargs = {"content_type": ContentType.objects.get_for_model(self.object),
                         "object_id": self.object.id}

        return AsociereDocument.objects.filter(**filter_kwargs).order_by("-moment_asociere")

    def get_context_data(self, **kwargs):
        data = super(MembruTabDocumente, self).get_context_data(**kwargs)
        data.update({"object": self.object})
        return data


class MembruTabConexiuni(DetailView):
    model = Membru
    template_name = "structuri/membru_tab_conexiuni.html"

    @allow_by_afiliere(
        [("Membru, Centru Local", "Lider"), ("Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(MembruTabConexiuni, self).dispatch(request, *args, **kwargs)


class MembruTabIstoric(DetailView):
    model = Membru
    template_name = "structuri/membru_tab_istoric.html"

    @allow_by_afiliere(
        [("Membru, Centru Local", "Lider"), ("Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(MembruTabIstoric, self).dispatch(request, *args, **kwargs)


class MembruTabContact(ContactTab):
    template_name = "structuri/membru_tab_contact.html"
    target_model = Membru

    @allow_by_afiliere(
        [("Membru, Centru Local", "Lider"), ("Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(MembruTabContact, self).dispatch(request, *args, **kwargs)


class MembruTabFamilie(DetailView):
    template_name = "structuri/membru_tab_familie.html"
    model = Membru

    @allow_by_afiliere([("Membru, Centru Local", "Lider"), ("Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(MembruTabFamilie, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({"object_list": self.object.asocieremembrufamilie_set.all(),
                       "nonmembru_object_list": self.object.persoanadecontact_set.all(), })
        return super(MembruTabFamilie, self).get_context_data(**kwargs)


class MembruTabActivitati(ListView):
    model = ParticipareEveniment
    template_name = "structuri/membru_tab_activitati.html"

    @allow_by_afiliere([("Membru, Centru Local", "Lider"), ("Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        self.membru = get_object_or_404(Membru, id=kwargs.pop("pk"))
        return super(MembruTabActivitati, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(membru=self.membru)


#   registration views

class ChangePassword(FormView):
    form_class = ChangePasswordForm
    template_name = "structuri/inregistrare/password_change.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return FormView.dispatch(self, request, *args, **kwargs)

    def get_form_kwargs(self):
        current = super(ChangePassword, self).get_form_kwargs()
        current.update({"request": self.request})
        return current

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data['parola'])
        self.request.user.save()

        messages.success(self.request, u"Parola ta a fost schimbată!")
        #TODO: think if it is needed to send user an email to make sure he remembers

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("login")


class ForgotPassword(FormView):
    form_class = ForgotPasswordForm
    template_name = "structuri/inregistrare/password_reset.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        return super(ForgotPassword, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            utilizator = Utilizator.objects.get(email=form.cleaned_data['email'])
        except Utilizator.DoesNotExist:
            messages.error(self.request, u"Nu am găsit niciun utilizator care sa aibă adresa pe care ai introdus-o")
            return HttpResponseRedirect(reverse("structuri:membru_forgot_password"))

        if utilizator.timestamp_accepted == None:
            messages.error(self.request,
                           u"Utilizatorul există, dar nu a fost încă confirmat de un lider. Așteaptă pentru când este confirmat, apoi solicită resetarea parolei!")
            return HttpResponseRedirect(reverse("structuri:membru_forgot_password"))

        utilizator.requested_password_reset = True
        utilizator.save()

        if not DEBUG or USE_EMAIL_CONFIRMATION:
            message = render_to_string("structuri/inregistrare/password_reset.txt",
                                       {"utilizator": utilizator, "form": form},
                                       context_instance=RequestContext(self.request))
            send_mail(u"Solicitare resetare parola ScoutFile", message, SYSTEM_EMAIL, [utilizator.email, ])

        logger.debug("%s: email sent" % self.__class__.__name__)

        messages.success(self.request, u"Un email cu instructiuni a fost trimis la adresa %s" % utilizator.email)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        logger.debug(u"form_invalid")
        return super(ForgotPassword, self).form_invalid(form)

    def get_success_url(self):
        return reverse("index")


class ConfirmForgotPassword(TemplateView):
    template_name = "structuri/inregistrare/password_reset_confirm.html"

    def dispatch(self, request, *args, **kwargs):
        self.utilizator = get_object_or_404(Utilizator, hash=kwargs.pop("hash"), requested_password_reset=True)

        #    the user exists and required password change
        #    do password change
        import random
        import string

        new_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
        self.utilizator.user.set_password(new_password)
        self.utilizator.user.save()

        self.utilizator.requested_password_reset = False
        self.utilizator.save()

        if not DEBUG or USE_EMAIL_CONFIRMATION:
            message = render_to_string("structuri/inregistrare/password_reset_confirm.txt",
                                       {"utilizator": self.utilizator, "password": new_password},
                                       context_instance=RequestContext(request))
            send_mail("Parola noua pentru ScoutFile", message, SYSTEM_EMAIL, [self.utilizator.email, ])

        messages.success(request,
                         u"O nouă parola a fost generată și trimisă pe adresa ta de email, %s" % self.utilizator.email)
        return HttpResponseRedirect(reverse("login"))


class RegisterMembru(CreateView):
    model = Membru
    form_class = MembruRegistrationForm
    template_name = "structuri/inregistrare/registration_form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        return super(RegisterMembru, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.user = User.objects.create_user(self.object.email, self.object.email, form.cleaned_data['parola'])
        self.object.user.is_active = False
        self.object.user.save()
        self.object.timestamp_registered = datetime.datetime.now()

        self.object.hash = hashlib.md5("%s%s" % (SECRET_KEY, self.object.email)).hexdigest()
        self.object.save()

        #    se creaza asocierile de membru
        tip_asociere, created = TipAsociereMembruStructura.objects.get_or_create(nume=u"Membru")
        if created:
            tip_asociere.save()

        asociere = AsociereMembruStructura(membru=self.object,
                                           content_type=ContentType.objects.get_for_model(
                                               form.cleaned_data['centrul_local']),
                                           object_id=form.cleaned_data['centrul_local'].id,
                                           tip_asociere=tip_asociere)
        asociere.save()

        asociere = AsociereMembruStructura(membru=self.object,
                                           content_type=ContentType.objects.get_for_model(form.cleaned_data['unitate']),
                                           object_id=form.cleaned_data['unitate'].id,
                                           tip_asociere=tip_asociere)
        asociere.save()

        if not DEBUG or USE_EMAIL_CONFIRMATION:
            #    send user confirmation required email
            body = render_to_string("structuri/inregistrare/registration_email.txt",
                                    {"utilizator": self.object, "centru_local": form.cleaned_data['centrul_local'],
                                     "unitate": form.cleaned_data['unitate']},
                                    context_instance=RequestContext(self.request))
            send_mail("Inregistrare ScoutFile", body, SYSTEM_EMAIL, [self.object.email, ])

        messages.success(self.request,
                         u"Solicitarea ta a fost trimisă, vei primi un email cu un link pentru confirmare!")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("login")

    def get_context_data(self, *args, **kwargs):
        current = super(RegisterMembru, self).get_context_data(*args, **kwargs)
        return current


class ConfirmMembruRegistration(TemplateView):
    template_name = "structuri/inregistrare/registration_confirm.html"

    def dispatch(self, *args, **kwargs):
        try:
            self.membru = Membru.objects.get(hash=kwargs.pop("hash"))
        except Membru.DoesNotExist, e:
            self.msg_code = "doesnotexist"
        except Exception, e:
            self.msg_code = "otherproblem"

        if self.membru.timestamp_confirmed != None:
            self.msg_code = "alreadyconfirmed"
        else:
            self.membru.timestamp_confirmed = datetime.datetime.now()
            self.membru.save()
            self.msg_code = "confirmed"

        return super(ConfirmMembruRegistration, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        current = super(ConfirmMembruRegistration, self).get_context_data(**kwargs)
        current.update({"msg": self.msg_code, "membru": self.membru})
        return current


class ConfirmMembruAdmin(UpdateView):
    model = Membru
    form_class = ConfirmMembruAdminForm
    template_name = "structuri/inregistrare/registration_accept.html"

    @allow_by_afiliere([("Membru, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(ConfirmMembruAdmin, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if "reject" in self.request.POST:
            #    creating message here, the Membru object does not exist anymore when sending email
            message = render_to_string("structuri/inregistrare/registration_deny.txt", {"membru": self.object},
                                       context_instance=RequestContext(self.request)),

            for asociere in AsociereMembruStructura.objects.filter(membru=self.object):
                asociere.delete()
            self.object.delete()

            if not DEBUG or USE_EMAIL_CONFIRMATION:
                messages.warning(self.request, u"Solicitarea de înregistrare a fost respinsă.")
                send_mail(u"Notificare respingere cont pe ScoutFile",
                          message,
                          SYSTEM_EMAIL,
                          [self.object.email, ])

            return HttpResponseRedirect(reverse("structuri:cl_membri_pending",
                                                kwargs={"pk": self.request.user.get_profile().membru.centru_local.id}))

        self.object.user.is_active = True
        self.object.user.save()

        self.object.timestamp_accepted = datetime.datetime.now()
        self.object.save()

        for asociere in AsociereMembruStructura.objects.filter(membru=self.object):
            asociere.confirmata = True
            asociere.confirmata_pe = datetime.datetime.now()
            asociere.confirmata_de = self.request.user.get_profile()

            if asociere.moment_inceput == None:
                asociere.moment_inceput = datetime.datetime.now()
            asociere.save()

        if not DEBUG or USE_EMAIL_CONFIRMATION:
            messages.success(self.request, u"Utilizatorul %s a fost confirmat" % self.object)
            send_mail(u"Confirmare acceptare cont pe ScoutFile",
                      render_to_string("structuri/inregistrare/registration_accept.txt", {"membru": self.object},
                                       context_instance=RequestContext(self.request)),
                      SYSTEM_EMAIL,
                      [self.object.email, ])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.object.id})


class UtilizatorHome(TemplateView, TabbedViewMixin):
    template_name = "structuri/utilizator_home.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UtilizatorHome, self).dispatch(request, *args, **kwargs)

    def get_tabs(self):
        self.tabs = (("brief", u"Pe scurt", reverse("structuri:membru_profil_tab_brief"), "", 1),
                     ("documente", u"Documente", reverse("structuri:membru_profil_tab_documente"), "icon-file", 3),
                     ("activitati", u"Activități", reverse("structuri:membru_profil_tab_activitati"), "icon-calendar", 2),
                     ("afiliere", u"Istoric", reverse("structuri:membru_profil_tab_afiliere"), "icon-time", 4))

        return super(UtilizatorHome, self).get_tabs()

    def get_context_data(self, **kwargs):
        current = super(UtilizatorHome, self).get_context_data(**kwargs)
        current.update(self.get_tabs())
        return current


class UtilizatorHomeTabsBrief(TemplateView):
    template_name = "structuri/utilizator_home_brief.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        kwargs['pk'] = request.user.get_profile().membru.id
        return super(UtilizatorHomeTabsBrief, self).dispatch(request, *args, **kwargs)


class UtilizatorHomeTabsAfiliere(UtilizatorHomeTabsBrief):
    template_name = "structuri/utilizator_home_afiliere.html"


class UtilizatorHomeTabsDocumente(ListView):
    template_name = "structuri/utilizator_home_documente.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = request.user.get_profile().membru
        return super(UtilizatorHomeTabsDocumente, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        from documente.models import AsociereDocument
        filter_kwargs = {"content_type": ContentType.objects.get_for_model(self.object),
                         "object_id": self.object.id}

        return AsociereDocument.objects.filter(**filter_kwargs).order_by("-moment_asociere")

    def get_context_data(self, **kwargs):
        data = super(UtilizatorHomeTabsDocumente, self).get_context_data(**kwargs)
        data.update({"object": self.object})
        return data


class UtilizatorHomeTabsActivitati(ListView):
    template_name = "structuri/utilizator_home_activitati.html"
    model = ParticipareEveniment

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UtilizatorHomeTabsActivitati, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.get_profile().membru.participareeveniment_set.all()


class UtilizatorEditProfile(UpdateView):
    form_class = UtilizatorProfileForm
    template_name = "structuri/utilizator_edit_profile.html"
    model = Membru

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UtilizatorEditProfile, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.get_profile().membru

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if self.object.email != self.object.user.username:
            self.object.user.username = self.object.email
            self.object.user.email = self.object.email
            self.object.user.save()

            if not DEBUG:
                send_mail(u"Schimbare cont ScoutFile",
                          u"Utilizatorul tau pentru ScoutFile a fost schimbat pe această adresa.\n\nNumai bine,\nyeti",
                          SERVER_EMAIL,
                          [self.object.email, ])

            messages.success(self.request, u"Numele tău de utilizator a fost schimbat")

        self.object.save()
        messages.success(self.request, u"Datele tale de profil au fost salvate")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:membru_profil")


class UtilizatorEditProfilePicture(UpdateView):
    form_class = UtilizatorProfilePictureForm
    template_name = "structuri/utilizator_edit_profile_picture.html"
    model = Membru

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UtilizatorEditProfilePicture, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        try:
            #    upload the file
            uploaded_file = self.request.FILES['poza_profil']
            with open('%sprofil/%d-%s' % (MEDIA_ROOT, self.object.id, uploaded_file.name), 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        except Exception, e:
            logger.error(
                u"%s: nu am putut să uploades poza. %s : %s" % (self.__class__.__name__, e, traceback.format_exc()))
            messages.error(self.request, u"Nu am putut încărca poza (%s)" % e)
            return HttpResponseRedirect(reverse("structuri:membru_edit_profile_picture"))

        #        if self.object.poza_profil != None:
        #            self.object.poza_profil.delete()

        poza_profil = ImagineProfil(image="profil/%d-%s" % (self.object.id, uploaded_file.name))
        poza_profil.save()
        self.object.poza_profil = poza_profil
        self.object.save()

        messages.success(self.request, u"Poza de profil a fost modificată cu success")
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return self.request.user.get_profile().membru

    def get_success_url(self):
        return reverse("structuri:membru_profil")


class AsociereCreate(CreateView):
    model = AsociereMembruStructura
    form_class = AsociereCreateForm
    template_name = "structuri/afiliere_form.html"

    @allow_by_afiliere([("Membru, Centru Local", "Lider")])
    def dispatch(self, *args, **kwargs):
        self.membru = get_object_or_404(Membru, id=kwargs.pop("pk"))
        return super(AsociereCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.membru = self.membru

        self.object.confirmata = True
        self.object.confirmata_pe = datetime.datetime.now()
        self.object.confirmata_de = self.request.user.utilizator

        self.object.save()
        messages.success(self.request, u"Asocierea a fost creată.")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        kwargs.update({"membru": self.membru})
        return super(AsociereCreate, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.membru.id}) + "#afilieri"


class AsociereUpdate(UpdateView):
    form_class = AsociereUpdateForm
    template_name = "structuri/afiliere_form.html"
    model = AsociereMembruStructura

    @allow_by_afiliere([("Afiliere, Membru, *, Centru Local", "Lider"),
                        ("Afiliere, Membru, *, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(AsociereUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({"membru": self.object.membru,
                       "tip_asociere": self.object.tip_asociere.id,
                       "object_id": self.object.object_id})
        return super(AsociereUpdate, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.object.membru.id}) + "#afilieri"


class GenericContactCreate(CreateView):
    form_class = InformatieContactCreateForm
    model = InformatieContact
    target_model = None

    def dispatch(self, request, *args, **kwargs):
        self.target_object = self.get_target_object(kwargs)
        return super(GenericContactCreate, self).dispatch(request, *args, **kwargs)

    def get_target_object(self, kwargs):
        if self.target_model == None:
            raise ImproperlyConfigured

        return get_object_or_404(self.target_model, id=kwargs.pop("pk"))

    def get_form_kwargs(self):
        current = super(GenericContactCreate, self).get_form_kwargs()
        current.update({"filter_by": self.filter_by})
        return current

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.data_start = datetime.datetime.now()
        self.object.content_type = ContentType.objects.get_for_model(self.target_object)
        self.object.object_id = self.target_object.id
        self.object.save()

        messages.success(self.request, u"Informația a fost adăugată cu succes")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        kwargs.update({"target_object": self.target_object})
        return super(GenericContactCreate, self).get_context_data(**kwargs)


class CentruLocalContactCreate(GenericContactCreate):
    template_name = "structuri/centrulocal_contact_form.html"
    filter_by = "Centru Local"
    target_model = CentruLocal

    @allow_by_afiliere([("Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(CentruLocalContactCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("structuri:cl_detail", kwargs={"pk": self.target_object.id}) + "#contact"


class MembruContactCreate(GenericContactCreate):
    template_name = "structuri/membru_contact_form.html"
    filter_by = "Membru"
    target_model = Membru

    @allow_by_afiliere(
        [("Membru, Centru Local", "Lider"), ("Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(MembruContactCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.target_object.id}) + "#contact"


class ContactUpdate(UpdateView):
    model = InformatieContact
    form_class = InformatieContactUpdateForm
    template_name = "structuri/centrulocal_contact_form.html"

    def dispatch(self, request, *args, **kwargs):
        return super(ContactUpdate, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        current = super(ContactUpdate, self).get_form_kwargs()
        current.update({"filter_by": self.filter_by})
        return current

    def get_context_data(self, **kwargs):
        kwargs.update({"target_object": self.object.content_object})
        return super(ContactUpdate, self).get_context_data(**kwargs)


class CentruLocalContactUpdate(ContactUpdate):
    template_name = "structuri/centrulocal_contact_form.html"
    filter_by = "Centru Local"

    @allow_by_afiliere([("InformatieContact, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(CentruLocalContactUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("structuri:cl_detail", kwargs={"pk": self.object.content_object.id}) + "#contact"


class MembruContactUpdate(ContactUpdate):
    template_name = "structuri/membru_contact_form.html"
    filter_by = "Membru"

    @allow_by_afiliere([("InformatieContact, Membru, Centru Local", "Lider"),
                        ("InformatieContact, Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        return super(MembruContactUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.object.content_object.id}) + "#contact"


class ContactDelete(GenericDeleteView):
    model = InformatieContact
    form_class = InformatieContactDeleteForm

    @allow_by_afiliere([("InformatieContact, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse("structuri:cl_detail", kwargs={"pk": self.get_object().id}) + "#contact"
        return super(ContactDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url


class MembruAddFamilie(CreateView):
    model = AsociereMembruFamilie
    form_class = AsociereMembruFamilieForm
    template_name = "structuri/membru_familie_form.html"

    @allow_by_afiliere([("Membru, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.membru = get_object_or_404(Membru, id=kwargs.pop("pk"))
        return super(MembruAddFamilie, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.persoana_sursa = self.membru
        self.object.save()

        if self.object.tip_relatie.reverse_relationship:
            kwargs = {"persoana_sursa": self.object.persoana_destinatie,
                      "persoana_destinatie": self.object.persoana_sursa,
                      "tip_relatie": self.object.tip_relatie.reverse_relationship}
            AsociereMembruFamilie(**kwargs).save()

        messages.success(self.request, u"Relația a fost adăugată")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.membru.id}) + "#relatii"

    def get_context_data(self, **kwargs):
        kwargs.update({"target_object": self.membru})
        return super(MembruAddFamilie, self).get_context_data(**kwargs)


class MembruEditFamilie(UpdateView):
    model = AsociereMembruFamilie
    form_class = AsociereMembruFamilieForm
    template_name = "structuri/membru_familie_form.html"

    @allow_by_afiliere([("Membru, Centru Local", "Lider")], pkname="mpk")
    def dispatch(self, request, *args, **kwargs):
        return super(MembruEditFamilie, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=True)
        if self.object.tip_relatie.reverse_relationship:
            kwargs = {"persoana_sursa": self.object.persoana_destinatie,
                      "persoana_destinatie": self.object.persoana_sursa,
                      "tip_relatie": self.object.tip_relatie.reverse_relationship}

            if AsociereMembruFamilie.objects.filter(**kwargs).count() == 0:
                AsociereMembruFamilie(**kwargs).save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.object.persoana_sursa.id})

    def get_context_data(self, **kwargs):
        kwargs.update({"target_object": self.object.persoana_sursa})
        return super(MembruEditFamilie, self).get_context_data(**kwargs)


class MembruPersoanaDeContactCreate(CreateView):
    model = PersoanaDeContact
    template_name = "structuri/membru_pdc_form.html"
    form_class = PersoanaDeContactForm

    @allow_by_afiliere([("Membru, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.membru = get_object_or_404(Membru, id=kwargs.pop("pk"))
        return super(MembruPersoanaDeContactCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.membru = self.membru
        self.object.save()

        messages.success(self.request, u"Am salvat persoana de contact pentru %s" % self.membru)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.membru.id}) + "#familie"

    def get_context_data(self, **kwargs):
        kwargs.update({"object": self.membru, "target_object": self.membru})
        return super(MembruPersoanaDeContactCreate, self).get_context_data(**kwargs)


class MembruPersoanaDeContactUpdate(UpdateView):
    model = PersoanaDeContact
    template_name = "structuri/membru_pdc_form.html"
    form_class = PersoanaDeContactForm

    @allow_by_afiliere([("Membru, Centru Local", "Lider")], pkname="mpk")
    def dispatch(self, request, *args, **kwargs):
        return super(MembruPersoanaDeContactUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.object.membru.id}) + "#familie"

    def get_context_data(self, **kwargs):
        kwargs.update({"object": self.object.membru, "target_object": self.object.membru})
        return super(MembruPersoanaDeContactUpdate, self).get_context_data(**kwargs)


class MembriForPatrocle(View):
    def get(self, request, *args, **kwargs):
        def get_profile_photo(m):
            if m.poza_profil:
                return m.poza_profil.get_profil_mic_url()
            return ""

        query = ""
        if "query" in request.GET and request.GET['query']:
            query = request.GET['query']

        qs = Membru.objects.filter(Q(nume__icontains=query) | Q(prenume__icontains=query) | Q(telefon__icontains=query))
        qs = qs.filter(afilieri__content_type=ContentType.objects.get_for_model(CentruLocal),
                       afilieri__object_id=self.request.user.get_profile().membru.get_centru_local().id,
                       afilieri__tip_asociere__nume__iexact=u"Membru",
                       afilieri__moment_incheiere__isnull=True).distinct()

        membri = [{"search": "%s %s<br />%s" % (m.prenume, m.nume.upper(), m.telefon),
                   "telefon": m.telefon,
                   "id": m.id,
                   "profil": get_profile_photo(m)} for m in qs]

        qs = PersoanaDeContact.objects.filter(Q(nume__icontains=query) | Q(telefon__icontains=query))
        qs = qs.filter(membru__afilieri__content_type=ContentType.objects.get_for_model(CentruLocal),
                       membru__afilieri__object_id=self.request.user.get_profile().membru.get_centru_local().id,
                       membru__afilieri__tip_asociere__nume__iexact=u"Membru",
                       membru__afilieri__moment_incheiere__isnull=True)

        contact = [{"search": "%s (%s cu %s)<br />%s" % (p.nume, p.tip_relatie.nume, p.membru, p.telefon),
                    "telefon": p.telefon,
                    "id": "%d:%d" % (p.id, p.membru.id),
                    "profil": ""} for p in qs]

        oameni = membri + contact

        return HttpResponse(simplejson.dumps(oameni))


class MembruDestinatarRepr(DetailView):
    template_name = "structuri/membru_destinatar_repr.html"
    model = Membru

    def dispatch(self, request, *args, **kwargs):
        if not "pk" in request.GET or not request.GET["pk"]:
            raise ValueError(u"'pk' GET parameter expected!")

        kwargs.update({"pk": request.GET['pk']})
        return super(MembruDestinatarRepr, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({"telefon": self.object.telefon})
        return super(MembruDestinatarRepr, self).get_context_data(**kwargs)


class PersoanaContactDestinatarRepr(DetailView):
    template_name = "structuri/persoanacontact_destinatar_repr.html"
    model = PersoanaDeContact

    def dispatch(self, request, *args, **kwargs):
        if not "pk" in request.GET or not request.GET['pk']:
            raise ValueError(u"'pk' GET parameter expected!")

        kwargs.update({"pk": request.GET['pk']})
        return super(PersoanaContactDestinatarRepr, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({"telefon": self.object.telefon})
        return super(PersoanaContactDestinatarRepr, self).get_context_data(**kwargs)


class GetSpeedList(View):
    def handler_ccl(self, request, *args, **kwargs):
        data = Membru.objects.filter(afilieri__content_type=ContentType.objects.get_for_model(CentruLocal),
                                     afilieri__object_id=request.user.get_profile().membru.centru_local.id,
                                     afilieri__confirmata=True,
                                     afilieri__moment_incheiere__isnull=True,
                                     afilieri__tip_asociere__nume__iexact=u"Membru Consiliul Centrului Local")

        def filter_mobil(info):
            if not info:
                return ""
            return "%s" % info[0].valoare.lstrip("0")

        return [[filter_mobil(m.informatie_contact("mobil")), "%s" % m.id] for m in data if
                filter_mobil(m.informatie_contact("mobil")) != ""]

    def handler_lideri(self, request, *args, **kwargs):
        data = Membru.objects.filter(afilieri__content_type=ContentType.objects.get_for_model(CentruLocal),
                                     afilieri__object_id=request.user.get_profile().membru.centru_local.id,
                                     afilieri__confirmata=True,
                                     afilieri__moment_incheiere__isnull=True,
                                     afilieri__tip_asociere__nume__icontains=u"Lider")

        def filter_mobil(info):
            if not info:
                return ""
            return "%s" % info[0].valoare.lstrip("0")

        return [[filter_mobil(m.informatie_contact("mobil")), "%s" % m.id] for m in data if
                filter_mobil(m.informatie_contact("mobil")) != ""]

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.mode = "ccl"
        if "mode" in request.GET and request.GET['mode']:
            self.mode = request.GET['mode']
        try:
            data = getattr(self, "handler_%s" % self.mode)(request, *args, **kwargs)
        except Exception, e:
            logger.debug("%s: %s \n %s" % (self.__class__.__name__, e, traceback.format_exc()))
            data = []
        return HttpResponse(simplejson.dumps(data))


class CentruLocalSeriiDocumente(ListView):
    #     model = SerieDocument
    #     template_name = "structuri/cl_serii_documente.html"
    #
    #     def dispatch(self, request, *args, **kwargs):
    #         self.centru_local = get_object_or_404(CentruLocal, id = kwargs.pop("pk"))
    #         return super(CentruLocalSeriiDocumente, self).dispatch(request, *args, **kwargs)
    #
    #     def get_queryset(self):
    #         filter_args = {"object_id" : self.centru_local.id,
    #                        "content_type" : ctype_centrulocal }
    #         qs = super(CentruLocalSeriiDocumente, self).get_queryset().filter(**filter_args)
    #         return qs.order_by("-data_inceput")
    #
    #     def get_context_data(self, **kwargs):
    #         data = super(CentruLocalSeriiDocumente, self).get_context_data(**kwargs)
    #         data.update({"centru_local" : self.centru_local})
    #         return data
    pass


class CentruLocalAdaugaSerieDocument(CreateView):
    #     model = SerieDocument
    #     template_name = "structuri/cl_serie_form.html"
    #     form_class = SerieCreateForm
    #
    #     def dispatch(self, request, *args, **kwargs):
    #         self.centru_local = get_object_or_404(CentruLocal, id = kwargs.pop("pk"))
    #         return super(CentruLocalAdaugaSerieDocument, self).dispatch(request, *args, **kwargs)
    #
    #     def get_success_url(self):
    #         return reverse("structuri:cl_serii_documente", kwargs = {"pk" : self.centru_local.id})
    #
    #     def form_valid(self, form):
    #         self.object = form.save(commit = False)
    #         self.object.object_id = self.centru_local.id
    #         self.object.content_type = ctype_centrulocal
    #         self.object.save()
    #         return HttpResponseRedirect(self.get_success_url())
    #
    #     def get_context_data(self, **kwargs):
    #         data = super(CentruLocalAdaugaSerieDocument, self).get_context_data(**kwargs)
    #         data.update({"centru_local" : self.centru_local})
    #         return data
    pass


class CentruLocalModificaSerieDocument(UpdateView):
    #     model = SerieDocument
    #     template_name = "structuri/cl_serie_form.html"
    #     form_class = SerieUpdateForm
    #
    #     def get_success_url(self):
    #         return reverse("structuri:cl_serii_documente", kwargs = {"pk" : self.centru_local.id})
    pass


class CentruLocalCuantumuriCotizatii(ListView):
    template_name = "structuri/cl_cuantumuri_cotizatie.html"

    def dispatch(self, request, *args, **kwargs):
        self.centru_local = get_object_or_404(CentruLocal, id=kwargs.pop("pk"))
        return super(CentruLocalCuantumuriCotizatii, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        from documente.models import ctype_deciziecotizatie

        filter_args = {"document_ctype": ctype_deciziecotizatie,
                       "content_type": ctype_centrulocal,
                       "object_id": self.centru_local.id}
        from documente.models import AsociereDocument

        qs = AsociereDocument.objects.prefetch_related().kwargs(**filter_args)
        qs = qs.order_by("-moment_asociere")
        return qs

    def get_context_data(self, **kwargs):
        data = super(CentruLocalCuantumuriCotizatii, self).get_context_data(**kwargs)
        data.update({"centru_local": self.centru_local})
        return data


class SetariSpecialeCentruLocal(UpdateView):
    model = CentruLocal
    template_name = "structuri/centrulocal_form.html"
    form_class = SetariSpecialeCentruLocalForm

    # TODO: add authorization
    def dispatch(self, request, *args, **kwargs):
        return super(SetariSpecialeCentruLocal, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, id=kwargs.get("pk"))
        if self.object.moment_initial_cotizatie:
            messages.warning(request, u"Nu poate fi modificată data de începere a înregistrărilor de cotizații. Dacă considerați că există un motiv legitim pentru a face asta, contactați un administrator")
            return HttpResponseRedirect(self.get_success_url())

        return super(SetariSpecialeCentruLocal, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.moment_initial_cotizatie = Trimestru.get_trimestru(year=int(form.cleaned_data['an']),
                                                                       order=int(form.cleaned_data['trimestru']))
        self.object.save()

        messages.success(self.request, u"Moment inițial cotizație salvat, %s" % self.object.moment_initial_cotizatie)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:cl_detail", kwargs={"pk": self.object.id})


class MembruConfirmaFacebook(TemplateView):
    template_name = "structuri/confirma_facebook.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MembruConfirmaFacebook, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(MembruConfirmaFacebook, self).get_context_data(**kwargs)
        data['facebook_connect_url'] = FacebookUserConnectView.get_facebook_endpoint(self.request)
        return data


class MembruDoAJAXWork(View):
    @allow_by_afiliere([("Membru, Centru Local", "Membru Consiliul Centrului Local")])
    def dispatch(self, request, *args, **kwargs):
        self.membru = get_object_or_404(Membru, id=kwargs.pop("pk"))
        return super(MembruDoAJAXWork, self).dispatch(request, *args, **kwargs)

    def do_work(self, request, *args, **kwargs):
        raise ImproperlyConfigured

    def post(self, request, *args, **kwargs):
        try:
            self.do_work(request, *args, **kwargs)
            messages.success(request, self.get_success_message())
        except Exception, e:
            messages.error(request, self.get_error_message(e))

        return HttpResponse("done")
        # return HttpResponseRedirect(reverse("structuri:membru_details", kwargs={"pk": self.membru.id}) + "#documente")


class MembruRecalculeazaAcoperire(MembruDoAJAXWork):
    def do_work(self, request, *args, **kwargs):
        return self.membru.recalculeaza_acoperire_cotizatie()

    def get_success_message(self):
        return u"Acoperirea plăților a fost recalculată cu succes"

    def get_error_message(self, e=""):
        return u"Eroare recalculare acoperire cotizație! Contactați administratorul (%s)" % e


class MembruStergeAcoperire(MembruDoAJAXWork):
    def do_work(self, request, *args, **kwargs):
        return self.membru.recalculeaza_acoperire_cotizatie(reset=True)

    def get_success_message(self):
        return u"Acoperirea plăților a fost ștearsă! Rezolvați ce aveți de rezolvat, apoi recalculați!"

    def get_error_message(self, e=""):
        return u"Eroare ștergere acoperire cotizație (%s)" % e
