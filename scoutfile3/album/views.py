# coding: utf-8
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from scoutfile3.album.models import Eveniment, ZiEveniment, Imagine, FlagReport
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from scoutfile3.album.forms import ReportForm
from django.contrib import messages
from django.views.generic.list import ListView

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