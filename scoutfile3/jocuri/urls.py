#coding: utf8
from django.conf.urls.defaults import patterns
from jocuri.views import ActivitateUpdate, ActivitateDetail, ActivitateCreate, ActivitateSearch

urlpatterns = patterns('jocuri.views',
    (r'cauta/$', ActivitateSearch.as_view(), {}, "activitate_search"),
    (r'adauga/$', ActivitateCreate.as_view(), {}, "activitate_create"),
    (r'(?P<pk>\d+)/$', ActivitateDetail.as_view(), {}, "activitate_detail"),
    (r'(?P<pk>\d+)/$', ActivitateUpdate.as_view(), {}, "activitate_edit"),
)
