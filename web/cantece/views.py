#coding: utf-8
import string

import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView
from unidecode import unidecode

from cantece.models import Cantec, CarteCantece
from cantece.forms import CantecForm, CarteCanteceForm, CantecFileForm


class CantecList(ListView):
    model = Cantec
    template_name = "cantece/cantec_list.html"


class CantecCreate(CreateView):
    model = Cantec
    template_name = "cantece/cantec_form.html"
    form_class = CantecForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CantecCreate, self).dispatch(request, *args, **kwargs)

    def create_song_file(self):
        # make sure weird chars are going away from filename
        song_file_name = unidecode(self.object.titlu)

        # make filename valid
        valid_chars = "-_.()%s%s" % (string.ascii_letters, string.digits)
        song_file_name = ''.join(c for c in song_file_name if c in valid_chars)
        file_name = "%s.sg" % song_file_name
        file_path = os.path.join(settings.LOCAL_MEDIA_ROOT, "cartecantece", "cantece", file_name)

        # make sure we're not overwriting something that exists
        cnt = 1
        while os.path.exists(file_path):
            file_name = "%s-%d.sg" % (song_file_name, cnt)
            file_path = os.path.join(settings.LOCAL_MEDIA_ROOT, "cartecantece", "cantece", file_name)
            cnt += 1

        header = u"\\beginsong{%s}\n\t[by=%s,album=%s]\n\n" % (self.object.titlu, self.object.artist, self.object.album)
        header = header.encode('utf8', 'replace')
        with open(file_path, "w") as f:
            f.write(header)

        return file_path

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.nume_fisier = self.create_song_file()
        self.object.owner = self.request.user
        self.object.save()
        messages.success(self.request, u"Cântecul a fost adăugat")
        return super(CantecCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse("cantece:cantec_detail", kwargs={"pk": self.object.id})


class CantecEdit(UpdateView):
    model = Cantec
    template_name = "cantece/cantec_form.html"
    form_class = CantecForm

    def get_success_url(self):
        return reverse("cantece:cantec_detail", kwargs={"pk": self.object.id})


class CantecDetail(FormView):
    model = Cantec
    template_name = "cantece/cantec_detail.html"
    form_class = CantecFileForm

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Cantec, id=kwargs.pop("pk"))
        return super(CantecDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(CantecDetail, self).get_context_data(**kwargs)
        data['object'] = self.object
        return data

    def get_initial(self):
        data = super(CantecDetail, self).get_initial()
        with open(self.object.nume_fisier, "r") as f:
            data['song_content'] = f.read()
        return data

    def form_valid(self, form):
        with open(self.object.nume_fisier, "w") as f:
            f.write(form.cleaned_data['song_content'])

        messages.success(self.request, u"Modificările tale au fost salvate!")
        return super(CantecDetail, self).form_valid(form)

    def get_success_url(self):
        return reverse("cantece:cantec_detail", kwargs={"pk": self.object.id})


class CarteList(ListView):
    model = CarteCantece
    template_name = "cantece/cartecantece_list.html"


class CarteCreate(CreateView):
    model = CarteCantece
    template_name = "cantece/cartecantece_form.html"
    form_class = CarteCanteceForm


class CarteEdit(UpdateView):
    model = CarteCantece
    template_name = "cantece/cartecantece_form.html"
    form_class = CarteCanteceForm

class CarteDetail(DetailView):
    model = CarteCantece
    templatE_name = "cantece/cartecantece_detail.html"


