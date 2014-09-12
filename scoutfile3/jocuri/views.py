# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from taggit.models import Tag
from jocuri.forms import FisaActivitateForm
from jocuri.models import FisaActivitate, CategorieFiseActivitate


class ActivitateSearch(ListView):
    model = FisaActivitate
    template_name = "jocuri/fisaactivitate_list.html"

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

    def get_queryset(self):
        qs = super(ActivitateSearch, self).get_queryset()
        if self.requested_category_id:
            qs = qs.filter(categorie_id=self.requested_category_id)
        if self.requested_tag_id:
            qs = qs.filter(tags__in=[Tag.objects.get(id=self.requested_tag_id)])
        return qs

    def get_context_data(self, **kwargs):
        data = super(ActivitateSearch, self).get_context_data(**kwargs)
        data['tag'] = self.tag
        data['categorie'] = self.category
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
        self.object.save()
        return super(ActivitateUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("jocuri:activitate_detail", kwargs={"pk": self.object.id})


class ActivitateDetail(DetailView):
    model = FisaActivitate
    template_name = "jocuri/fisaactivitate_detail.html"