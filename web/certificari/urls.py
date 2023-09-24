from django.urls import path

from certificari.views import MembruCertificateCreate, MembruCertificateUpdate

urlpatterns = [
    path('membru/<int:pk>/certificate/adauga/', MembruCertificateCreate.as_view(), name="membru_add_certificate"),
    path('membru/<int:mpk>/certificate/<int:pk>/edit/', MembruCertificateUpdate.as_view(),
         name="membru_edit_certificate")
]
