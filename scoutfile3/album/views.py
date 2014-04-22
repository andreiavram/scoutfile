# coding: utf-8
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.utils.simplejson import dumps
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import View, TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect, HttpResponse, \
    HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest
from django.core.urlresolvers import reverse
import datetime
from django.contrib import messages
from django.views.generic.list import ListView
import simplejson
import logging
import os
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from taggit.utils import parse_tags

from album.models import Eveniment, ZiEveniment, Imagine, FlagReport, RaportEveniment, ParticipantiEveniment, \
    ParticipareEveniment, AsociereEvenimentStructura, TipEveniment, STATUS_EVENIMENT
from album.forms import ReportForm, EvenimentCreateForm, EvenimentUpdateForm, PozaTagsForm, ZiForm, RaportEvenimentForm, \
    EvenimentParticipareForm
from album.models import SetPoze
from album.forms import SetPozeCreateForm, SetPozeUpdateForm
from goodies.views import GenericDeleteView, CalendarViewMixin
from settings import MEDIA_ROOT
from structuri.forms import AsociereEvenimentStructuraForm
from structuri.models import Membru, RamuraDeVarsta, CentruLocal, Unitate
from goodies.views import JSONView
from generic.views import ScoutFileAjaxException
from album.models import IMAGINE_PUBLISHED_STATUS
from structuri.models import TipAsociereMembruStructura
from structuri.decorators import allow_by_afiliere
import settings

logger = logging.getLogger(__name__)


class EvenimentFiltruMixin(object):
    def process_request_filters(self, request):
        if not request.is_ajax():
            if "qnume" in request.GET:
                request.session['qnume'] = request.GET['qnume']
            elif "qnume" in request.session:
                del request.session['qnume']


        if "status" not in request.session:
            request.session["status"] = "terminat"
        if "status" in request.GET:
            request.session["status"] = request.GET.get("status")

        if "unitate" in request.GET:
            if request.GET.get("unitate") == "0" and "unitate" in request.session:
                del request.session['unitate']
            else:
                request.session['unitate'] = int(request.GET.get("unitate"))

        self.unitate = None
        if "unitate" in request.session and request.session['unitate'] != 0:
            self.unitate = Unitate.objects.get(id=request.session['unitate'])

        if "view" not in request.session:
            request.session["view"] = "list_detail"
        if "view" in request.GET:
            request.session["view"] = request.GET.get("view")

        if "tip" in request.GET:
            if request.GET.get("tip") == "0" and "tip" in request.session:
                del request.session["tip"]
            else:
                request.session["tip"] = int(request.GET.get("tip"))

        self.tip_activitate = None
        if "tip" in request.session and request.session["tip"] != 0:
            self.tip_activitate = TipEveniment.objects.get(id=request.session["tip"])

        if "album" not in request.session:
            request.session["album"] = False
        if "album" in request.GET:
            request.session["album"] = int(request.GET.get("album")) > 0

        if "an" not in request.session:
            request.session["an"] = 0
        if "an" in request.GET:
            request.session["an"] = int(request.GET.get("an"))

    def filters_context_data(self):
        data = {}
        if self.request.user.is_authenticated():
            centru_local = self.request.user.get_profile().membru.centru_local
            data['unitati'] = centru_local.unitate_set.all()
        data['tipuri_activitate'] = [t for t in TipEveniment.objects.all() if t.eveniment_set.count() > 0]
        data['status_activitate'] = STATUS_EVENIMENT
        data['tip_activitate'] = self.tip_activitate
        data['unitate'] = self.unitate
        status = "Toate"
        for s in STATUS_EVENIMENT:
            if s[0] == self.request.session["status"]:
                status = s[1]
                break

        data['status'] = status

        return data

    def apply_filters(self, qs):
        if self.unitate:
            qs = qs.filter(id__in=[e.id for e in qs if e.are_asociere(self.unitate)])

        if self.request.session["status"] != "toate":
            qs = qs.filter(status=self.request.session["status"])

        if self.tip_activitate:
            qs = qs.filter(tip_eveniment=self.tip_activitate)

        if self.request.session["album"]:
            qs = qs.filter(id__in=[e.id for e in qs if e.total_poze > 0])

        if self.request.session["an"] > 0:
            qs = qs.filter(start_date__year=self.request.session["an"])

        return qs


