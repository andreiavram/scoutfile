# coding: utf-8
from __future__ import division
from builtins import str
from builtins import range

from django.db.models import Sum
from past.utils import old_div
from builtins import object
import datetime
import json
import logging
from json import dumps

import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.files.base import File
from django.urls import reverse
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse, \
    HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.views.generic.list import ListView

from documente.models import Document
from financiar.models import PaymentDocument, Currency
from goodies.views import GenericDeleteView, CalendarViewMixin
from goodies.views import JSONView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from structuri.forms import AsociereEvenimentStructuraForm
from structuri.models import Membru, CentruLocal, Unitate, Patrula, TipAsociereMembruStructura
from taggit.models import Tag
from taggit.utils import parse_tags

from album.exporters.envelopes import C5Envelopes
from album.models import Eveniment, ZiEveniment, Imagine, FlagReport, RaportEveniment, ParticipareEveniment, \
    AsociereEvenimentStructura, TipEveniment, SetPoze, IMAGINE_PUBLISHED_STATUS, \
    CampArbitrarParticipareEveniment, InstantaCampArbitrarParticipareEveniment, FLAG_MOTIVES, ParticipantEveniment, \
    StatusEveniment, EventContributionOption, EventURL, StatusParticipare, RolParticipare
from album.forms import ReportForm, EvenimentCreateForm, EvenimentUpdateForm, PozaTagsForm, ZiForm, RaportEvenimentForm, \
    EvenimentParticipareForm, SetPozeCreateForm, SetPozeUpdateForm, CampArbitrarForm, EvenimentParticipareUpdateForm, \
    ReportFormNoButtons, EvenimentParticipareNonMembruForm, EvenimentParticipareNonmembruUpdateForm, \
    EvenimentParticipantFilterForm, EventContributionOptionForm, EventPaymentDocumentForm, EventURLForm, \
    EvenimentParticipareRegistrationForm
from album.exporters.table import TabularExport
from generic.views import ScoutFileAjaxException
from structuri.decorators import allow_by_afiliere

logger = logging.getLogger(__name__)


