#coding: utf8
from django.conf.urls import patterns
from django.conf.urls import url

from cantece.views import CantecList, CantecCreate, CantecDetail, CantecEdit, CarteList, CarteCreate, CarteDetail, \
    CarteEdit

urlpatterns = patterns('cantece.views',
                       url(r'cantec/list/$', CantecList.as_view(), name="cantec_list"),
                       url(r'cantec/create/$', CantecCreate.as_view(), name="cantec_add"),
                       url(r'cantec/(?P<pk>\d+)/$', CantecDetail.as_view(), name="cantec_detail"),
                       url(r'cantec/(?P<pk>\d+)/edit/$', CantecEdit.as_view(), name="cantec_edit"),

                       url(r'carte/list/$', CarteList.as_view(), name="carte_list"),
                       url(r'carte/create/$', CarteCreate.as_view(), name="carte_add"),
                       url(r'carte/(?P<pk>\d+)/$', CarteDetail.as_view(), name="carte_detail"),
                       url(r'carte/(?P<pk>\d+)/edit/$', CarteEdit.as_view(), name="carte_edit"),
                       )
