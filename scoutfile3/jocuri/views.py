# Create your views here.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from jocuri.forms import FisaActivitateForm
from jocuri.models import FisaActivitate


class ActivitateSearch(ListView):
    model = FisaActivitate
    template_name = "jocuri/fisaactivitate_list.html"


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

    def get_success_url(self):
        return reverse("jocuri:activitate_detail", kwargs={"pk": self.object.id})


class ActivitateDetail(DetailView):
    model = FisaActivitate
    template_name = "jocuri/fisaactivitate_detail.html"