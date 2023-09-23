from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView

from locuri.forms import GPXTrackForm
from locuri.models import GPXTrack


class LocuriDashboard(TemplateView):
    template_name = "locuri/dashboard.html"

    def get_context_data(self, **kwargs):
        track_cnt = GPXTrack.objects.all().count()
        context = super().get_context_data(**kwargs)
        context.update({
            "track_cnt": track_cnt
        })
        return context

class GPXTrackList(ListView):
    model = GPXTrack
    template_name = "locuri/gpx_track_list.html"


class GPXTrackDetail(DetailView):
    model = GPXTrack
    template_name = "locuri/gpx_track_detail.html"


class GPXTrackCreate(CreateView):
    model = GPXTrack
    template_name = "locuri/gpx_track_form.html"
    form_class = GPXTrackForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("locuri:gpx_track_list")


class GPXTrackEdit(UpdateView):
    model = GPXTrack
    template_name = "locuri/gpx_track_form.html"
    form_class = GPXTrackForm

    def get_success_url(self):
        return reverse("locuri:gpx_track_list")
