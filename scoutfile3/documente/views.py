#coding=utf8
import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Sum
from django.db.models.query_utils import Q
from django.utils.simplejson import dumps
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.shortcuts import get_object_or_404
from documente.forms import DeclaratieCotizatieSocialaForm, RegistruUpdateForm, RegistruCreateForm, DecizieCuantumCotizatieForm, TransferIncasariForm
from documente.models import DocumentCotizatieSociala, TipAsociereDocument, AsociereDocument, Registru, REGISTRU_TIPURI, DecizieCotizatie, PlataCotizatieTrimestru, ChitantaCotizatie
from documente.models import Document
from django.core.exceptions import ImproperlyConfigured
import logging
from documente.forms import DocumentCreateForm, FolderCreateForm, \
    CotizatieMembruForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from generic.views import JSONView, ScoutFileAjaxException
from structuri.models import Membru, CentruLocal, AsociereMembruStructura
from django.contrib import messages
logger = logging.getLogger(__name__)


class DocumentFolderList(ListView):
    template_name = "documente/folder_list.html"
    model = Document

    def dispatch(self, request, *args, **kwargs):
        self.folder = None
        if kwargs.has_key("id"):
            self.folder = get_object_or_404(Document, id=kwargs.pop("id"))
            if not self.folder.is_folder:
                logger.error(u"%s: Document is not a folder" % self.__class__.__name__)
                raise ImproperlyConfigured(u"%s: Document is not a folder" % self.__class__.__name__)

        return super(DocumentFolderList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(DocumentFolderList, self).get_queryset()
        if self.folder:
            qs = qs.filter(folder=self.folder)
        else:
            qs = qs.filter(folder__isnull=True)

        return qs

    def get_context_data(self, **kwargs):
        data = super(DocumentFolderList, self).get_context_data(**kwargs)
        data.update({"folder": self.folder})


class DocumentList(ListView):
    """
    TODO: Should manage tags, searches
    """
    template_name = "documente/document_list.html"
    model = Document

    def get_queryset(self):
        return super(DocumentList, self).get_queryset().filter(is_folder=False)


class DocumentCreate(CreateView):
    model = Document
    template_name = "documente/document_form.html"
    form_class = DocumentCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.folder = get_object_or_404(Document, id=kwargs.pop("pk"))
        if not self.folder.is_folder:
            logger.error(u"%s: Document is not a folder" % self.__class__.__name__)
            raise ImproperlyConfigured(u"%s: Document is not a folder" % self.__class__.__name__)

        return super(DocumentCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.parent = self.folder
        self.object.uploader = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("documente:folder_list", kwargs={"pk": self.folder.id})


class FolderCreate(DocumentCreate):
    model = Document
    template_name = "documente/document_form.html"
    form_class = FolderCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.parent = self.folder
        self.object.uploader = self.request.user
        self.object.is_folder = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class DocumentUpdate(UpdateView):
    pass


class CotizatieMembruAdauga(CreateView):
    form_class = CotizatieMembruForm
    template_name = "documente/cotizatie_form.html"

    def dispatch(self, request, *args, **kwargs):
        from structuri.models import Membru

        self.target = get_object_or_404(Membru, id=kwargs.pop("pk"))
        return super(CotizatieMembruAdauga, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        data = super(CotizatieMembruAdauga, self).get_form_kwargs()
        data.update({"centru_local" : self.target.centru_local,
                     "membru" : self.target})
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.casier = self.request.user.get_profile().membru
        self.object.uploader = self.request.user
        self.object.data_inregistrare = datetime.date.today()
        self.object.titlu = u"Chitanță cotizație pentru %s" % self.target
        self.object.save()

        #   ataseaza platitorul ca asociere /
        AsociereDocument.inregistreaza(document=self.object,
                                       to=self.target,
                                       tip="platitor",
                                       responsabil=self.object.casier.user)

        #   stabileste si salveaza acoperirea
        plati, rest, status, diff  = PlataCotizatieTrimestru.calculeaza_acoperire(membru=self.target,
                                                     chitanta=self.object,
                                                     commit=True)

        msg_data = (self.object.suma, self.target, plati[-1].trimestru, u" - parțial" if (plati[-1].partial and not plati[-1].final) else "")
        mesaj = u"Am înregistrat plata a %.2f RON pentru %s (acoperă trimestrul %s%s)" % msg_data
        messages.success(self.request, mesaj)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.target.id}) + "#documente"

    def get_context_data(self, **kwargs):
        kwargs.update({"object": self.target})
        return kwargs


#class NumarInregistrareUrmatorJSON(View):
#    @csrf_exempt
#    def dispatch(self, request, *args, **kwargs):
#        return super(NumarInregistrareUrmatorJSON, self).dispatch(request, *args, **kwargs)
#
#    def post(self, request, *args, **kwargs):
#        centru_local = request.user.get_profile().membru.centru_local
#        from django.contrib.contenttypes.models import ContentType
#
#        filter_kwargs = {"content_type": ContentType.objects.get_for_model(centru_local),
#                         "object_id": centru_local.id,
#                         "deschisa": True}
#        serii_disponibile = SerieDocument.objects.filter(**filter_kwargs).order_by("-document_referinta__date_created")
#        if serii_disponibile.count() != 0:
#            try:
#                numar_inregistrare = serii_disponibile[0].get_next_item()
#            except ValueError:
#                numar_inregistrare = None
#            serie = serii_disponibile[0].cod_unic
#
#        json_output = {'result': (serii_disponibile.count() > 0) and (numar_inregistrare != None),
#                       'numar_inregistrare': numar_inregistrare,
#                       'serie': serie}
#
#        return HttpResponse(simplejson.dumps(json_output))


class CuantumuriCotizatieNational(ListView):
    #TODO: implement this
    pass


class CuantumCotizatieNationalAdauga(CreateView):
    #TODO: implement this
    pass


class DeclaratieCotizatieSocialaAdauga(CreateView):
    form_class = DeclaratieCotizatieSocialaForm
    template_name = "documente/declaratie_cotizatie_sociala.html"
    model = DocumentCotizatieSociala

    def dispatch(self, request, *args, **kwargs):
        self.target = get_object_or_404(Membru, id=kwargs.pop("pk"))
        return super(DeclaratieCotizatieSocialaAdauga, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.titlu = u"Declarație proprie răspundere cotizație socială"
        self.object.uploader = self.request.user
        self.object.save()

        responsabil = self.target.centru_local.ocupant_functie(u"Secretar Centru Local")
        #   adauga asociere document
        AsociereDocument.inregistreaza(document=self.object,
                                       to=self.target,
                                       tip="beneficiar-cotizatie-sociala",
                                       responsabil=responsabil.user)

        messages.success(self.request, u"Declarație salvată")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk":self.target.id}) + "#documente"

    def get_context_data(self, **kwargs):
        data = super(DeclaratieCotizatieSocialaAdauga, self).get_context_data(**kwargs)
        data.update({"membru" : self.target})
        return data

class DeclaratieCotizatieSocialaModifica(UpdateView):
    template_name = "documente/declaratie_cotizatie_sociala.html"
    model = DocumentCotizatieSociala
    form_class = DeclaratieCotizatieSocialaForm

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, id = kwargs.get("pk"))
        asocieri = AsociereDocument.objects.filter(document=self.object, tip_asociere__slug="beneficiar-cotizatie-sociala")
        if asocieri.count():
            self.target = asocieri[0].content_object

        return super(DeclaratieCotizatieSocialaModifica, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=True)

        messages.success(self.request, u"Declarație salvată")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        data = super(DeclaratieCotizatieSocialaModifica, self).get_context_data(**kwargs)
        data.update({"membru" : self.target})
        return data

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk":self.target.id}) + "#documente"


class MembruAlteDocumente(TemplateView):
    template_name = "documente/membru_adauga_documente.html"

    def dispatch(self, request, *args, **kwargs):
        self.membru = get_object_or_404(Membru, id=kwargs.pop("pk"))
        return super(MembruAlteDocumente, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {"object" : self.membru}

class CentruLocalRegistre(ListView):
    template_name = "documente/registru_list.html"
    model = Registru

    # TODO: add permissions check for this
    def dispatch(self, request, *args, **kwargs):
        from structuri.models import CentruLocal
        self.centru_local = get_object_or_404(CentruLocal, id=kwargs.get("pk"))
        self.inactive = False
        if "inactive" in request.GET:
            self.inactive = False if request.GET['inactive'] == "off" else True
        self.tip = None
        if "tip" in request.GET and request.GET['tip'] in [a[0] for a in REGISTRU_TIPURI]:
            self.tip = request.GET['tip']
        return super(CentruLocalRegistre, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(CentruLocalRegistre, self).get_queryset()
        if not self.inactive:
            qs = qs.filter(valabil = True)
        if self.tip:
            qs = qs.filter(tip_registru = self.tip)
        return qs

    def get_context_data(self, **kwargs):
        data = super(CentruLocalRegistre, self).get_context_data(**kwargs)
        data.update({"centru_local" : self.centru_local, "inactive" : self.inactive, "tipuri_registre" : REGISTRU_TIPURI})
        return data

class RegistruCreate(CreateView):
    template_name = "documente/registru_form.html"
    model = Registru
    form_class = RegistruCreateForm

    # TODO: add permissions check for this
    def dispatch(self, request, *args, **kwargs):
        from structuri.models import CentruLocal
        self.centru_local = get_object_or_404(CentruLocal, id=kwargs.get("pk"))
        return super(RegistruCreate, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        current = super(RegistruCreate, self).get_form_kwargs()
        current.update({"centru_local" : self.centru_local})
        return current

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.centru_local = self.centru_local
        self.object.owner = self.request.user.get_profile().membru
        self.object.save()

        messages.success(self.request, u"%s creat cu succes" % self.object.get_tip_registru_display())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("documente:registru_detail", kwargs={"pk" : self.object.id})

    def get_context_data(self, **kwargs):
        data = super(RegistruCreate, self).get_context_data(**kwargs)
        data.update({"centru_local" : self.centru_local})
        return data

class RegistruUpdate(UpdateView):
    template_name = "documente/registru_form.html"
    model = Registru
    form_class = RegistruUpdateForm

    # TODO: add permissions check for this
    def dispatch(self, request, *args, **kwargs):
        return super(RegistruUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(RegistruUpdate, self).get_context_data(**kwargs)
        data.update({"centru_local" : self.object.centru_local})
        return data

    def form_valid(self, form):
        messages.success(self.request, u"Registru actualizat cu succes")
        return super(RegistruUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("documente:registru_detail", kwargs={"pk" : self.object.id})

class RegistruDetail(DetailView):
    template_name = "documente/registru_detail.html"
    model = Registru

    # TODO: add permissions check for this
    def dispatch(self, request, *args, **kwargs):
        return super(RegistruDetail, self).dispatch(request, *args, **kwargs)

class SelectieAdaugareDocument(TemplateView):
    template_name = "documente/centru_local_adauga_documente.html"

    # TODO: add permission check for this
    def dispatch(self, request, *args, **kwargs):
        from structuri.models import CentruLocal
        self.centru_local = get_object_or_404(CentruLocal, id=kwargs.pop("pk"))
        return super(SelectieAdaugareDocument, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(SelectieAdaugareDocument, self).get_context_data(**kwargs)
        data.update({"centru_local" : self.centru_local})
        return data

class DecizieCuantumAdauga(CreateView):
    model = DecizieCotizatie
    form_class = DecizieCuantumCotizatieForm
    template_name = "documente/decizie_cuantum_cotizatie_form.html"

    # TODO: add permission checks for this
    def dispatch(self, request, *args, **kwargs):
        from structuri.models import CentruLocal
        self.centru_local = get_object_or_404(CentruLocal, id=kwargs.pop("pk"))
        return super(DecizieCuantumAdauga, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        data = super(DecizieCuantumAdauga, self).get_form_kwargs(**kwargs)
        data.update({"centru_local" : self.centru_local})
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.centru_local = self.centru_local
        self.object.uploader = self.request.user
        self.object.titlu = u"Decizie cuantum cotizatie %s" % self.object.get_categorie_display()
        self.object.data_inregistrare = datetime.date.today()

        decizie_filter = {"centru_local" : self.centru_local,
                          "categorie" : form.cleaned_data['categorie'],
                          "data_sfarsit__isnull" : True}
        decizii_existente = DecizieCotizatie.objects.filter(**decizie_filter)
        if decizii_existente.count():
            decizie_to_close = decizii_existente[0]
            decizie_to_close.data_sfarsit = self.object.data_inceput - datetime.timedelta(days = 1)
            decizie_to_close.save()

        self.object.save()

        messages.success(self.request, u"Decizia a fost înregistrată")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("documente:registru_detail", kwargs={"pk" : self.object.registru.id})

    def get_context_data(self, **kwargs):
        data = super(DecizieCuantumAdauga, self).get_context_data(**kwargs)
        data.update({"centru_local" : self.centru_local})
        return data

#class DecizieCuantumEdit(UpdateView):
#    model = DecizieCotizatie
#    form_class = DecizieCuantumCotizatieUpdateForm
#    template_name = "documente/decizie_cuantum_cotizatie_form.html"
#
#    # TODO: add permission checks for this
#    def dispatch(self, request, *args, **kwargs):
#        return super(DecizieCuantumEdit, self).dispatch(request, *args, **kwargs)
#
#    def get_success_url(self):
#        return reverse("documente:registru_detail", kwargs={"pk" : self.object.registru.id})


class DecizieCuantumDetail(DetailView):
    model = DecizieCotizatie
    template_name = "documente/decizie_cuantum_cotizatie_detail.html"

    # TODO: add permission checks for this
    def dispatch(self, request, *args, **kwargs):
        return super(DecizieCuantumDetail, self).dispatch(request, *args, **kwargs)


class CalculeazaAcoperireCotizatie(JSONView):
    _params = {"membru" : {"type" : "required"},
               "suma" : {"type" : "required"}}

    def clean_membru(self, value):
        try:
            return Membru.objects.get(id = value)
        except Membru.DoesNotExist, e:
            raise ScoutFileAjaxException(exception = e)
        return None

    def clean_suma(self, value):
        return float(value)

    def get(self, request, *args, **kwargs):
        self.validate(**self.parse_json_data())

        plati, rest, status_text, diff  = PlataCotizatieTrimestru.calculeaza_acoperire(membru=self.cleaned_data['membru'],
                                                     suma=self.cleaned_data['suma'])

        return HttpResponse(self.construct_json_response(plati=plati,
                                                         suma=rest,
                                                         status_text=status_text,
                                                         diff=diff))

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def plati_to_json(self, plati):
        return [p.__json__() for p in plati]

    def construct_json_response(self, plati=None, **kwargs):
        json = {"plati" : self.plati_to_json(plati),
                "suma" : self.cleaned_data['suma'],
                "rest" : kwargs.get("suma", 0),
                "status" : kwargs.get("status_text", None),
                "diff" : kwargs.get("diff", None)}
        return dumps(json)

class CasieriMixin(object):
    def get_casieri(self, centru_local):
        casieri = ChitantaCotizatie.objects.filter(registru__centru_local = centru_local).distinct().values_list("casier", flat=True)
        return Membru.objects.filter(id__in = casieri)

class CotizatiiCentruLocal(ListView, CasieriMixin):
    template_name = "documente/cotizatii_list.html"
    model = ChitantaCotizatie

    # TODO: add permissions check
    def dispatch(self, request, *args, **kwargs):
        self.centru_local = get_object_or_404(CentruLocal, id = kwargs.pop("pk"))
        return super(CotizatiiCentruLocal, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        #membrii = self.centru_local.cercetasi(qs=True).values_list("membru_id", flat=True)
        return self.model.objects.filter(registru__centru_local = self.centru_local).order_by("-data_inregistrare")

    def get_context_data(self, **kwargs):
        data = super(CotizatiiCentruLocal, self).get_context_data(**kwargs)
        data.update({"centru_local" : self.centru_local, "casieri" : self.get_casieri(self.centru_local)})
        return data

class CotizatiiLider(ListView, CasieriMixin):
    template_name = "documente/cotizatii_list.html"
    model = ChitantaCotizatie

    def dispatch(self, request, *args, **kwargs):
        self.lider = get_object_or_404(Membru, id = kwargs.pop("pk"))
        return super(CotizatiiLider, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(casier = self.lider)

    def get_suma_lider(self):
        search = dict(casier=self.lider,
                      registru__centru_local=self.lider.centru_local,
                      predat=False)
        return self.model.objects.filter(**search).aggregate(Sum("suma"))['suma__sum']

    def get_context_data(self, **kwargs):
        data = super(CotizatiiLider, self).get_context_data(**kwargs)
        data.update({"lider" : self.lider, "centru_local" : self.lider.centru_local,
                     "casieri" : self.get_casieri(centru_local=self.lider.centru_local),
                     "suma_casa" : self.get_suma_lider(), "trezorier" : self.lider.centru_local.ocupant_functie(u"Trezorier Centru Local")})
        return data

class PreiaIncasariCasier(FormView):
    form_class = TransferIncasariForm
    template_name = "documente/transfer_incasari.html"

    # TODO: adauga verificare permisiuni
    def dispatch(self, request, *args, **kwargs):
        self.lider = get_object_or_404(Membru, id=kwargs.pop("pk"))
        return super(PreiaIncasariCasier, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        plati = form.cleaned_data['plati']
        suma = 0
        for p in plati:
            p.predat = True
            suma += p.suma
            p.save()

        messages.success(self.request, u"Am transferat %.2f RON de la %s la trezorier" % (suma, self.lider))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("documente:cotizatii_centru_local", kwargs={"pk" : self.request.user.get_profile().membru.centru_local.id})

    def get_form_kwargs(self):
        data = super(PreiaIncasariCasier, self).get_form_kwargs()
        data.update({"centru_local" : self.request.user.get_profile().membru.centru_local})
        return data

    def get_context_data(self, **kwargs):
        data = super(PreiaIncasariCasier, self).get_context_data(**kwargs)
        plati = ChitantaCotizatie.objects.filter(registru__centru_local = self.lider.centru_local,
                                                 casier = self.lider,
                                                 predat = False)
        data.update({"plati" : plati,
                     "trezorier" : self.request.user.get_profile().membru.are_calitate("Trezorier Centru Local", self.lider.centru_local),
                     "lider" : self.lider,
                     "suma" : plati.aggregate(Sum("suma"))['suma__sum']})
        return data