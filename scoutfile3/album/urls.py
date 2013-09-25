from django.conf.urls.defaults import patterns
from album.views import AlbumEvenimentDetail, ZiDetail, PozaDetail,\
    RotateImage, EvenimentStats, ZiStats, FlagImage, EvenimentList, \
    SetImaginiUpload, SetImaginiDeleteAjax, SetImaginiToate,\
    SetImaginiUser, EvenimentSeturiUser, EvenimentSeturi, SetPozeUpdate, EvenimentCreate, EvenimentUpdate, EvenimentDetail, EvenimentDelete, PozaUpdate
from scoutfile3.album.views import ChangeImagineVisibility


urlpatterns = patterns('scoutfile3.album.views',
       (r'eveniment/list/$', EvenimentList.as_view(), {}, "index"),
       (r'eveniment/(?P<slug>\w+)/album/$', AlbumEvenimentDetail.as_view(), {}, "eveniment_detail"),
       (r'eveniment/(?P<pk>\d+)/stats/$', EvenimentStats.as_view(), {}, "eveniment_stats"),
       (r'eveniment/zi/(?P<pk>\d+)/$', ZiDetail.as_view(), {}, "zi_detail"),
       (r'eveniment/zi/(?P<pk>\d+)/stats/$', ZiStats.as_view(), {}, "zi_stats"),
       (r'eveniment/(?P<slug>\w+)/upload/$', SetImaginiUpload.as_view(), {}, "eveniment_upload"),
       (r'eveniment/(?P<slug>\w+)/seturi/$', EvenimentSeturi.as_view(), {}, "eveniment_seturi_toate"),
       (r'eveniment/(?P<slug>\w+)/mine/$', EvenimentSeturiUser.as_view(), {}, "eveniment_seturi_user"),

       (r'eveniment/create/$', EvenimentCreate.as_view(), {}, "eveniment_create"),
       (r'eveniment/(?P<slug>\w+)/edit/$', EvenimentUpdate.as_view(), {}, "eveniment_update"),
       (r'eveniment/(?P<slug>\w+)/delete/$', EvenimentDelete.as_view(), {}, "eveniment_delete"),
       (r'eveniment/(?P<slug>\w+)/$', EvenimentDetail.as_view(), {}, "eveniment_main_detail"),

       (r'set/(?P<pk>\d+)/$', SetPozeUpdate.as_view(), {}, "set_poze_edit"),
       (r'set/(?P<pk>\d+)/delete/$', SetImaginiDeleteAjax.as_view(), {}, "set_poze_delete_ajax"),
       (r'set/mine/$', SetImaginiUser.as_view(), {}, "set_poze_user"),
       (r'set/all/$', SetImaginiToate.as_view(), {}, "set_poze_all"),

       (r'poza/(?P<pk>\d+)/$', PozaDetail.as_view(), {}, "poza_detail"),
       (r'poza/(?P<pk>\d+)/rotate/$', RotateImage.as_view(), {}, "poza_rotate"),
       (r'poza/(?P<pk>\d+)/flag/$', FlagImage.as_view(), {}, "poza_flag"),
       (r'poza/visibility/', ChangeImagineVisibility.as_view(), {}, "poza_visibility"),
       (r'poza/(?P<pk>\d+)/edit/$', PozaUpdate.as_view(), {}, "poza_edit"),
)
