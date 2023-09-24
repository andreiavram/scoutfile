from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin

from certificari.forms import CertificateForm
from certificari.models import Certificate
from structuri.decorators import allow_by_afiliere
from structuri.models import Membru


class MembruCertificateCreate(CreateView):
    model = Certificate
    template_name = "certificari/membru_certificate_form.html"
    form_class = CertificateForm

    @allow_by_afiliere([("Membru, Centru Local", "Membru Consiliul Centrului Local"), ("Membru, Centru Local", "Responsabil Safe from Harm")])
    def dispatch(self, request, *args, **kwargs):
        self.membru = get_object_or_404(Membru, id=kwargs.pop("pk"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.issued_to = self.membru
        self.object.save()

        messages.success(self.request, "Am adăugat certificatul pentru %s" % self.membru)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.membru.id}) + "#certificari"

    def get_context_data(self, **kwargs):
        kwargs.update({"object": self.membru, "target_object": self.membru})
        return super().get_context_data(**kwargs)


class MembruCertificateUpdate(UpdateView):
    model = Certificate
    template_name = "certificari/membru_certificate_form.html"
    form_class = CertificateForm

    @allow_by_afiliere([("Membru, Centru Local", "Membru Consiliul Centrului Local"), ("Membru, Centru Local", "Responsabil Safe from Harm")])
    def dispatch(self, request, *args, **kwargs):
        self.membru = get_object_or_404(Membru, id=kwargs.pop("pk"))
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return reverse("structuri:membru_detail", kwargs={"pk": self.object.issued_to.id}) + "#certificari"

    def get_context_data(self, **kwargs):
        kwargs.update({"object": self.object.issued_to, "target_object": self.object.issued_to})
        return super().get_context_data(**kwargs)

