from django.conf.urls.defaults import patterns
from scoutfile3.album.views import EvenimentDetail, ZiDetail, PozaDetail,\
    RotateImage, EvenimentStats, ZiStats, FlagImage, EvenimentList


urlpatterns = patterns('scoutfile3.album.views',
       (r'eveniment/list/$', EvenimentList.as_view(), {}, "index"),
       (r'eveniment/(?P<slug>\w+)/$', EvenimentDetail.as_view(), {}, "eveniment_detail"),
       (r'eveniment/(?P<pk>\d+)/stats/$', EvenimentStats.as_view(), {}, "eveniment_stats"),
       (r'eveniment/zi/(?P<pk>\d+)/$', ZiDetail.as_view(), {}, "zi_detail"),
       (r'eveniment/zi/(?P<pk>\d+)/stats/$', ZiStats.as_view(), {}, "zi_stats"),

       (r'poza/(?P<pk>\d+)/$', PozaDetail.as_view(), {}, "poza_detail"),
       (r'poza/(?P<pk>\d+)/rotate/$', RotateImage.as_view(), {}, "poza_rotate"),
       (r'poza/(?P<pk>\d+)/flag/$', FlagImage.as_view(), {}, "poza_flag"),
)