class EvenimentList(EvenimentFiltruMixin, ListView):
    model = Eveniment
    template_name = "album/eveniment_list.html"

    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            self.per_page = int(request.POST.get("per_page", 5))
            self.offset = int(request.POST.get("offset", 0))

        self.process_request_filters(request)
        return super(EvenimentList, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(EvenimentList, self).get_queryset(*args, **kwargs)
        if self.request.user.is_authenticated():
            qs = qs.filter(centru_local=self.request.user.get_profile().membru.centru_local)

        if "qnume" in self.request.session:
            qs = qs.filter(nume__icontains=self.request.session['qnume'])

        qs = self.apply_filters(qs)

        if self.request.is_ajax():
            self.total_count = qs.count()
            qs = qs[self.offset:self.offset + self.per_page]
            self.current_count = qs.count()

        return qs

    def get_template_names(self):
        if self.request.is_ajax():
            return "album/json/eveniment_list.json"
        return self.template_name

    def get_context_data(self, **kwargs):
        data = super(EvenimentList, self).get_context_data(**kwargs)

        if self.request.is_ajax():
            data['total_count'] = self.total_count
            data['current_count'] = self.current_count
            data['requested_count'] = self.per_page
            data['current_offset'] = self.offset

        an_curent = datetime.datetime.now().year
        data['ani_activitati'] = range(an_curent - 2, an_curent + 1)
        data['ani_activitati'].reverse()
        data.update(self.filters_context_data())

        return data


class AlbumEvenimentDetail(DetailView):
    model = Eveniment
    template_name = "album/eveniment_album.html"

    def dispatch(self, request, *args, **kwargs):
        self.autor = request.GET['autor'] if "autor" in request.GET else None
        return super(AlbumEvenimentDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        current = super(AlbumEvenimentDetail, self).get_context_data(*args, **kwargs)

        zile = []
        for zi_eveniment in self.object.zieveniment_set.all().order_by("index", "date"):
            zile.append((zi_eveniment, zi_eveniment.filter_photos(autor=self.autor, user=self.request.user)))

        current.update({"zile": zile, "autor": self.autor})

        return current


class EvenimentStats(DetailView):
    model = Eveniment
    template_name = "album/eveniment_stats.html"

    def get_context_data(self, *args, **kwargs):
        current = super(EvenimentStats, self).get_context_data(*args, **kwargs)
        return current


class ZiDetail(DetailView):
    model = ZiEveniment
    template_name = "album/zi_detail.html"

    def dispatch(self, request, *args, **kwargs):
        if request.GET.has_key("autor"):
            self.autor = request.GET['autor']
        else:
            self.autor = None
        return super(ZiDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        current = super(ZiDetail, self).get_context_data(*args, **kwargs)

        object_list = self.object.filter_photos(autor=self.autor, user=self.request.user)
        current.update({"object_list": object_list, "autor": self.autor,
                        "visibility_states": IMAGINE_PUBLISHED_STATUS})

        centru_local = self.object.eveniment.centru_local
        calitate = TipAsociereMembruStructura.objects.get(nume__iexact=u"Păstrător al amintirilor", content_types__in=[
            ContentType.objects.get_for_model(centru_local)])
        if self.request.user.is_authenticated() and (self.request.user.get_profile().membru.are_calitate(calitate,
                                                                                                         centru_local) or self.request.user.is_superuser):
            current.update({"media_manager": True})

        return current


class ZiEdit(UpdateView):
    model = ZiEveniment
    template_name = "album/zi_form.html"
    form_class = ZiForm

    def dispatch(self, request, *args, **kwargs):
        return super(ZiEdit, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("album:zi_detail", kwargs={"pk": self.object.id})


class ZiStats(DetailView):
    model = ZiEveniment
    template_name = "album/zi_stats.html"


class PozaDetail(DetailView):
    model = Imagine
    template_name = "album/poza_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.autor = None
        if request.GET.has_key("autor"):
            self.autor = request.GET['autor']

        self.object = get_object_or_404(Imagine, id=kwargs.get("pk"))
        if self.object.published_status < self.object.set_poze.eveniment.get_visibility_level(user=request.user):
            return HttpResponseForbidden()

        return super(PozaDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        current = super(PozaDetail, self).get_context_data(*args, **kwargs)

        import random

        current.update({"random_value": random.randrange(1000, 2000)})
        current.update({"next_photo": self.object.get_next_photo(autor=self.autor, user=self.request.user),
                        "prev_photo": self.object.get_prev_photo(autor=self.autor, user=self.request.user)})
        current.update({"autor": self.autor})

        backward_limit = datetime.datetime.combine(self.object.get_day().date,
                                                   datetime.time(0, 0, 0)) + datetime.timedelta(hours=3)
        photo = Imagine.objects.filter(set_poze__eveniment=self.object.set_poze.eveniment, data__lt=self.object.data,
                                       data__gte=backward_limit)
        if self.autor is not None:
            photo = photo.filter(set_poze__autor__icontains=self.autor)

        zi_page = ((photo.count()) / 30) + 1
        current.update({"zi_page": zi_page})
        current.update({"visibility_states": IMAGINE_PUBLISHED_STATUS})

        centru_local = self.object.set_poze.eveniment.centru_local
        calitate = TipAsociereMembruStructura.objects.get(nume__iexact=u"Păstrător al amintirilor", content_types__in=[
            ContentType.objects.get_for_model(centru_local)])
        if self.request.user.is_authenticated() and (self.request.user.get_profile().membru.are_calitate(calitate,
                                                                                                         centru_local) or self.request.user.is_superuser):
            current.update({"media_manager": True})

        return current


class PozaUpdate(UpdateView):
    model = Imagine
    template_name = "album/poza_form.html"
    form_class = PozaTagsForm

    @allow_by_afiliere([("Imagine, Centru Local", u"Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(PozaUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.tags.clear()
        messages.success(self.request, u"Modificări salvate")
        return super(PozaUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("album:poza_detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        current = super(PozaUpdate, self).get_context_data(**kwargs)

        centru_local = self.object.set_poze.eveniment.centru_local
        calitate = TipAsociereMembruStructura.objects.get(nume__iexact=u"Păstrător al amintirilor", content_types__in=[
            ContentType.objects.get_for_model(centru_local)])
        if self.request.user.get_profile().membru.are_calitate(calitate, centru_local):
            current.update({"media_manager": True})

        return current


class PozaDelete(GenericDeleteView):
    model = Imagine
    template_name = "album/poza_form.html"

    @allow_by_afiliere([("Imagine, Centru Local", u"Păstrător al amintirilor")])
    def dispatch(self, request, *args, **kwargs):
        return super(PozaDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("album:eveniment_detail", kwargs={"slug": self.object.set_poze.eveniment.slug})


class FlagImage(CreateView):
    model = FlagReport
    template_name = "album/poza_flag.html"
    form_class = ReportForm

    def dispatch(self, *args, **kwargs):
        self.poza = get_object_or_404(Imagine, id=kwargs.pop("pk"))
        return super(FlagImage, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.imagine = self.poza
        self.object.save()
        messages.success(self.request,
                         "Poza a fost flag-uită, un lider sau fotograful vor decide ce acțiune se va lua în continuare")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:poza_detail", kwargs={"pk": self.poza.id})

    def get_context_data(self, *args, **kwargs):
        current = super(FlagImage, self).get_context_data(*args, **kwargs)

        current.update({"poza": self.poza})

        return current


class RotateImage(View):
    @allow_by_afiliere([("Imagine, Centru Local", u"Păstrător al amintirilor")])
    def dispatch(self, request, *args, **kwargs):
        self.imagine = get_object_or_404(Imagine, id=kwargs.pop("pk"))

        if "direction" not in request.GET:
            raise Http404()

        self.direction = request.GET.get("direction", "cw")
        if self.direction not in ("cw", "ccw"):
            return HttpResponseBadRequest()

        return super(RotateImage, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.imagine.rotate(self.direction)

        if "size" in request.GET:
            data = getattr(self.imagine, "get_%s_url" % request.GET['size'])()
            return HttpResponse(data)
        return HttpResponseRedirect(reverse("album:poza_detail", kwargs={"pk": self.imagine.id}))


class SetImaginiUpload(CreateView):
    model = SetPoze
    form_class = SetPozeCreateForm
    template_name = "album/create_set_imagini.html"

    def response_mimetype(self):
        if "application/json" in self.request.META['HTTP_ACCEPT']:
            return "application/json"
        else:
            return "text/plain"

    def handle_zip_upload(self, f, byte_ranges):
        local_file_name = self.object.zip_file

        import io

        if not os.path.exists(local_file_name):
            # create empty file with given size
            with io.open(local_file_name, "w+b") as fp:
                fp.seek(int(byte_ranges[2]) - 1)
                fp.write("\0")

        with io.open(local_file_name, "a+b") as destination:
            destination.seek(int(byte_ranges[0]))
            for chunk in f.chunks():
                destination.write(chunk)

    @allow_by_afiliere([("Eveniment, Centru Local", "Lider")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.get("slug"))
        return super(SetImaginiUpload, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        #   Cleanup residual uploads here
        for key in request.session.keys():
            if len(key.split("-")) > 1 and key.split("-")[0] == request.user.id:
                del request.session[key]

        return super(SetImaginiUpload, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        logger.debug("%s - form valid" % self.__class__.__name__)

        import re

        byte_ranges = re.findall(r"bytes (\d+)-(\d+)/(\d+)", self.request.META['HTTP_CONTENT_RANGE'])
        logger.debug("%s - byte ranges %s to %s out of %s" % (
        self.__class__.__name__, byte_ranges[0][0], byte_ranges[0][1], byte_ranges[0][2]))
        f = self.request.FILES.get('zip_file')

        session_key = "{0}-{1}".format(self.request.user.id, f.name.replace("-", "+"))
        if session_key in self.request.session:
            self.object = get_object_or_404(self.model, id=int(self.request.session[session_key]))
            logger.debug("%s - retrieving existing set (%d)" % (self.__class__.__name__, self.object.id))
        else:
            self.object = form.save(commit=False)
            from structuri.models import Membru

            self.object.autor_user = Membru.objects.get(id=self.request.user.get_profile().id)

            if not self.object.autor:
                self.object.autor = "%s" % self.object.autor_user.nume_complet()

            self.object.eveniment = self.eveniment
            self.object.zip_file = "/" + os.path.join("tmp", "{0}_{1}_{2}".format(self.request.user.id,
                                                                                  datetime.datetime.now().strftime(
                                                                                      "%Y%m%d%H%M%S"), f.name))
            self.object.save()

            self.request.session[session_key] = self.object.id
            logger.debug("%s - no match on session_key, creating new object with file data" % (self.__class__.__name__))

        self.handle_zip_upload(f, byte_ranges[0])

        #   if this is the last chunk, update set info
        if int(byte_ranges[0][1]) == int(byte_ranges[0][2]) - 1:
            self.object.status = 1
            self.object.save()
            logger.debug("%s - removing session key from session dict" % self.__class__.__name__)
            del self.request.session[session_key]

        data = {"files": [{'name': f.name,
                           #'url': self.object.zip_file.url,
                           #'thumbnail_url': STATIC_URL + "album/zip.png",
                           'size': int(byte_ranges[0][2]),
                           'type': "application/zip",
                           #'descriere' : self.object.descriere,
                           'delete_url': settings.URL_ROOT + reverse("album:set_poze_delete_ajax",
                                                                     kwargs={"pk": self.object.id}),
                           'delete_type': "DELETE"}]}

        response = HttpResponse(simplejson.dumps(data), mimetype=self.response_mimetype())
        return response

    def form_invalid(self, form):
        logger.debug("%s - form invalid (%s)" % (self.__class__.__name__, form.errors))
        logger.debug("%s - POST data (%s)" % (self.__class__.__name__, self.request.POST))
        #         data = [{"error" : u"Cannot upload", "error_dict" : form.errors}]

        f = self.request.FILES.get('zip_file')
        data = {"files": [{"name": f.name, "error": u"Cannot upload"}]}

        response = HttpResponse(simplejson.dumps(data), mimetype=self.response_mimetype())
        return response

    def get_context_data(self, **kwargs):
        current = super(SetImaginiUpload, self).get_context_data(**kwargs)
        current.update({"eveniment": self.eveniment})
        return current


class SetImaginiDeleteAjax(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.set_poze = get_object_or_404(SetPoze, id=kwargs.pop("pk"))
        return super(SetImaginiDeleteAjax, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        from structuri.models import Membru

        logger.debug("%s: user is superuser: %s, user is same membru object %s" % (
        self.__class__.__name__, request.user.is_superuser,
        Membru.objects.get(id=request.user.get_profile().id) == self.set_poze.autor_user))
        if request.user.is_superuser or Membru.objects.get(
                id=request.user.get_profile().id) == self.set_poze.autor_user:
            try:
                os.unlink(self.set_poze.zip_file)
            except Exception, e:
                logger.info("%s - could not delete file, file does not exit" % self.__class__.__name__)
            self.set_poze.delete()
        else:
            return HttpResponseForbidden()

        return HttpResponse("")


class SetImaginiToate(ListView):
    model = SetPoze
    template_name = "album/set_poze_list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.membru = request.user.get_profile().membru
        return super(SetImaginiToate, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(eveniment__centru_local=self.membru.centru_local)

    def get_context_data(self, **kwargs):
        current = super(SetImaginiToate, self).get_context_data(**kwargs)
        current.update(
            {"media_manager": self.membru.are_calitate(u"Păstrător al amintirilor", self.membru.centru_local)})
        return current


class SetImaginiUser(SetImaginiToate):
    def get_queryset(self):
        qs = super(SetImaginiUser, self).get_queryset()
        qs = qs.filter(autor_user=Membru.objects.get(id=self.request.user.get_profile().id))
        return qs

    def get_context_data(self, **kwargs):
        current = super(SetImaginiUser, self).get_context_data(**kwargs)
        current.update({"user_only": True})
        return current


class EvenimentSeturi(SetImaginiToate):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.get("slug"))
        return super(EvenimentSeturi, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(EvenimentSeturi, self).get_queryset()
        qs = qs.filter(eveniment=self.eveniment)
        return qs

    def get_context_data(self, **kwargs):
        current = super(EvenimentSeturi, self).get_context_data(**kwargs)
        current.update({"eveniment": self.eveniment})
        return current


class EvenimentSeturiUser(EvenimentSeturi):
    def get_queryset(self):
        qs = super(EvenimentSeturiUser, self).get_queryset()
        qs = qs.filter(autor_user=Membru.objects.get(id=self.request.user.get_profile().id))
        return qs

    def get_context_data(self, **kwargs):
        current = super(SetImaginiUser, self).get_context_data(**kwargs)
        current.update({"user_only": True})
        return current


class SetPozeUpdate(UpdateView):
    model = SetPoze
    form_class = SetPozeUpdateForm
    template_name = "album/set_poze_edit.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, id=kwargs.get("pk"))
        if self.object.autor_user_id != request.user.get_profile().id:
            return HttpResponseNotAllowed()
        return super(SetPozeUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        offset_initial = self.object.offset_secunde
        self.object = form.save(commit=True)
        if offset_initial != self.object.offset_secunde:
            self.object.offset_changed = True
            self.object.save()

        messages.success(self.request, "Actualizări salvate!")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:set_poze_edit", kwargs={"pk": self.object.id})


class ChangeImagineVisibility(JSONView):
    _params = {"imagine": {"type": "required"},
               "new_status": {"type": "required"}}

    def clean_imagine(self, value):
        try:
            return Imagine.objects.get(id=int(value))
        except Exception, e:
            raise ScoutFileAjaxException(extra_message="This image does not exist", exception=e)

    def clean_new_status(self, value):
        #TODO: change this from range to actual valid values
        if int(value) not in range(1, 5):
            raise ScoutFileAjaxException(extra_message="The status is invalid")
        return int(value)

    def post(self, request, *args, **kwargs):
        self.validate(**self.parse_json_data())

        centru_local = self.cleaned_data['imagine'].set_poze.eveniment.centru_local
        calitate = TipAsociereMembruStructura.objects.get(nume__iexact=u"Păstrător al amintirilor", content_types__in=[
            ContentType.objects.get_for_model(centru_local)])
        if not self.request.user.get_profile().membru.are_calitate(calitate,
                                                                   centru_local) and not self.request.user.is_superuser:
            return HttpResponseForbidden()

        self.cleaned_data['imagine'].published_status = self.cleaned_data['new_status']
        self.cleaned_data['imagine'].save()

        return HttpResponse(self.construct_json_response(result=True, imagine=self.cleaned_data['imagine']))

    def construct_json_response(self, **kwargs):
        json_dict = {"result": kwargs.get("result", False),
                     "new_status_string": kwargs.get("imagine").get_published_status_display()}
        return simplejson.dumps(json_dict)


class EvenimentEditMixin(object):
    participanti = ["lupisori", "temerari", "seniori", "exploratori", "adulti", "lideri"]

    def update_counts(self, form):
        counts = ParticipantiEveniment.objects.filter(eveniment=self.object)

        participanti = self.participanti[:]
        for c in counts:
            key = None
            if c.ramura_de_varsta is not None and c.ramura_de_varsta.slug in participanti:
                key = c.ramura_de_varsta.slug
            elif c.alta_categorie is not None and c.alta_categorie in participanti:
                key = c.alta_categorie

            if key and key in form.cleaned_data:
                c.numar = form.cleaned_data.get(key)
                c.save()
                participanti.remove(key)

        for c in participanti:
            pe_data = dict(eveniment=self.object, numar=form.cleaned_data.get(c, 0))
            try:
                rdv = RamuraDeVarsta.objects.get(slug=c)
                pe_data['ramura_de_varsta'] = rdv
            except RamuraDeVarsta.DoesNotExist:
                pe_data['alta_categorie'] = c

            ParticipantiEveniment(**pe_data).save()

    def get_participant_count_initial(self):
        totals = {t: 0 for t in self.participanti}
        if not hasattr(self, "object") or self.object is None:
            return totals

        counts = ParticipantiEveniment.objects.filter(eveniment=self.object)
        for c in counts:
            if c.ramura_de_varsta is not None and c.ramura_de_varsta.slug in self.participanti:
                totals[c.ramura_de_varsta.slug] = c.numar
            elif c.alta_categorie is not None and c.alta_categorie in self.participanti:
                totals[c.alta_categorie] = c.numar
        return totals

    def handle_uploaded_file(self, f):
        fname = f.name
        if hasattr(self, 'object') and self.object is not None and self.object.id is not None:
            fname += str(self.object.id) + "-" + fname

        base_path = os.path.join("album", fname)
        path = os.path.join(MEDIA_ROOT, base_path)
        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        return base_path


class EvenimentCreate(CreateView, EvenimentEditMixin):
    model = Eveniment
    form_class = EvenimentCreateForm
    template_name = "album/eveniment_form.html"

    @allow_by_afiliere([("Utilizator, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.centru_local = request.user.utilizator.membru.centru_local
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        data = super(EvenimentCreate, self).get_initial()
        data.update(self.get_participant_count_initial())
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.centru_local = self.centru_local

        if "cover_photo" in self.request.FILES:
            path = self.handle_uploaded_file(self.request.FILES['cover_photo'])
            cover_photo = Imagine(image=path)
            cover_photo.save()
            self.object.custom_cover_photo = cover_photo

        self.object.save()
        self.update_counts(form)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_detail", kwargs={"slug": self.object.slug})


class EvenimentUpdate(UpdateView, EvenimentEditMixin):
    model = Eveniment
    form_class = EvenimentUpdateForm
    template_name = "album/eveniment_form.html"

    @allow_by_afiliere([("Eveniment, Centru Local", "Lider")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        return super(EvenimentUpdate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        data = super(EvenimentUpdate, self).get_initial()
        data.update(self.get_participant_count_initial())
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if "cover_photo" in self.request.FILES:
            path = self.handle_uploaded_file(self.request.FILES['cover_photo'])
            cover_photo = Imagine(image=path)
            cover_photo.save()
            self.object.custom_cover_photo = cover_photo
        self.object.save()
        self.update_counts(form)

        messages.success(self.request, u"Evenimentul a fost actualizat")
        return super(EvenimentUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("album:eveniment_detail", kwargs={"slug": self.object.slug})


class EvenimentDelete(GenericDeleteView):
    model = Eveniment

    @allow_by_afiliere([("Eveniment, Centru Local", u"Păstrător al amintirilor")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        return super(EvenimentDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("album:index")


class EvenimentDetail(DetailView):
    model = Eveniment
    template_name = "album/eveniment_detail.html"


class ImagineTagSearch(TemplateView):
    template_name = "album/tags_search.html"

    def get_context_data(self, **kwargs):
        tags = Tag.objects.all().annotate(num_times=Count("taggit_taggeditem_items")).order_by("-num_times")[:20]
        current = super(ImagineTagSearch, self).get_context_data(**kwargs)
        current.update({"tags": tags})
        return current


class ImagineSearchJSON(JSONView):
    _params = {"tags": {"type": "optional"},
               "limit": {"type": "optional"},
               "offset": {"type": "optional"},
               "authors": {"type": "optional"},
               "eveniment": {"type": "optional"},
               "zi": {"type": "optional"},
               "ordering": {"type": "optional"}}

    def clean_limit(self, value):
        try:
            limit = int(value)
            return limit if limit > 0 else 10
        except Exception, e:
            raise ScoutFileAjaxException("Bad limit", original_exception=e)

    def clean_ordering(self, value):
        return value

    def clean_offset(self, value):
        try:
            offset = int(value)
            return offset if offset > 0 else 0
        except Exception, e:
            raise ScoutFileAjaxException("Bad offset", original_exception=e)

    def clean_eveniment(self, value):
        try:
            return Eveniment.objects.get(id=int(value))
        except Exception, e:
            raise ScoutFileAjaxException(u"Nu există evenimentul", original_exception=e)

    def clean_zi(self, value):
        try:
            return ZiEveniment.objects.get(id=int(value))
        except Exception, e:
            raise ScoutFileAjaxException(u"Nu există ziua pentru eveniment", original_exception=e)

    def clean_tags(self, value):
        return parse_tags(value)

    def clean_authors(self, value):
        return value

    def post(self, request, *args, **kwargs):
        self.validate(**self.parse_json_data())

        qs = Imagine.objects.all()
        ordering_strings = []
        if "tags" in self.cleaned_data:
            qs = qs.filter(tags__name__in=self.cleaned_data['tags'])
        if "eveniment" in self.cleaned_data:
            ordering_strings.append("-score")
            qs = qs.filter(set_poze__eveniment=self.cleaned_data['eveniment'])
        if "zi" in self.cleaned_data:
            qs = qs.filter(id__in=[p.id for p in self.cleaned_data['zi'].filter_photos(user=request.user)])
        if "authors" in self.cleaned_data:
            qs = qs.filter(set_poze__autor__icontains=self.cleaned_data['authors'])


        qs = Imagine.filter_visibility(qs, request.user)
        if self.cleaned_data.get("ordering", "desc") == "desc":
            ordering_strings.append("-data")
        elif self.cleaned_data.get("ordering") == "asc":
            ordering_strings.append("data")

        if len(ordering_strings):
            qs = qs.order_by(*ordering_strings)

        #   limit users to access only available photos
        # qs = qs.filter(published_status__lt=self.eveniment.get_visibility_level(request.user))

        limit = self.cleaned_data.get("limit", 10)
        offset = self.cleaned_data.get("offset", 0)

        total_count = qs.count()
        qs = qs[offset:offset + limit]

        return HttpResponse(self.construct_json_response(queryset=qs, total_count=total_count))

    def imagine_to_json(self, imagine):
        return {"id": imagine.id,
                "url_thumb": imagine.get_thumbnail_url(),
                "url_detail": reverse("album:poza_detail", kwargs={"pk": imagine.id}),
                "url_detail_img": imagine.get_large_url(),
                "titlu": u"%s - %s" % (imagine.set_poze.eveniment.nume, imagine.titlu),
                "descriere": imagine.descriere or "",
                "autor": imagine.set_poze.get_autor(),
                "data": imagine.data.strftime("%d %B %Y %H:%M:%S"),
                "tags": [t.name for t in imagine.tags.all()[:10]],
                "rotate_url": reverse("album:poza_rotate", kwargs={"pk": imagine.id}),
                "published_status_display": imagine.get_published_status_display(),
                "flag_url": reverse("album:poza_flag", kwargs={"pk": imagine.id}),
                "score": imagine.score,

        }

    def construct_json_response(self, queryset, total_count, **kwargs):
        response_json = {"data": [self.imagine_to_json(im) for im in queryset],
                         "offset": self.cleaned_data['offset'],
                         "limit": self.cleaned_data['limit'],
                         "count": queryset.count(),
                         "total_count": total_count,
        }
        return dumps(response_json)


class ZiDetailBeta(DetailView):
    model = ZiEveniment
    template_name = "album/zi_detail_infinite.html"

    def dispatch(self, request, *args, **kwargs):
        if request.GET.has_key("autor"):
            self.autor = request.GET['autor']
        else:
            self.autor = None
        return super(ZiDetailBeta, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        current = super(ZiDetailBeta, self).get_context_data(*args, **kwargs)

        current.update({"autor": self.autor,
                        "visibility_states": IMAGINE_PUBLISHED_STATUS})

        centru_local = self.object.eveniment.centru_local
        calitate = TipAsociereMembruStructura.objects.get(nume__iexact=u"Păstrător al amintirilor", content_types__in=[
            ContentType.objects.get_for_model(centru_local)])
        if self.request.user.is_authenticated() and (self.request.user.get_profile().membru.are_calitate(calitate,
                                                                                                         centru_local) or self.request.user.is_superuser):
            current.update({"media_manager": True})

        return current


class RaportEvenimentUpdate(UpdateView):
    form_class = RaportEvenimentForm
    template_name = "album/eveniment_raport_form.html"
    model = RaportEveniment

    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))

        #TODO: trateaza cazul cu mai multe leaf-uri
        self.raport_nou = False
        if self.eveniment.raporteveniment_set.exists():
            kwargs['pk'] = self.eveniment.raporteveniment_set.all()[0].id
        else:
            self.object = self.create_raport(request)
            self.raport_nou = True
            kwargs['pk'] = self.object.id
        return super(RaportEvenimentUpdate, self).dispatch(request, *args, **kwargs)

    def create_raport(self, request):
        raport_data = {"eveniment": self.eveniment,
                       "editor": request.user.get_profile().membru,
                       "is_leaf": True,
                       "is_locked": False}
        raport = RaportEveniment(**raport_data)
        raport.save()
        return raport

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.editor = self.request.user.get_profile().membru
        if self.raport_nou is True:
            self.object.save()
        else:
            self.object.save_new_version(user=self.request.user)
        messages.success(self.request, u"Raportul a fost salvat!")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_detail", kwargs={"slug": self.eveniment.slug})

    def get_context_data(self, **kwargs):
        data = super(RaportEvenimentUpdate, self).get_context_data(**kwargs)
        data['eveniment'] = self.eveniment
        return data


class RaportEvenimentDetail(DetailView):
    model = Eveniment
    template_name = "album/eveniment_raport_detail.html"

    def dispatch(self, request, *args, **kwargs):
        #self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(RaportEvenimentDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(RaportEvenimentDetail, self).get_context_data(**kwargs)
        if self.object.raporteveniment_set.exists():
            data['raport'] = self.object.raporteveniment_set.all()[0]
        return data


class RaportEvenimentHistory(ListView):
    model = RaportEveniment
    template_name = "album/eveniment_raport_history.html"

    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(RaportEvenimentHistory, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return RaportEveniment.objects.version_history(eveniment=self.eveniment)

    def get_context_data(self, **kwargs):
        data = super(RaportEvenimentHistory, self).get_context_data(**kwargs)
        data['eveniment'] = self.eveniment
        return data


class CalendarCentruLocal(EvenimentFiltruMixin, CalendarViewMixin, DetailView):
    template_name = "album/calendar.html"
    model = CentruLocal

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.process_request_filters(request)
        return super(CalendarCentruLocal, self).dispatch(request, *args, **kwargs)

    def get_events_url(self):
        return reverse("album:events_centru_local", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        data = super(CalendarCentruLocal, self).get_context_data(**kwargs)
        data.update(self.filters_context_data())
        return data


class CalendarEvents(EvenimentFiltruMixin, ListView):
    model = Eveniment
    template_name = "album/json/events.json"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.cl = get_object_or_404(CentruLocal, id=kwargs.pop("pk"))
        if "from" not in request.GET or "to" not in request.GET:
            return HttpResponseBadRequest("Need to have 'to' and 'from' data set!")
        self.from_date = datetime.datetime.fromtimestamp(float(request.GET['from']) / 1000)
        self.to_date = datetime.datetime.fromtimestamp(float(request.GET['to']) / 1000)
        self.process_request_filters(request)
        return super(CalendarEvents, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.model.objects.filter(centru_local=self.cl)
        qs = qs.filter(Q(start_date__range=[self.from_date, self.to_date])
                       | Q(end_date__range=[self.from_date, self.to_date])
                       | Q(start_date__lte=self.from_date, end_date__gte=self.to_date))
        qs = self.apply_filters(qs)
        return qs

    def get_context_data(self, **kwargs):
        data = super(CalendarEvents, self).get_context_data(**kwargs)
        data.update(self.filters_context_data())
        return data


class RaportStatus(ListView):
    model = Eveniment
    template_name = "album/eveniment_raport_status.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.cl = request.user.get_profile().membru.get_centru_local()
        return super(RaportStatus, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.an = datetime.datetime.now().year - 1
        return self.model.objects.filter(start_date__year=self.an, centru_local=self.cl).order_by("start_date")

    def get_context_data(self, **kwargs):
        data = super(RaportStatus, self).get_context_data(**kwargs)
        data['scor_anual'] = sum(e.scor_calitate() for e in self.object_list)
        data['an'] = self.an
        return data


# class EvenimentParticipantList(ListView):
#     model = ParticipareEveniment
#     template_name = "album/eveniment_participant_list.html"
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(EvenimentParticipantList, self).dispatch(request, *args, **kwargs)


class AdaugaParticipantEveniment(CreateView):
    model = ParticipareEveniment
    template_name = "album/eveniment_participant_form.html"
    # form_class = ParticipantEvenimentForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(AdaugaParticipantEveniment, self).dispatch(request, *args, **kwargs)


class ModificaParticipantEveniment(UpdateView):
    model = ParticipareEveniment
    template_name = "album/eveniment_participant_form.html"
    # form_class = ParticipantEvenimentForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ModificaParticipantEveniment, self).dispatch(request, *args, **kwargs)


class InscriereEveniment(CreateView):
    model = ParticipareEveniment
    template_name = "album/eveniment_participant_form.html"
    # form_class = InscriereEvenimentForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(InscriereEveniment, self).dispatch(request, *args)


class RaportCompletPentruExport(ListView):
    model = Eveniment
    template_name = "album/eveniment_raport_export.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RaportCompletPentruExport, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.an = datetime.datetime.now().year - 1
        qs = super(RaportCompletPentruExport, self).get_queryset()
        qs = qs.filter(centru_local=self.request.user.get_profile().membru.centru_local)
        qs = qs.filter(end_date__year=self.an)
        qs = qs.order_by("end_date")
        return qs

    def get_context_data(self, **kwargs):
        data = super(RaportCompletPentruExport, self).get_context_data(**kwargs)
        data['an'] = self.an
        return data

class RaportActivitate(DetailView):
    model = Eveniment
    template_name = "album/eveniment_raport_complet.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RaportActivitate, self).dispatch(request, *args, **kwargs)


class AsociereEvenimentStructuraCreate(CreateView):
    model = AsociereEvenimentStructura
    form_class = AsociereEvenimentStructuraForm
    template_name = "album/asociere_eveniment_structura_form.html"

    @allow_by_afiliere([("Eveniment, Centru Local", "Lider")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(AsociereEvenimentStructuraCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.eveniment = self.eveniment
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_detail", kwargs={"slug": self.eveniment.slug})

    def get_context_data(self, **kwargs):
        data = super(AsociereEvenimentStructuraCreate, self).get_context_data(**kwargs)
        # data['object'] = self.eveniment
        data['eveniment'] = self.eveniment
        return data


class EvenimentParticipanti(ListView):
    model = ParticipareEveniment
    template_name = "album/eveniment_participanti_list.html"

    @allow_by_afiliere([("Eveniment, Centru Local", "Lider")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(EvenimentParticipanti, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(EvenimentParticipanti, self).get_context_data(**kwargs)
        data['eveniment'] = self.eveniment
        return data

class EvenimentParticipantiCreate(CreateView):
    model = ParticipareEveniment
    template_name = "album/eveniment_participanti_form.html"
    form_class = EvenimentParticipareForm

    @allow_by_afiliere([("Eveniment, Centru Local", "lider")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(EvenimentParticipantiCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        data = super(EvenimentParticipantiCreate, self).get_initial()
        data['data_sosire'] = self.eveniment.start_date
        data['data_plecare'] = self.eveniment.end_date
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.eveniment = self.eveniment
        self.object.user_modificare = self.request.user.get_profile().membru
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_participanti_list", kwargs={"slug": self.eveniment.slug})

    def get_context_data(self, **kwargs):
        data = super(EvenimentParticipantiCreate, self).get_context_data(**kwargs)
        data['eveniment'] = self.eveniment
        return data


class EvenimentParticipantiUpdate(UpdateView):
    model = ParticipareEveniment
    template_name = "album/eveniment_participanti_form.html"
    form_class = EvenimentParticipareForm

    @allow_by_afiliere([("Participare, Eveniment, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(EvenimentParticipantiUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(EvenimentParticipantiUpdate, self).get_context_data(**kwargs)
        data['eveniment'] = self.object.eveniment
        return data

    def get_success_url(self):
        return reverse("album:eveniment_participanti_list", kwargs={"slug": self.object.eveniment.slug})