class EvenimentFiltruMixin(object):
    def process_request_filters(self, request):
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if "qnume" in request.GET:
                request.session['qnume'] = request.GET['qnume']
            elif "qnume" in request.session:
                del request.session['qnume']

        if "status" not in request.session:
            request.session["status"] = "terminat"
        if "status" in request.GET:
            request.session["status"] = request.GET.get("status")

        if "unitate" in request.GET:
            if "patrula" in request.session:
                del request.session['patrula']
            if request.GET.get("unitate") == "0" and "unitate" in request.session:
                del request.session['unitate']
            else:
                request.session['unitate'] = int(request.GET.get("unitate"))

        if "patrula" in request.GET:
            if "unitate" in request.session:
                del request.session['unitate']
            if request.GET.get("patrula") == "0" and "patrula" in request.session:
                del request.session['patrula']
            else:
                request.session['patrula'] = int(request.GET.get("patrula"))

        self.unitate = None
        if "unitate" in request.session and request.session['unitate'] != 0:
            self.unitate = Unitate.objects.get(id=request.session['unitate'])

        self.patrula = None
        if "patrula" in request.session and request.session["patrula"] != 0:
            self.patrula = Patrula.objects.get(id=request.session["patrula"])

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
        if self.request.user.is_authenticated:
            centru_local = self.request.user.utilizator.membru.centru_local
            data['unitati'] = centru_local.unitate_set.all()
        data['tipuri_activitate'] = [t for t in TipEveniment.objects.all() if t.eveniment_set.count() > 0]
        data['status_activitate'] = StatusEveniment.choices
        data['tip_activitate'] = self.tip_activitate
        data['unitate'] = self.unitate
        data['patrula'] = self.patrula
        status = "Toate"
        for s in StatusEveniment.choices:
            if s[0] == self.request.session["status"]:
                status = s[1]
                break

        data['status'] = status

        return data

    def apply_filters(self, qs):
        if self.unitate:
            qs = qs.filter(id__in=[e.id for e in qs if e.are_asociere(self.unitate)])
        if self.patrula:
            qs = qs.filter(id__in=[e.id for e in qs if e.are_asociere(self.patrula)])

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
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.per_page = int(request.POST.get("per_page", 5))
            self.offset = int(request.POST.get("offset", 0))

        if request.user.is_authenticated:
            self.centru_local = request.user.utilizator.membru.centru_local
        else:
            self.centru_local = CentruLocal.objects.get(id=settings.CENTRU_LOCAL_IMPLICIT)

        self.process_request_filters(request)
        return super(EvenimentList, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(EvenimentList, self).get_queryset(*args, **kwargs)
        qs = qs.filter(centru_local=self.centru_local)

        if "qnume" in self.request.session:
            qs = qs.filter(nume__icontains=self.request.session['qnume'])

        qs = self.apply_filters(qs)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.total_count = qs.count()
            qs = qs[self.offset:self.offset + self.per_page]
            self.current_count = qs.count()

        return qs

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return "album/json/eveniment_list.json"
        return self.template_name

    def get_context_data(self, **kwargs):
        data = super(EvenimentList, self).get_context_data(**kwargs)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data['total_count'] = self.total_count
            data['current_count'] = self.current_count
            data['requested_count'] = self.per_page
            data['current_offset'] = self.offset

        an_curent = datetime.datetime.now().year
        data['ani_activitati'] = list(range(an_curent - 2, an_curent + 1))
        data['ani_activitati'].reverse()
        data['centru_local'] = self.centru_local
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
        current["visibility_states"] = IMAGINE_PUBLISHED_STATUS

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
        if "autor" in request.GET:
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
        if self.request.user.is_authenticated and (self.request.user.utilizator.membru.are_calitate(calitate,
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
        if "autor" in request.GET:
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

        zi_page = (old_div((photo.count()), 30)) + 1
        current.update({"zi_page": zi_page})
        current.update({"visibility_states": IMAGINE_PUBLISHED_STATUS})

        centru_local = self.object.set_poze.eveniment.centru_local
        calitate = TipAsociereMembruStructura.objects.get(nume__iexact=u"Păstrător al amintirilor", content_types__in=[
            ContentType.objects.get_for_model(centru_local)])
        if self.request.user.is_authenticated and (self.request.user.utilizator.membru.are_calitate(calitate,
                                                                                                      centru_local) or self.request.user.is_superuser):
            current.update({"media_manager": True})

        current["report_form"] = ReportFormNoButtons()
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
        if self.request.user.utilizator.membru.are_calitate(calitate, centru_local):
            current.update({"media_manager": True})

        return current


#TODO: update this to a full API view
class PozaUpdateTags(View):
    def dispatch(self, request, *args, **kwargs):
        self.poza = get_object_or_404(Imagine, id=kwargs.pop("pk"))
        return super(PozaUpdateTags, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.debug("PozaUpdateTags: %s", request.POST.get("tags"))
        self.poza.tags.clear()
        self.poza.tags.set(*parse_tags(request.POST.get("tags")))

        import json
        return HttpResponse(json.dumps({"tags": list(self.poza.tags.names())}))


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
        messages.success(self.request, "Poza a fost flag-uită, un lider sau fotograful vor decide ce acțiune se va lua în continuare")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:poza_detail", kwargs={"pk": self.poza.id})

    def get_form(self, form_class):
        form = super(FlagImage, self).get_form(form_class)
        form.has_submit_buttons = True
        return form

    def get_context_data(self, *args, **kwargs):
        current = super(FlagImage, self).get_context_data(*args, **kwargs)
        current.update({"object": self.poza, "poza": self.poza})

        return current

class FlagImageAjax(JSONView):
    _params = {"imagine": {"type": "required"},
               "motiv": {"type": "required"},
               "motiv_altul": {"type": "required"}}

    def clean_imagine(self, value):
        try:
            return Imagine.objects.get(id=int(value))
        except Exception as e:
            raise ScoutFileAjaxException(extra_message="This image does not exist", exception=e)

    def clean_motiv(self, value):
        if value not in [v[0] for v in FLAG_MOTIVES]:
            raise ScoutFileAjaxException(extra_message="Motivul este invalid")
        return value

    def clean_motiv_altul(self, value):
        if not len(value):
            value = None
        return value

    def post(self, request, *args, **kwargs):
        self.validate(**self.parse_json_data())

        if self.cleaned_data['motiv'] == 'altul' and not self.cleaned_data['motiv_altul']:
            return HttpResponseBadRequest('Motiv "altul" fara explicatii')

        FlagReport.objects.create(imagine=self.cleaned_data['imagine'], motiv=self.cleaned_data["motiv"], alt_motiv=self.cleaned_data["motiv_altul"])
        return HttpResponse(self.construct_json_response(result=True, imagine=self.cleaned_data['imagine']))

    def construct_json_response(self, **kwargs):
        json_dict = {"result": kwargs.get("result", False)}
        return json.dumps(json_dict)


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
        for key in list(request.session.keys()):
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

            self.object.autor_user = Membru.objects.get(id=self.request.user.utilizator.id)

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
                           'delete_url': "https://" + Site.objects.get_current().domain + reverse("album:set_poze_delete_ajax",
                                                                     kwargs={"pk": self.object.id}),
                           'delete_type': "DELETE"}]}

        response = HttpResponse(json.dumps(data), content_type=self.response_mimetype())
        return response

    def form_invalid(self, form):
        logger.debug("%s - form invalid (%s)" % (self.__class__.__name__, form.errors))
        logger.debug("%s - POST data (%s)" % (self.__class__.__name__, self.request.POST))
        #         data = [{"error" : u"Cannot upload", "error_dict" : form.errors}]

        f = self.request.FILES.get('zip_file')
        data = {"files": [{"name": f.name, "error": u"Cannot upload"}]}

        response = HttpResponse(json.dumps(data), content_type=self.response_mimetype())
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
        Membru.objects.get(id=request.user.utilizator.id) == self.set_poze.autor_user))
        if request.user.is_superuser or Membru.objects.get(
                id=request.user.utilizator.id) == self.set_poze.autor_user:
            try:
                os.unlink(self.set_poze.zip_file)
            except Exception as e:
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
        self.membru = request.user.utilizator.membru
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
        qs = qs.filter(autor_user=Membru.objects.get(id=self.request.user.utilizator.id))
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
        qs = qs.filter(autor_user=Membru.objects.get(id=self.request.user.utilizator.id))
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
        if self.object.autor_user_id != request.user.utilizator.id:
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
        except Exception as e:
            raise ScoutFileAjaxException(extra_message="This image does not exist", exception=e)

    def clean_new_status(self, value):
        #TODO: change this from range to actual valid values
        if int(value) not in list(range(1, 5)):
            raise ScoutFileAjaxException(extra_message="The status is invalid")
        return int(value)

    def post(self, request, *args, **kwargs):
        self.validate(**self.parse_json_data())

        centru_local = self.cleaned_data['imagine'].set_poze.eveniment.centru_local
        calitate = TipAsociereMembruStructura.objects.get(nume__iexact=u"Păstrător al amintirilor", content_types__in=[
            ContentType.objects.get_for_model(centru_local)])
        if not self.request.user.utilizator.membru.are_calitate(calitate,
                                                                   centru_local) and not self.request.user.is_superuser:
            return HttpResponseForbidden()

        self.cleaned_data['imagine'].published_status = self.cleaned_data['new_status']
        self.cleaned_data['imagine'].save()

        return HttpResponse(self.construct_json_response(result=True, imagine=self.cleaned_data['imagine']))

    def construct_json_response(self, **kwargs):
        json_dict = {"result": kwargs.get("result", False),
                     "new_status_string": kwargs.get("imagine").get_published_status_display()}
        return json.dumps(json_dict)


