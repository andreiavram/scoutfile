# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from taggit.models import Tag
from album.models import Imagine
from album.views import FileUploadMixin
from documente.models import Document
from jocuri.forms import FisaActivitateForm, parse_string_to_seconds, DocumentActivitateForm
from jocuri.models import FisaActivitate, CategorieFiseActivitate
from structuri.models import RamuraDeVarsta
import logging

logger = logging.getLogger(__name__)


class ActivitateSearch(ListView):
    model = FisaActivitate
    template_name = "jocuri/fisaactivitate_list.html"
    form_search_params = ("query", "time", "participanti", "rdv", "categorie", "tags")

    def dispatch(self, request, *args, **kwargs):
        self.category = None
        self.tag = None

        self.requested_category_id = int(request.GET.get("cat", 0))
        if self.requested_category_id:
            self.category = get_object_or_404(CategorieFiseActivitate, id=self.requested_category_id)
        self.requested_tag_id = int(request.GET.get("tag", 0))
        if self.requested_tag_id:
            self.tag = get_object_or_404(Tag, id=self.requested_tag_id)

        return super(ActivitateSearch, self).dispatch(request, *args, **kwargs)

    def process_search_form(self, qs):
        query_data = {}
        for query_key in self.form_search_params:
            query_data[query_key] = self.request.GET.get(query_key, None)

        self.filtered = False
        if any(query_data.values()):
            self.filtered = True
        if query_data.get("query"):
            qs = qs.filter(Q(titlu__icontains=query_data.get("query")) | Q(descriere__icontains=query_data.get("query")) | Q(descriere_joc__icontains=query_data.get("query")) | Q(materiale_necesare__icontains=query_data.get("query")) | Q(obiective_educative__icontains=query_data.get("query")))
        if query_data.get("time"):
            durata_secunde = parse_string_to_seconds(query_data.get("time"))
            qs = qs.filter(Q(min_durata__isnull=True, max_durata__gte=0.9 * durata_secunde) | Q(max_durata__isnull=True, min_durata__lte=durata_secunde * 1.1) | Q(min_durata__lte = durata_secunde * 1.1, max_durata__gte = durata_secunde * 0.9))
        if query_data.get("participanti"):
            p = int(query_data.get("participanti"))
            qs = qs.filter(Q(min_participanti__isnull=True, max_participanti__gte=0.9 * p) | Q(max_participanti__isnull=True, min_participanti__lte=p * 1.1) | Q(min_participanti__lte = p * 1.1, max_participanti__gte = p * 0.9))
        if query_data.get("rdv"):
            qs = qs.filter(ramuri_de_varsta__in=[rdv for rdv in RamuraDeVarsta.objects.filter(id__in=query_data.get("rdv").split(","))]).distinct()
        if query_data.get("categorie"):
            qs = qs.filter(categorie_id=query_data.get("categorie"))
        if query_data.get("tags"):
            qs = qs.filter(tags__in=[tag for tag in Tag.objects.filter(id__in=query_data.get("tags").split(","))]).distinct()
        return qs

    def get_queryset(self):
        qs = super(ActivitateSearch, self).get_queryset()
        if self.requested_category_id:
            qs = qs.filter(categorie_id=self.requested_category_id)
        if self.requested_tag_id:
            qs = qs.filter(tags__in=[Tag.objects.get(id=self.requested_tag_id)])

        qs = self.process_search_form(qs)
        return qs

    def get_context_data(self, **kwargs):
        data = super(ActivitateSearch, self).get_context_data(**kwargs)
        data['tag'] = self.tag
        data['categorie'] = self.category
        data['categorii'] = CategorieFiseActivitate.objects.all()

        taguri = Tag.objects.all()
        taguri_relevante = []

        for tag in taguri:
            cnt = FisaActivitate.objects.filter(tags__name__in=[tag.name, ]).count()
            if cnt:
                taguri_relevante.append((tag, cnt))

        taguri_relevante.sort(key=lambda x: x[1], reverse=True)
        data['taguri'] = taguri_relevante
        data['ramuri_de_varsta'] = RamuraDeVarsta.objects.all()
        data['filtered'] = self.filtered

        return data


