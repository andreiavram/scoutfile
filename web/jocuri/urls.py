# coding: utf8
from django.urls import path
from jocuri.views import ActivitateUpdate, ActivitateDetail, ActivitateCreate, ActivitateSearch, DocumentActivitateList, \
    DocumentActivitateAdauga

urlpatterns = [
    path('<int:pk>/edit/', ActivitateUpdate.as_view(), name="activitate_edit"),
    path('<int:pk>/', ActivitateDetail.as_view(), name="activitate_detail"),
    path('<int:pk>/documente/', DocumentActivitateList.as_view(), name="activitate_documents"),
    path('<int:pk>/documente/adauga/', DocumentActivitateAdauga.as_view(), name="activitate_document_create"),
    path('cauta/', ActivitateSearch.as_view(), name="activitate_search"),
    path('adauga/', ActivitateCreate.as_view(), name="activitate_create"),
]