class FileUploadMixin(object):
    def handle_uploaded_file(self, f):
        fname = f.name
        if hasattr(self, 'object') and self.object is not None and self.object.id is not None:
            fname += str(self.object.id) + "-" + fname

        path = os.path.join("/tmp", fname)
        #path = os.path.join(MEDIA_ROOT, base_path)
        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        return path

    def get_save_kwargs(self, file_handler, local_file_name):
        return {}

    def save_photo(self, form_field_name="cover_photo", object_field_name="custom_cover_photo", image_class=Imagine, folder_path="covers", save=True):
        return self.save_file(form_field_name, object_field_name, image_class, folder_path, save)

    def get_target_object(self):
        return self.object

    def save_file(self, form_field_name="cover_photo", object_field_name='custom_cover_photo', image_class=Imagine, folder_path="covers", save=True):
        if form_field_name in self.request.FILES:
            try:
                path = self.handle_uploaded_file(self.request.FILES[form_field_name])
            except Exception as e:
                return

            target_object = self.get_target_object()
            if getattr(target_object, object_field_name):
                try:
                    getattr(target_object, object_field_name).image.delete()
                    getattr(target_object, object_field_name).delete()
                except Exception as e:
                    logger.error("%s: Could not delete photo %s" % (self.__class__.__name__, e))
            filehandler = open(path, "rb")
            cover_photo = image_class()
            cover_photo_path = os.path.join(settings.PHOTOLOGUE_DIR, folder_path, self.request.FILES[form_field_name].name)
            cover_photo.image.save(cover_photo_path, File(filehandler), save=False)
            cover_photo.save(**self.get_save_kwargs(file_handler=filehandler, local_file_name=path))
            setattr(target_object, object_field_name, cover_photo)

            if save:
                target_object.save()


class EvenimentEditMixin(FileUploadMixin):
    participanti = ["lupisori", "temerari", "seniori", "exploratori", "adulti", "lideri"]

    def get_save_kwargs(self, file_handler, local_file_name):
        return {"file_handler": file_handler, "local_file_name": local_file_name}

    def save_cover_photo(self, save=True):
        cover_photo_args = dict(form_field_name="cover_photo", object_field_name="custom_cover_photo", image_class=Imagine, folder_path="covers")
        cover_photo_args['save'] = save
        self.save_photo(**cover_photo_args)


