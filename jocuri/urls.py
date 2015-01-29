#coding: utf8
from django.conf.urls import patterns
from jocuri.views import ActivitateUpdate, ActivitateDetail, ActivitateCreate, ActivitateSearch, DocumentActivitateList, \
    DocumentActivitateAdauga

urlpatterns = patterns('jocuri.views',
    (r'(?P<pk>\d+)/edit/$', ActivitateUpdate.as_view(), {}, "activitate_edit"),
    (r'(?P<pk>\d+)/$', ActivitateDetail.as_view(), {}, "activitate_detail"),
    (r'(?P<pk>\d+)/documente/$', DocumentActivitateList.as_view(), {}, "activitate_documents"),
    (r'(?P<pk>\d+)/documente/adauga/$', DocumentActivitateAdauga.as_view(), {}, "activitate_document_create"),
    (r'cauta/$', ActivitateSearch.as_view(), {}, "activitate_search"),
    (r'adauga/$', ActivitateCreate.as_view(), {}, "activitate_create"),

)
