# coding: utf-8
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect, HttpResponse,\
    HttpResponseForbidden, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
import datetime
from django.contrib import messages
from django.views.generic.list import ListView
import simplejson
import logging
import os
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from album.models import Eveniment, ZiEveniment, Imagine, FlagReport
from album.forms import ReportForm, EvenimentCreateForm, EvenimentUpdateForm, PozaTagsForm, ZiForm
from album.models import SetPoze
from album.forms import SetPozeCreateForm, SetPozeUpdateForm
from generic.views import GenericDeleteView
from scoutfile3.structuri.models import Membru
from scoutfile3.generic.views import JSONView, ScoutFileAjaxException
from scoutfile3.album.models import IMAGINE_PUBLISHED_STATUS
from scoutfile3.structuri.models import TipAsociereMembruStructura
from scoutfile3.structuri.decorators import allow_by_afiliere

logger = logging.getLogger(__name__)

class EvenimentList(ListView):
    model = Eveniment
    template_name = "album/eveniment_list.html"
    
    def get_queryset(self, *args, **kwargs):
        return super(EvenimentList, self).get_queryset(*args, **kwargs)
    

class AlbumEvenimentDetail(DetailView):
    model = Eveniment
    template_name = "album/eveniment_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        self.autor = request.GET['autor'] if "autor" in request.GET else None
        return super(AlbumEvenimentDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        current = super(AlbumEvenimentDetail, self).get_context_data(*args, **kwargs)
        
        zile = {}
        for zi_eveniment in self.object.zieveniment_set.all():
            zile[zi_eveniment] = zi_eveniment.filter_photos(autor=self.autor, user=self.request.user)
        
        current.update({"zile" : zile, "autor" : self.autor})
        
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
        current.update({"object_list":  object_list, "autor" : self.autor,
                        "visibility_states": IMAGINE_PUBLISHED_STATUS})

        centru_local = self.object.eveniment.centru_local
        calitate = TipAsociereMembruStructura.objects.get(nume__iexact = u"Păstrător al amintirilor", content_types__in = [ContentType.objects.get_for_model(centru_local)])
        if self.request.user.get_profile().membru.are_calitate(calitate, centru_local):
            current.update({"media_manager": True})

        return current

class ZiEdit(UpdateView):
    model = ZiEveniment
    template_name = "album/zi_form.html"
    form_class = ZiForm

    def dispatch(self, request, *args, **kwargs):
        return super(ZiEdit, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("album:zi_detail", kwargs={"pk" : self.object.id})

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
        current.update({"random_value" : random.randrange(1000, 2000)})
        current.update({"next_photo" : self.object.get_next_photo(autor=self.autor, user=self.request.user),
                        "prev_photo" : self.object.get_prev_photo(autor=self.autor, user=self.request.user)})
        current.update({"autor" : self.autor })
        
        backward_limit = datetime.datetime.combine(self.object.get_day().date, datetime.time(0, 0, 0)) + datetime.timedelta(hours = 3)
        photo = Imagine.objects.filter(set_poze__eveniment = self.object.set_poze.eveniment, data__lt = self.object.data, data__gte = backward_limit)
        if self.autor is not None:
            photo = photo.filter(set_poze__autor__icontains = self.autor)

        zi_page = ((photo.count()) / 30) + 1
        current.update({"zi_page" : zi_page})
        current.update({"visibility_states": IMAGINE_PUBLISHED_STATUS})

        centru_local = self.object.set_poze.eveniment.centru_local
        calitate = TipAsociereMembruStructura.objects.get(nume__iexact = u"Păstrător al amintirilor", content_types__in = [ContentType.objects.get_for_model(centru_local)])
        if self.request.user.get_profile().membru.are_calitate(calitate, centru_local):
            current.update({"media_manager": True})

        return current

class PozaUpdate(UpdateView):
    model = Imagine
    template_name = "album/poza_form.html"
    form_class = PozaTagsForm

    #TODO: add authentication verification here (who can edit these things?)

    def form_valid(self, form):
        self.object.tags.clear()
        messages.success(self.request, u"Modificări salvate")
        return super(PozaUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("album:poza_detail", kwargs = {"pk": self.object.id})
    
class FlagImage(CreateView):
    model = FlagReport
    template_name = "album/poza_flag.html"
    form_class = ReportForm
    
    def dispatch(self, *args, **kwargs):
        self.poza = get_object_or_404(Imagine, id = kwargs.pop("pk"))
        return super(FlagImage, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.imagine = self.poza
        self.object.save()
        messages.success(self.request, "Poza a fost flag-uită, un lider sau fotograful vor decide ce acțiune se va lua în continuare")
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse("album:poza_detail", kwargs = {"pk" : self.poza.id})
    
    def get_context_data(self, *args, **kwargs):
        current = super(FlagImage, self).get_context_data(*args, **kwargs)
        
        current.update({"poza" : self.poza})
        
        return current

class RotateImage(View):
    def dispatch(self, request, *args, **kwargs):
        self.imagine = get_object_or_404(Imagine, id = kwargs.pop("pk"))
        
        if not request.GET.has_key("direction"):
            raise Http404
        
        self.direction = request.GET.get("direction")
        if self.direction not in ("cw", "ccw"):
            raise Http404
        
        return super(RotateImage, self).dispatch(request, *args, **kwargs)
    
    def get(self, *args, **kwargs):
        self.imagine.rotate(self.direction)
        return HttpResponseRedirect(reverse("album:poza_detail", kwargs = {"pk" : self.imagine.id}))
    
    
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
                fp.write("\0" * int(byte_ranges[2]))

        with io.open(local_file_name, "a+b") as destination:
            destination.seek(int(byte_ranges[0]))
            for chunk in f.chunks():
                destination.write(chunk)

    @allow_by_afiliere([("Eveniment, Centru Local", "Lider")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug = kwargs.get("slug"))
        return super(SetImaginiUpload, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        logger.debug("%s - form valid" % self.__class__.__name__)

        import re
        byte_ranges = re.findall(r"bytes (\d+)-(\d+)/(\d+)", self.request.META['HTTP_CONTENT_RANGE'])
        logger.debug("%s - byte ranges %s to %s out of %s" % (self.__class__.__name__, byte_ranges[0][0], byte_ranges[0][1], byte_ranges[0][2]))
        f = self.request.FILES.get('zip_file')

        session_key = "{0}-{1}".format(self.request.user.id, f.name.replace("-", "+"))
        if session_key in self.request.session:
            self.object = get_object_or_404(self.model, id = int(self.request.session[session_key]))
            logger.debug("%s - retrieving existing set (%d)" % (self.__class__.__name__, self.object.id))
        else:
            self.object = form.save(commit = False)
            from scoutfile3.structuri.models import Membru
            self.object.autor_user = Membru.objects.get(id = self.request.user.get_profile().id)

            if not self.object.autor:
                self.object.autor = "%s" % self.object.autor_user.nume_complet()

            self.object.eveniment = self.eveniment
            self.object.zip_file = "/" + os.path.join("tmp", "{0}_{1}_{2}".format(self.request.user.id, datetime.datetime.now().strftime("%Y%m%d%H%M%S"), f.name))
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

        data = {"files" : [{'name': f.name, 
                 #'url': self.object.zip_file.url,
                 #'thumbnail_url': STATIC_URL + "album/zip.png",
                 'size' : int(byte_ranges[0][2]),
                 'type' :  "application/zip",
                 #'descriere' : self.object.descriere, 
                 'delete_url': "http" + ("s" if self.request.is_secure() else "") + "://" + self.request.get_host() + reverse("album:set_poze_delete_ajax", kwargs = {"pk" : self.object.id}), 
                 'delete_type': "DELETE"}]}
        
        response = HttpResponse(simplejson.dumps(data), mimetype = self.response_mimetype())
        return response

    def form_invalid(self, form):
        logger.debug("%s - form invalid (%s)" % (self.__class__.__name__, form.errors))
        logger.debug("%s - POST data (%s)" % (self.__class__.__name__, self.request.POST))
#         data = [{"error" : u"Cannot upload", "error_dict" : form.errors}]
        
        f = self.request.FILES.get('zip_file')
        data = {"files" : [{"name" : f.name, "error" : u"Cannot upload"}]}
        
        response = HttpResponse(simplejson.dumps(data), mimetype = self.response_mimetype())
        return response

    def get_context_data(self, **kwargs):
        current = super(SetImaginiUpload, self).get_context_data(**kwargs)
        current.update({"eveniment" : self.eveniment})
        return current
        
        
class SetImaginiDeleteAjax(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.set_poze = get_object_or_404(SetPoze, id = kwargs.pop("pk"))
        return super(SetImaginiDeleteAjax, self).dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        from scoutfile3.structuri.models import Membru
        logger.debug("%s: user is superuser: %s, user is same membru object %s" % (self.__class__.__name__, request.user.is_superuser, Membru.objects.get(id = request.user.get_profile().id) == self.set_poze.autor_user))
        if request.user.is_superuser or Membru.objects.get(id = request.user.get_profile().id) == self.set_poze.autor_user:
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
        return self.model.objects.filter(eveniment__centru_local = self.membru.centru_local)

    def get_context_data(self, **kwargs):
        current = super(SetImaginiToate, self).get_context_data(**kwargs)
        current.update({"media_manager" : self.membru.are_calitate(u"Păstrător al amintirilor", self.membru.centru_local)})
        return current

class SetImaginiUser(SetImaginiToate):
    def get_queryset(self):
        qs = super(SetImaginiUser, self).get_queryset()
        qs = qs.filter(autor_user = Membru.objects.get(id = self.request.user.get_profile().id))
        return qs

    def get_context_data(self, **kwargs):
        current = super(SetImaginiUser, self).get_context_data(**kwargs)
        current.update({"user_only" : True})
        return current
    
class EvenimentSeturi(SetImaginiToate):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug = kwargs.get("slug"))
        return super(EvenimentSeturi, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = super(EvenimentSeturi, self).get_queryset()
        qs = qs.filter(eveniment = self.eveniment)
        return qs
    
    def get_context_data(self, **kwargs):
        current = super(EvenimentSeturi, self).get_context_data(**kwargs)
        current.update({"eveniment" : self.eveniment})
        return current
    
class EvenimentSeturiUser(EvenimentSeturi):
    def get_queryset(self):
        qs = super(EvenimentSeturiUser, self).get_queryset()
        qs = qs.filter(autor_user = Membru.objects.get(id = self.request.user.get_profile().id))
        return qs
    
    def get_context_data(self, **kwargs):
        current = super(SetImaginiUser, self).get_context_data(**kwargs)
        current.update({"user_only" : True})
        return current
    

class SetPozeUpdate(UpdateView):
    model = SetPoze
    form_class = SetPozeUpdateForm
    template_name = "album/set_poze_edit.html"

    @method_decorator(login_required)    
    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, id = kwargs.get("pk"))
        if self.object.autor_user_id != request.user.get_profile().id:
            return HttpResponseNotAllowed()
        return super(SetPozeUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Actualizări salvate!")
        return super(SetPozeUpdate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse("album:set_poze_edit", kwargs = {"pk" : self.object.id})


class ChangeImagineVisibility(JSONView):
    _params = {"imagine" : {"type" : "required"},
               "new_status" : {"type" : "required"}}

    def clean_imagine(self, value):
        try:
            return Imagine.objects.get(id = int(value))
        except Exception, e:
            raise ScoutFileAjaxException(extra_message = "This image does not exist", exception = e)
    
    def clean_new_status(self, value):
        #TODO: change this from range to actual valid values
        if int(value) not in range(1,5):
            raise ScoutFileAjaxException(extra_message = "The status is invalid")
        return int(value)
    
    def post(self, request, *args, **kwargs):
        self.validate(**self.parse_json_data())

        centru_local = self.cleaned_data['imagine'].set_poze.eveniment.centru_local
        calitate = TipAsociereMembruStructura.objects.get(nume__iexact = u"Păstrător al amintirilor", content_types__in = [ContentType.objects.get_for_model(centru_local)])
        if not self.request.user.get_profile().membru.are_calitate(calitate, centru_local) and not self.request.user.is_superuser:
            return HttpResponseForbidden()

        self.cleaned_data['imagine'].published_status = self.cleaned_data['new_status']
        self.cleaned_data['imagine'].save()
        
        return HttpResponse(self.construct_json_response(result = True, imagine = self.cleaned_data['imagine']))
    
    def construct_json_response(self, **kwargs):
        json_dict = {"result" : kwargs.get("result", False), "new_status_string" : kwargs.get("imagine").get_published_status_display()}
        return simplejson.dumps(json_dict)

class EvenimentCreate(CreateView):
    model = Eveniment
    form_class = EvenimentCreateForm
    template_name = "album/eveniment_form.html"

    @allow_by_afiliere([("Utilizator, Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        self.centru_local = request.user.utilizator.membru.centru_local
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.centru_local = self.centru_local
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("album:eveniment_detail", kwargs = {"slug": self.object.slug})

class EvenimentUpdate(UpdateView):
    model = Eveniment
    form_class = EvenimentUpdateForm
    template_name = "album/eveniment_form.html"

    @allow_by_afiliere([("Centru Local", "Lider")])
    def dispatch(self, request, *args, **kwargs):
        return super(EvenimentUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, u"Evenimentul a fost actualizat")
        #   make sure tags will be recreated - this is a bit lazy and can be improved
        self.object.tags.clear()
        return super(EvenimentUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("album:eveniment_detail", kwargs = {"slug": self.object.slug})

class EvenimentDelete(GenericDeleteView):
    model = Eveniment

    @allow_by_afiliere([("Eveniment, Centru Local", u"Păstrător al amintirilor")], pkname="slug")
    def dispatch(self, request, *args, **kwargs):
        return super(EvenimentDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("album:index")

class EvenimentDetail(DetailView):
    model = Eveniment
    template_name = "album/eveniment_main_detail.html"