class EvenimentCreate(CreateView, EvenimentEditMixin):
    model = Eveniment
    form_class = EvenimentCreateForm
    template_name = "album/eveniment_form.html"
    target_model = CentruLocal

    adauga_persoane_possible = False

    @allow_by_afiliere([("Utilizator, Centru Local", "Lider"), ("Utilizator, Centru Local", "Lider asistent"), ])
    def dispatch(self, request, *args, **kwargs):
        self.centru_local = request.user.utilizator.membru.centru_local

        self.target_obj = None
        if "pk" in kwargs:
            self.target_obj = get_object_or_404(self.target_model, id=kwargs.pop("pk"))

        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.centru_local = self.centru_local
        self.object.slug = slugify(self.object.nume) + "-%s" % self.object.start_date.year
        index = 1
        while self.model.objects.filter(slug=self.object.slug).exists():
            index += 1
            self.object.slug = slugify(self.object.nume) + "-%s-%d" % (self.object.start_date.year, index)

        self.object.save()
        self.save_cover_photo()
        self.create_connections(
            adauga_persoane=form.cleaned_data["adauga_persoane"],
            adauga_lideri=form.cleaned_data["adauga_lideri"]
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_detail", kwargs={"slug": self.object.slug})

    def create_connections(self, adauga_persoane=False, adauga_lideri=False):
        if self.target_obj is not None:
            self.object.creeaza_asociere_structura(self.target_obj)

            if self.adauga_persoane_possible:
                if adauga_persoane:
                    _ = [self.object.creaza_participare(c) for c in self.target_obj.cercetasi()]
                if adauga_lideri:
                    _ = [self.object.creaza_participare(l) for l in self.target_obj.lideri()]


class UnitateEvenimentCreate(EvenimentCreate):
    target_model = Unitate
    adauga_persoane_possible = True


class PatrulaEvenimentCreate(UnitateEvenimentCreate):
    target_model = Patrula
    adauga_persoane_possible = True


class EvenimentUpdate(UpdateView, EvenimentEditMixin):
    model = Eveniment
    form_class = EvenimentUpdateForm
    template_name = "album/eveniment_form.html"

    @allow_by_afiliere([("Eveniment, Centru Local", "Lider")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        return super(EvenimentUpdate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        data = super(EvenimentUpdate, self).get_initial()
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.save_cover_photo(save=False)
        self.object.save()

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

    def get_context_data(self, **kwargs):
        data = super(EvenimentDetail, self).get_context_data(**kwargs)
        data['report_form'] = ReportFormNoButtons()
        data['visibility_states'] = IMAGINE_PUBLISHED_STATUS
        return data


class ImagineTagSearch(TemplateView):
    template_name = "album/tags_search.html"

    def get_context_data(self, **kwargs):
        tags = Tag.objects.all().annotate(num_times=Count("taggit_taggeditem_items")).order_by("-num_times")[:20]
        current = super(ImagineTagSearch, self).get_context_data(**kwargs)
        current.update({"tags": tags})
        current['report_form'] = ReportFormNoButtons()
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
        except Exception as e:
            raise ScoutFileAjaxException("Bad limit", original_exception=e)

    def clean_ordering(self, value):
        return value

    def clean_offset(self, value):
        try:
            offset = int(value)
            return offset if offset > 0 else 0
        except Exception as e:
            raise ScoutFileAjaxException("Bad offset", original_exception=e)

    def clean_eveniment(self, value):
        try:
            return Eveniment.objects.get(id=int(value))
        except Exception as e:
            raise ScoutFileAjaxException(u"Nu există evenimentul", original_exception=e)

    def clean_zi(self, value):
        try:
            return ZiEveniment.objects.get(id=int(value))
        except Exception as e:
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

        eveniment = None
        if "eveniment" in self.cleaned_data:
            eveniment =self.cleaned_data['eveniment']
            ordering_strings.append("-score")
            qs = qs.filter(set_poze__eveniment=self.cleaned_data['eveniment'])

        if "zi" in self.cleaned_data:
            qs = qs.filter(id__in=[p.id for p in self.cleaned_data['zi'].filter_photos(user=request.user)])
        if "authors" in self.cleaned_data:
            qs = qs.filter(set_poze__autor__icontains=self.cleaned_data['authors'])

        qs = Imagine.filter_visibility(qs, eveniment=eveniment, user=request.user)


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

    # def imagine_to_json(self, imagine):
    #     return imagine.to_json()

    def construct_json_response(self, queryset, total_count, **kwargs):
        response_json = {"data": [im.to_json() for im in queryset],
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
        if "autor" in request.GET:
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
        if self.request.user.is_authenticated and (self.request.user.utilizator.membru.are_calitate(calitate,
                                                                                                         centru_local) or self.request.user.is_superuser):
            current.update({"media_manager": True})

        current['report_form'] = ReportFormNoButtons()
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
            self.object = self.eveniment.raporteveniment_set.all()[0]
        else:
            self.object = self.create_raport(request)
            self.raport_nou = True

        return super(RaportEvenimentUpdate, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.object

    def create_raport(self, request):
        raport_data = {"eveniment": self.eveniment,
                       "editor": request.user.utilizator.membru,
                       "is_leaf": True,
                       "is_locked": False}
        raport = RaportEveniment(**raport_data)
        raport.save()
        return raport

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.editor = self.request.user.utilizator.membru
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
        data['centru_local'] = self.object
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
        self.cl = request.user.utilizator.membru.get_centru_local()
        date_now = datetime.datetime.now()
        year = date_now.year
        if date_now.day < 15 and date_now.month < 2:
            year -= 1
        self.an = int(request.GET.get("an", year))
        return super(RaportStatus, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(start_date__year=self.an, centru_local=self.cl).order_by("start_date")

    def get_context_data(self, **kwargs):
        data = super(RaportStatus, self).get_context_data(**kwargs)
        data['scor_anual'] = sum(e.scor_calitate() for e in self.object_list)
        data['an'] = self.an
        data['ani'] = list(range(self.an - 1, self.an + 2))
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
        qs = qs.filter(centru_local=self.request.user.utilizator.membru.centru_local)
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
        self.cancelled = False
        if "cancelled" in request.GET:
            self.cancelled = True

        self.pagesize = None
        if "pagesize" in request.GET:
            self.pagesize = int(request.GET.get("pagesize", 0))

        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(EvenimentParticipanti, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.model.objects.filter(eveniment=self.eveniment)
        if self.cancelled:
            qs = qs.filter(status_participare=5)
        else:
            qs = qs.exclude(status_participare=5)

        qs = qs.select_related("membru", "nonmembru", "eveniment")

        return qs

    def get_context_data(self, **kwargs):
        data = super(EvenimentParticipanti, self).get_context_data(**kwargs)
        data['eveniment'] = self.eveniment
        data['cancelled'] = self.cancelled
        data['campuri_arbitrare'] = self.eveniment.camparbitrarparticipareeveniment_set.all().prefetch_related("instante")[0:]
        data['pagesize'] = self.pagesize
        data['full_count'] = self.object_list.count()
        return data


class EvenimentParticipantiExport(FormView):
    form_class = EvenimentParticipantFilterForm
    template_name = "album/eveniment_participanti_options.html"

    EXPORT_OPTIONS = (("plicuri_c5", u"Plicuri C5", u"Export PDF cu plicuri C5 pentru printare"),
                      ("tabel_xlsx", u"Tabel", u"Export XLS cu toți participanții"),
                      ("date_json", u"JSON", u"Date în format JSON, care pot fi procesate de alte aplicații"))

    @allow_by_afiliere([("Eveniment, Centru Local", "Lider")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(EvenimentParticipantiExport, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        data = super(EvenimentParticipantiExport, self).get_form_kwargs()
        data['export_options'] = self.EXPORT_OPTIONS
        data['eveniment'] = self.eveniment
        return data

    def get_queryset(self, filters=None, status_list=()):
        qs = self.eveniment.participareeveniment_set.filter(status_participare__in=status_list)

        for camp, valoare in list(filters.items()):
            instante_filters = dict(camp=camp, valoare_text="%s" % valoare)
            instante = InstantaCampArbitrarParticipareEveniment.objects.filter(**instante_filters)
            qs = qs.filter(id__in=instante.values_list("participare_id", flat=True))

        return qs

    def plicuri_c5(self, qs):
        return C5Envelopes.generate_envelopes(qs)

    def tabel_xlsx(self, qs):
        return TabularExport.generate_xlsx(qs)

    def date_json(self, qs):
        return TabularExport.generate_json(qs)

    def form_valid(self, form):
        qs = self.get_queryset(filters=form.cleaned_data.get("filter_expression", None),
                               status_list=form.cleaned_data.get("status_participare"))

        return getattr(self, form.cleaned_data.get("tip_export"))(qs)

    def get_context_data(self, **kwargs):
        data = super(EvenimentParticipantiExport, self).get_context_data(**kwargs)
        data['eveniment'] = self.eveniment
        return data


class EvenimentParticipantiCreate(CreateView):
    model = ParticipareEveniment
    template_name = "album/eveniment_participanti_form.html"
    form_class = EvenimentParticipareForm

    @allow_by_afiliere([("Eveniment, Centru Local", "Lider")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(EvenimentParticipantiCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        data = super(EvenimentParticipantiCreate, self).get_initial()
        data['data_sosire'] = self.eveniment.start_date
        data['data_plecare'] = self.eveniment.end_date
        return data

    def get_form_kwargs(self):
        data = super(EvenimentParticipantiCreate, self).get_form_kwargs()
        data['eveniment'] = self.eveniment
        data['request'] = self.request
        return data

    def _process_object_from_form(self, form):
        self.object = form.save(commit=False)
        self.object.eveniment = self.eveniment
        self.object.user_modificare = self.request.user.utilizator.membru

    def form_valid(self, form):
        self._process_object_from_form(form)
        self.object.save()

        for camp in self.eveniment.camparbitrarparticipareeveniment_set.all():
            camp.set_value(form.cleaned_data[camp.slug], self.object)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_participanti_list", kwargs={"slug": self.eveniment.slug})

    def get_context_data(self, **kwargs):
        data = super(EvenimentParticipantiCreate, self).get_context_data(**kwargs)
        data['eveniment'] = self.eveniment
        return data


class EvenimentParticipantNonMembruCreate(EvenimentParticipantiCreate):
    form_class = EvenimentParticipareNonMembruForm

    def _process_object_from_form(self, form):
        super(EvenimentParticipantNonMembruCreate, self)._process_object_from_form(form)
        pe_kwargs = {n: form.cleaned_data.get(n, None) for n in ["nume", "prenume", "email", "telefon", "adresa_postala"]}
        pe, created = ParticipantEveniment.objects.get_or_create(**pe_kwargs)
        self.object.nonmembru = pe


class EvenimentParticipantiUpdate(UpdateView):
    model = ParticipareEveniment
    template_name = "album/eveniment_participanti_form.html"
    form_class = EvenimentParticipareUpdateForm

    @allow_by_afiliere([("Participare, Eveniment, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(EvenimentParticipantiUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(EvenimentParticipantiUpdate, self).get_context_data(**kwargs)
        data['eveniment'] = self.object.eveniment
        return data

    def get_form_kwargs(self):
        data = super(EvenimentParticipantiUpdate, self).get_form_kwargs()
        data['eveniment'] = self.object.eveniment
        data['request'] = self.request
        return data

    def get_initial(self):
        data = super(EvenimentParticipantiUpdate, self).get_initial()
        for camp in self.object.eveniment.camparbitrarparticipareeveniment_set.all():
            data[camp.slug] = camp.get_value(self.object)

        return data

    def _process_object_from_form(self, form):
        self.object = form.save(commit=False)
        self.object.user_modificare = self.request.user.utilizator.membru

    def form_valid(self, form):
        self._process_object_from_form(form)
        self.object.save()

        for camp in self.object.eveniment.camparbitrarparticipareeveniment_set.all():
            camp.set_value(form.cleaned_data[camp.slug], self.object)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_participanti_list", kwargs={"slug": self.object.eveniment.slug})


class EvenimentParticipantNonMembruUpdate(EvenimentParticipantiUpdate):
    form_class = EvenimentParticipareNonmembruUpdateForm

    def get_initial(self):
        data = super(EvenimentParticipantNonMembruUpdate, self).get_initial()
        nonmembru = {n: getattr(self.object.nonmembru, n, None) for n in ["nume", "prenume", "email", "telefon", "adresa_postala"]}
        data.update(nonmembru)
        return data

    def _process_object_from_form(self, form):
        super(EvenimentParticipantNonMembruUpdate, self)._process_object_from_form(form)
        for key in ["nume", "prenume", "email", "telefon", "adresa_postala"]:
            setattr(self.object.nonmembru, key, form.cleaned_data.get(key, None))
        self.object.nonmembru.save()


class EvenimentCampuriArbitrare(ListView):
    model = CampArbitrarParticipareEveniment
    template_name = "album/eveniment_campuri_list.html"

    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(EvenimentCampuriArbitrare, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(eveniment=self.eveniment)

    def get_context_data(self, **kwargs):
        data = super(EvenimentCampuriArbitrare, self).get_context_data(**kwargs)
        data['eveniment'] = self.eveniment
        data['coloane_permise'] = Eveniment.CAMPURI_PERMISE
        return data


class EvenimentSlugMixin(object):
    def make_slug_unique(self, slug, obj=None):
        # make sure slug is unique pentru eveniment
        slugs = self.eveniment.camparbitrarparticipareeveniment_set.all()
        if obj:
            slugs = slugs.exclude(id = obj.id)
        slugs = list(slugs.values_list("slug", flat=True))
        slugs.sort(key=lambda x: len(x))
        found = False
        found_max_count = 0
        for s in slugs:
            if s == slug:
                found = True
                found_max_count = 1

        if found:
            s = "%s_%d" % (slug, 1)
            while s in slugs:
                found_max_count += 1
                s = "%s_%d" % (slug, found_max_count)

            slug = s

        return slug


class EvenimentCampuriArbitrareCreate(EvenimentSlugMixin, CreateView):
    model = CampArbitrarParticipareEveniment
    form_class = CampArbitrarForm
    template_name = "album/eveniment_campuri_form.html"

    #TODO: limit access
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(EvenimentCampuriArbitrareCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        from django.template.defaultfilters import slugify
        self.object.slug = self.make_slug_unique(slugify(self.object.nume))
        self.object.eveniment = self.eveniment
        self.object.save()

        if self.object.implicit:
            for participare in self.eveniment.participareeveniment_set.all():
                self.object.set_value(self.object.implicit, participare=participare)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_campuri_list", kwargs={"slug": self.eveniment.slug})

    def get_context_data(self, **kwargs):
        data = super(EvenimentCampuriArbitrareCreate, self).get_context_data(**kwargs)
        data['eveniment'] = self.eveniment
        return data

    def get_form_kwargs(self):
        data = super(EvenimentCampuriArbitrareCreate, self).get_form_kwargs()
        data['eveniment'] = self.eveniment
        return data


class EvenimentCampuriArbitrareUpdate(EvenimentSlugMixin, UpdateView):
    model = CampArbitrarParticipareEveniment
    form_class = CampArbitrarForm
    template_name = "album/eveniment_campuri_form.html"

    #TODO: limit access
    def dispatch(self, request, *args, **kwargs):
        return super(EvenimentCampuriArbitrareUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(EvenimentCampuriArbitrareUpdate, self).get_context_data(**kwargs)
        data['eveniment'] = self.object.eveniment
        return data

    def get_object(self, queryset=None):
        obj = super(EvenimentCampuriArbitrareUpdate, self).get_object(queryset=queryset)
        self.eveniment = obj.eveniment
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        from django.template.defaultfilters import slugify
        self.object.slug = self.make_slug_unique(slugify(self.object.nume), self.object)
        self.object.save()

        if self.object.implicit:
            for participare in self.eveniment.participareeveniment_set.all():
                filter_kwargs = dict(camp=self.object, participare=participare)

                if InstantaCampArbitrarParticipareEveniment.objects.filter(**filter_kwargs).count() == 0:
                    self.object.set_value(self.object.implicit, participare)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_campuri_list", kwargs={"slug": self.object.eveniment.slug})

    def get_form_kwargs(self):
        data = super(EvenimentCampuriArbitrareUpdate, self).get_form_kwargs()
        data['eveniment'] = self.object.eveniment
        return data


class EvenimentUpdateCampuriAditionale(View):
    @allow_by_afiliere([("Eveniment, Centru Local", "Lider"), ("Eveniment, Centru Local", "Lider asistent")])
    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Eveniment, slug=kwargs.pop("slug"))
        return super(EvenimentUpdateCampuriAditionale, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST.get("campuri", "").strip(";").split(";")
        data = [d for d in data if d in [c[0] for c in self.object.CAMPURI_PERMISE]]
        data = ";".join(data)
        if self.object.campuri_aditionale != data:
            self.object.campuri_aditionale = data
            self.object.save()

        return HttpResponse(status=200)


class PozaVot(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        img_id = int(request.data.get("picture_id"))
        img = get_object_or_404(Imagine, id=img_id)

        if "has_voted_%d" % img.id in request.session:
            json_data = {}
            return Response(json_data)

        request.session["has_voted_%d" % img.id] = True

        score = int(request.data.get("score"))
        score = old_div(score, abs(score))

        img.vote_photo(score)
        json_data = {"picture_id": img.id, "current_score": img.score}

        return Response(json_data)


class PozaMakeCover(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        img_id = int(request.data.get('picture_id'))
        img = get_object_or_404(Imagine, id=img_id)
        img.set_poze.eveniment.custom_cover_photo = img
        img.set_poze.eveniment.save()

        return Response({"message": u"Imaginea a fost setată ca poza de copertă pentru album"})


@method_decorator(login_required, name="dispatch")
class EventContributionList(ListView):
    model = EventContributionOption
    template_name = "album/eveniment_tipcontributii_list.html"

    def dispatch(self, request, *args, **kwargs):
        self.event = Eveniment.objects.get(slug=kwargs.pop("slug"))
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(eveniment=self.event)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['eveniment'] = self.event
        return context


class EventContributionCreate(CreateView):
    models = EventContributionOption
    form_class = EventContributionOptionForm
    template_name = "album/eveniment_tipcontributii_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.eveniment = self.event
        self.object.save()
        messages.success(
            self.request,
            "Tip Contribuție creat"
        )
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        self.event = Eveniment.objects.get(slug=kwargs.pop("slug"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eveniment'] = self.event
        return context

    def get_success_url(self):
        return reverse("album:eveniment_tipcontributii_list", kwargs={"slug": self.event.slug})


class EventContributionUpdate(UpdateView):
    model = EventContributionOption
    form_class = EventContributionOptionForm
    template_name = "album/eveniment_tipcontributii_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eveniment'] = self.object.eveniment
        return context

    def get_success_url(self):
        return reverse("album:eveniment_tipcontributii_list", kwargs={"slug": self.object.eveniment.slug})


@method_decorator(login_required, name="dispatch")
class EventPaymentCreate(CreateView):
    model = PaymentDocument
    form_class = EventPaymentDocumentForm
    template_name = "album/eveniment_payment_form.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            self.participation = ParticipareEveniment.objects.select_related("eveniment", "membru", "contribution_option").get(pk=self.kwargs.get("pk"))
        except ParticipareEveniment.DoesNotExist:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        if self.participation.contribution_option:
            if self.participation.contribution_payments.exists():
                total_value = self.participation.contribution_payments.aggregate(Sum('value'))
                initial['value'] = self.participation.contribution_option.value - total_value['value__sum']
            else:
                initial['value'] = self.participation.contribution_option.value

        initial['notes'] = f"Contribuție participare pentru {self.participation.eveniment.nume}"
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.currency = Currency.RON
        self.object.domain = self.participation.eveniment.centru_local.default_payment_domain
        self.object.registration_status = PaymentDocument.RegistrationType.PAYMENT
        self.object.registered_by = self.request.user
        self.object.direction = PaymentDocument.RegistrationDirection.ISSUER
        if self.participation.membru:
            self.object.third_party_internal = self.participation.membru
        self.object.save()
        self.participation.contribution_payments.add(self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_participanti_list", kwargs={"slug": self.participation.eveniment.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eveniment'] = self.participation.eveniment
        context['participare'] = self.participation
        return context


class EvenimentDetailMixin:
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug=kwargs.pop('slug'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['eveniment'] = self.eveniment
        return context


class EventLinkList(EvenimentDetailMixin, ListView):
    model = EventURL
    template_name = "album/eveniment_url_list.html"
    @allow_by_afiliere([("Eveniment, Centru Local", "Lider"), ("Eveniment, Centru Local", "Lider asistent")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(eveniment=self.eveniment)


class EventLinkCreate(EvenimentDetailMixin, CreateView):
    model = EventURL
    form_class = EventURLForm
    template_name = "album/eveniment_url_form.html"
    @allow_by_afiliere([("Eveniment, Centru Local", "Lider"), ("Eveniment, Centru Local", "Lider asistent")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.eveniment = self.eveniment
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_url_list", kwargs={"slug": self.eveniment.slug})


class EventLinkUpdate(UpdateView):
    model = EventURL
    form_class = EventURLForm
    template_name = "album/eveniment_url_form.html"

    @allow_by_afiliere([("Eveniment, Centru Local", "Lider"), ("Eveniment, Centru Local", "Lider asistent")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eveniment'] = self.object.eveniment
        return context

    def get_success_url(self):
        return reverse("album:eveniment_url_list", kwargs={"slug": self.object.eveniment.slug})


class EventDocumentsView(EvenimentDetailMixin, ListView):
    model = Document
    template_name = "album/eveniment_documents.html"

    @allow_by_afiliere([("Eveniment, Centru Local", "Lider"), ("Eveniment, Centru Local", "Lider asistent")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(evenimente__in=[self.eveniment, ])


class EventRegisterView(EvenimentDetailMixin, UpdateView):
    model = ParticipareEveniment
    form_class = EvenimentParticipareRegistrationForm
    template_name = "album/eveniment_register_form.html"

    # TODO: make this depend on Conexiuni Internet as well
    @allow_by_afiliere([("Eveniment, Centru Local", "Membru"), ], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['eveniment'] = self.eveniment
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        submit_mapping = {
            "confirm": StatusParticipare.CONFIRMED,
            "deffer": StatusParticipare.UNKNOWN,
            "reject": StatusParticipare.REFUSED,
        }

        action = 'deffer'
        for key in submit_mapping.keys():
            if self.request.POST.get(key):
                action = key

        self.object = form.save(commit=False)
        self.object.eveniment = self.eveniment
        self.object.membru = self.request.user.utilizator.membru
        self.object.status_participare = submit_mapping.get(action)
        self.object.data_sosire = self.eveniment.start_date
        self.object.data_plecare = self.eveniment.end_date
        self.object.rol = RolParticipare.PARTICIPANT

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_detail", kwargs={"slug": self.eveniment.slug})

    def get_initial(self):
        data = super().get_initial()
        data['data_sosire'] = self.eveniment.start_date
        data['data_plecare'] = self.eveniment.end_date
        return data

    def get_object(self, queryset=None):
        try:
            membru = self.request.user.utilizator.membru
            return ParticipareEveniment.objects.get(eveniment=self.eveniment, membru=membru)
        except ParticipareEveniment.DoesNotExist:
            return None

