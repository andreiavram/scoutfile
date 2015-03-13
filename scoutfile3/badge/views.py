#coding: utf-8
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from album.models import Imagine
from album.views import FileUploadMixin
from badge.forms import BadgeForm
from badge.models import Badge


class BadgeList(ListView):
    template_name = "badge/badge_list.html"
    model = Badge


class BadgeFileUploadMixin(FileUploadMixin):
    def save_badge_photo(self, save=True):
        cover_photo_args = dict(form_field_name="poza", object_field_name="poza_badge", image_class=Imagine, folder_path="badgeuri")
        cover_photo_args['save'] = save
        self.save_photo(**cover_photo_args)


class BadgeCreate(BadgeFileUploadMixin, CreateView):
    template_name = "badge/badge_form.html"
    model = Badge
    form_class = BadgeForm

    @method_decorator(user_passes_test(lambda u: u.get_profile().membru.is_lider()))
    def dispatch(self, request, *args, **kwargs):
        return super(BadgeCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user.get_profile().membru
        self.save_badge_photo(save=False)
        self.object.save()

        return super(BadgeCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse("badge:badge_detail", kwargs={"pk": self.object.id})


class BadgeUpdate(BadgeFileUploadMixin, UpdateView):
    template_name = "badge/badge_form.html"
    model = Badge
    form_class = BadgeForm

    @method_decorator(user_passes_test(lambda u: u.get_profile().membru.is_lider()))
    def dispatch(self, request, *args, **kwargs):
        return super(BadgeUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.save_badge_photo(save=False)
        self.object.save()
        return super(BadgeUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("badge:badge_detail", kwargs={"pk": self.object.id})


class BadgeDetail(DetailView):
    template_name = "badge/badge_detail.html"
    model = Badge

