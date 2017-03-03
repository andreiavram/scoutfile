#coding: utf8
from django.conf.urls import patterns
from django.conf.urls import url
from badge.views import BadgeList, BadgeCreate, BadgeDetail, BadgeUpdate

urlpatterns = patterns('badge.views',
                       url(r'adauga/$', BadgeCreate.as_view(), name="badge_add"),
                       url(r'(?P<pk>\d+)/$', BadgeDetail.as_view(), name="badge_detail"),
                       url(r'(?P<pk>\d+)/edit/$', BadgeUpdate.as_view(), name="badge_edit"),
                       url(r'$', BadgeList.as_view(), name="badge_list"),
                       )
