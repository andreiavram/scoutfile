#coding=utf8
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from documente.forms import DeclaratieCotizatieSocialaForm, RegistruUpdateForm, RegistruCreateForm
from documente.models import DocumentCotizatieSociala, TipAsociereDocument, AsociereDocument, Registru
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
from structuri.models import Membru
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

    def form_valid(self, form):
        self.object = form.save(commit=False)

        #    verifica numarul de inregistrare (sa nu fie duplicat, pentru centrul asta local)
        #    obtine data de referinta (momentul 0)
        #    fa calculele si ataseaza plati de trimestre
        #    rescrie balanta utilizatorului
        #    salveaza (si eventual printeaza) chitanta


        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:membru_tab_documente", kwargs={"pk": self.target.id})

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

class CalculeazaAcoperireSumaJSON(View):
    pass


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
        return super(CentruLocalRegistre, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(CentruLocalRegistre, self).get_queryset()
        if not self.inactive:
            qs = qs.filter(valabil = True)
        return qs

    def get_context_data(self, **kwargs):
        data = super(CentruLocalRegistre, self).get_context_data(**kwargs)
        data.update({"centru_local" : self.centru_local, "inactive" : self.inactive})
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