class ActivitateCreate(CreateView):
    model = FisaActivitate
    template_name = "jocuri/fisaactivitate_form.html"
    form_class = FisaActivitateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ActivitateCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.uploader = self.request.user
        self.object.min_durata = form.cleaned_data.get("min_durata_string", None)
        self.object.max_durata = form.cleaned_data.get("max_durata_string", None)
        self.object.save()

        try:
            self.object.editori.add(self.request.user.utilizator.membru)
        except Exception, e:
            logger.error("%s: error adding user %s to activitate, cannot fetch membru (%s)" % (self.__class__.__name__, self.request.user, e))
        return super(ActivitateCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse("jocuri:activitate_detail", kwargs={"pk": self.object.id})


class ActivitateUpdate(UpdateView):
    model = FisaActivitate
    template_name = "jocuri/fisaactivitate_form.html"
    form_class = FisaActivitateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ActivitateUpdate, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def seconds_to_shortstring(value):
        import datetime
        td = datetime.timedelta(seconds=value)
        weeks, days, hours, minutes = td.days // 7, td.days % 7, td.seconds // 3600, td.seconds // 60 % 60
        output = ""
        if weeks:
            output += u"%ds"
        if days:
            output += " " if len(output) else ""
            output += "%dz" % days
        if hours:
            output += " " if len(output) else ""
            output += "%dh" % hours
        if minutes:
            output += " " if len(output) else ""
            output += "%dm" % minutes
        return output

    def get_initial(self):
        data = super(ActivitateUpdate, self).get_initial()
        data["min_durata_string"] = self.seconds_to_shortstring(self.object.min_durata) if self.object.min_durata else None
        data["max_durata_string"] = self.seconds_to_shortstring(self.object.max_durata) if self.object.max_durata else None
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.min_durata = form.cleaned_data.get("min_durata_string", None)
        self.object.max_durata = form.cleaned_data.get("max_durata_string", None)
        try:
            editor = self.request.user.utilizator.membru
        except Exception, e:
            editor = None
            logger.error("%s: error adding user %s to activitate, cannot fetch membru (%s)" % (self.__class__.__name__, e))
        if editor not in self.object.editori.all():
            self.object.editori.add(editor)

        self.object.save()
        return super(ActivitateUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("jocuri:activitate_detail", kwargs={"pk": self.object.id})


class ActivitateDetail(DetailView):
    model = FisaActivitate
    template_name = "jocuri/fisaactivitate_detail.html"


class DocumentActivitateAdauga(FileUploadMixin, CreateView):
    model = Document
    form_class = DocumentActivitateForm
    template_name = "jocuri/documentactivitate_form.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.activitate = get_object_or_404(FisaActivitate, id=kwargs.pop("pk"))
        return super(DocumentActivitateAdauga, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.folder = self.activitate

        import os
        print "numefisier ", os.path.splitext(form.cleaned_data.get("fisier").name)
        fname, fextension = os.path.splitext(form.cleaned_data.get("fisier").name)
        fextension = fextension[1:]
        if fextension.lower() in ["jpg", "jpeg", "png", "gif"]:
            if not self.object.titlu:
                self.object.titlu = "Imagine #"
            #   delegate image safe to image object
            self.save_file(form_field_name="fisier", object_field_name="image_storage", image_class=Imagine, folder_path="jocuri", save=False)
            self.object.image_storage.title = self.object.titlu
            self.object.fisier = None
        else:
            if not self.object.titlu:
                self.object.titlu = "Document #"

        print self.object.fisier.storage.__class__.__name__
        self.object.uploader = self.request.user
        self.object.is_folder = False

        self.object.save()
        if self.object.titlu.endswith("#"):
            self.object.titlu += str(self.object.id)
            self.object.save()
        return super(DocumentActivitateAdauga, self).form_valid(form)

    def get_success_url(self):
        return reverse("jocuri:activitate_documents", kwargs={"pk": self.activitate.id})

    def get_context_data(self, **kwargs):
        data = super(DocumentActivitateAdauga, self).get_context_data(**kwargs)
        data['activitate'] = self.activitate
        return data


class DocumentActivitateList(ListView):
    model = Document
    template_name = "jocuri/documentactivitate_list.html"

    def dispatch(self, request, *args, **kwargs):
        self.activitate = get_object_or_404(FisaActivitate, id=kwargs.pop("pk"))
        return super(DocumentActivitateList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Document.objects.filter(folder=self.activitate)

    def get_context_data(self, **kwargs):
        data = super(DocumentActivitateList, self).get_context_data(**kwargs)
        data['activitate'] = self.activitate
        return data