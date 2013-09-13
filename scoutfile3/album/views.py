# coding: utf-8
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from album.models import Eveniment, ZiEveniment, Imagine, FlagReport
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse,\
    HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest
from django.core.urlresolvers import reverse
import datetime
from album.forms import ReportForm
from django.contrib import messages
from django.views.generic.list import ListView
from album.models import SetPoze
from album.forms import SetPozeCreateForm, SetPozeUpdateForm
import simplejson
import logging
import os
from settings import MEDIA_ROOT, STATIC_URL
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from structuri.models import Membru
from generic.views import JSONView, ScoutFileAjaxException

logger = logging.getLogger(__name__)

class EvenimentList(ListView):
    model = Eveniment
    template_name = "album/eveniment_list.html"
    
    def get_queryset(self, *args, **kwargs):
        return super(EvenimentList, self).get_queryset(*args, **kwargs)
    

class EvenimentDetail(DetailView):
    model = Eveniment
    template_name = "album/eveniment_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.GET.has_key("autor"):
            self.autor = request.GET['autor']
        else:
            self.autor = None
        
        return super(EvenimentDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        current = super(EvenimentDetail, self).get_context_data(*args, **kwargs)
        
        zile = {}
        for zi_eveniment in self.object.zieveniment_set.all():
            zile[zi_eveniment] = zi_eveniment.filter_photos(autor = self.autor)
        
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
        
        object_list = self.object.filter_photos(autor = self.autor)
        current.update({"object_list" :  object_list, "autor" : self.autor})
        
        return current

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
        return super(PozaDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        current = super(PozaDetail, self).get_context_data(*args, **kwargs)

        import random
        current.update({"random_value" : random.randrange(1000, 2000)})
        current.update({"next_photo" : self.object.get_next_photo(autor = self.autor), "prev_photo" : self.object.get_prev_photo(autor = self.autor)})
        current.update({"autor" : self.autor })
        
        backward_limit = datetime.datetime.combine(self.object.get_day().date, datetime.time(0, 0, 0)) + datetime.timedelta(hours = 3)
        photo = Imagine.objects.filter(set_poze__eveniment = self.object.set_poze.eveniment, data__lt = self.object.data, data__gte = backward_limit)
        if self.autor != None:
            photo = photo.filter(set_poze__autor__icontains = self.autor)

        zi_page = ((photo.count()) / 30) + 1
        current.update({"zi_page" : zi_page})
        return current

class PozaUpdate(UpdateView):
    model = Imagine
    template_name = "album/poza_form.html"
    
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

    
    def dispatch(self, request, *args, **kwargs):
        self.eveniment = get_object_or_404(Eveniment, slug = kwargs.pop("slug"))
        return super(SetImaginiUpload, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        logger.debug("%s - form valid" % self.__class__.__name__)
        self.object = form.save(commit = False)

        from structuri.models import Membru
        self.object.autor_user = Membru.objects.get(id = self.request.user.get_profile().id)

        if not self.object.autor:
            self.object.autor = "%s" % self.object.autor_user.nume_complet()

        self.object.eveniment = self.eveniment
        
        #    have this in mind when migrated to chunked uploads!
        self.object.status = 1
        self.object.save()
        
        f = self.request.FILES.get('zip_file')
        
        data = {"files" : [{'name': f.name, 
                 'url': self.object.zip_file.url, 
                 'thumbnail_url': STATIC_URL + "album/zip.png",
                 'size' : os.stat(MEDIA_ROOT + "%s" % self.object.zip_file).st_size,
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
        from structuri.models import Membru
        logger.debug("%s: user is superuser: %s, user is same membru object %s" % (self.__class__.__name__, request.user.is_superuser, Membru.objects.get(id = request.user.get_profile().id) == self.set_poze.autor_user))
        if request.user.is_superuser or Membru.objects.get(id = request.user.get_profile().id) == self.set_poze.autor_user:
            try:
                os.unlink(MEDIA_ROOT + "%s" % self.set_poze.zip_file)
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
        return super(SetImaginiToate, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.model.objects.all()
    
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
        if self.autor_user_id != request.user.get_profile().id:
            return HttpResponseNotAllowed()
        return super(SetPozeUpdate, self).dispatch(request, *args, **kwargs)
    
    
    def form_valid(self, form):
        messages.success(self.request, "Actualizări salvate!")
        
    
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
        if int(value) not in range(1,5):
            raise ScoutFileAjaxException(extra_message = "The status is invalid")
        return int(value)
    
    def post(self, request, *args, **kwargs):
        self.validate(**self.parse_json_data())
        
        self.cleaned_data['imagine'].published_status = self.cleaned_data['new_status']
        self.cleaned_data['imagine'].save()
        
        return HttpResponse(self.construct_json_response(result = True))
    
    def construct_json_response(self, **kwargs):
        json_dict = {"result" : kwargs.get("result", False)}
        return simplejson.dumps(json_dict)
    
    