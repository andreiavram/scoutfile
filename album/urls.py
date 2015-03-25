from django.conf.urls import patterns
from album.models import AsociereEvenimentStructura
from album.views import AlbumEvenimentDetail, ZiDetail, PozaDetail, \
    RotateImage, EvenimentStats, ZiStats, FlagImage, EvenimentList, \
    SetImaginiUpload, SetImaginiDeleteAjax, SetImaginiToate, \
    SetImaginiUser, EvenimentSeturiUser, EvenimentSeturi, SetPozeUpdate, EvenimentCreate, EvenimentUpdate, EvenimentDetail, EvenimentDelete, PozaUpdate, ZiEdit, PozaDelete, ImagineTagSearch, ImagineSearchJSON, ZiDetailBeta, \
    RaportEvenimentDetail, RaportEvenimentUpdate, RaportEvenimentHistory, CalendarCentruLocal, CalendarEvents, \
    RaportStatus, RaportActivitate, RaportCompletPentruExport, AsociereEvenimentStructuraCreate, EvenimentParticipanti, \
    EvenimentParticipantiCreate, EvenimentParticipantiUpdate, UnitateEvenimentCreate, PatrulaEvenimentCreate, \
    EvenimentCampuriArbitrare, EvenimentCampuriArbitrareCreate, EvenimentCampuriArbitrareUpdate, PozaUpdateTags, \
    FlagImageAjax, EvenimentUpdateCampuriAditionale, EvenimentParticipantNonMembruCreate, \
    EvenimentParticipantNonMembruUpdate, EvenimentParticipantiExport, PozaVot, PozaMakeCover
from album.views import ChangeImagineVisibility


urlpatterns = patterns('album.views',
                       (r'eveniment/list/$', EvenimentList.as_view(), {}, "index"),
                       (r'eveniment/raport/status/$', RaportStatus.as_view(), {}, "raport_status"),
                       (r'eveniment/raport/export/$', RaportCompletPentruExport.as_view(), {}, "raport_export"),
                       (r'eveniment/(?P<slug>[\w\-]+)/album/$', AlbumEvenimentDetail.as_view(), {}, "eveniment_album"),
                       (r'eveniment/(?P<pk>\d+)/stats/$', EvenimentStats.as_view(), {}, "eveniment_stats"),
                       (r'eveniment/zi/(?P<pk>\d+)/$', ZiDetail.as_view(), {}, "zi_detail_old"),
                       (r'eveniment/zi/(?P<pk>\d+)/beta/k$', ZiDetailBeta.as_view(), {}, "zi_detail"),
                       (r'eveniment/zi/(?P<pk>\d+)/stats/$', ZiStats.as_view(), {}, "zi_stats"),
                       (r'eveniment/zi/(?P<pk>\d+)/edit/$', ZiEdit.as_view(), {}, "zi_edit"),
                       (r'eveniment/(?P<slug>[\w\-]+)/upload/$', SetImaginiUpload.as_view(), {}, "eveniment_upload"),
                       (r'eveniment/(?P<slug>[\w\-]+)/seturi/$', EvenimentSeturi.as_view(), {}, "eveniment_seturi_toate"),
                       (r'eveniment/(?P<slug>[\w\-]+)/mine/$', EvenimentSeturiUser.as_view(), {}, "eveniment_seturi_user"),
                       (r'eveniment/(?P<slug>[\w\-]+)/asocieri/$', AsociereEvenimentStructuraCreate.as_view(), {}, "eveniment_asociere_structura_create"),

                       (r'eveniment/(?P<pk>\d+)/calendar/$', CalendarCentruLocal.as_view(), {}, "calendar_centru_local"),
                       (r'eveniment/(?P<pk>\d+)/calendar/events/$', CalendarEvents.as_view(), {}, "events_centru_local"),

                       (r'eveniment/create/$', EvenimentCreate.as_view(), {}, "eveniment_create"),
                       (r'eveniment/unitate/(?P<pk>\d+)/create/$', UnitateEvenimentCreate.as_view(), {}, "unitate_eveniment_create"),
                       (r'eveniment/patrula/(?P<pk>\d+)/create/$', PatrulaEvenimentCreate.as_view(), {}, "patrula_eveniment_create"),
                       (r'eveniment/(?P<slug>[\w\-]+)/edit/$', EvenimentUpdate.as_view(), {}, "eveniment_update"),
                       (r'eveniment/(?P<slug>[\w\-]+)/delete/$', EvenimentDelete.as_view(), {}, "eveniment_delete"),
                       (r'eveniment/(?P<slug>[\w\-]+)/$', EvenimentDetail.as_view(), {}, "eveniment_detail"),

                       (r'eveniment/(?P<slug>[\w\-]+)/participanti/list/$', EvenimentParticipanti.as_view(), {}, "eveniment_participanti_list"),
                       (r'eveniment/(?P<slug>[\w\-]+)/participanti/adauga/$', EvenimentParticipantiCreate.as_view(), {}, "eveniment_participanti_adauga"),
                       (r'eveniment/participanti/(?P<pk>\d+)/modifica/$', EvenimentParticipantiUpdate.as_view(), {}, "eveniment_participanti_modifica"),
                       (r'eveniment/(?P<slug>[\w\-]+)/participanti/adauga/nonmembru/$', EvenimentParticipantNonMembruCreate.as_view(), {}, "eveniment_participanti_nonmembru_adauga"),
                       (r'eveniment/participanti/(?P<pk>\d+)/modifica/nonmembru/$', EvenimentParticipantNonMembruUpdate.as_view(), {}, "eveniment_participanti_nonmembru_modifica"),

                       (r'eveniment/(?P<slug>[\w\-]+)/campuri/$', EvenimentCampuriArbitrare.as_view(), {}, "eveniment_campuri_list"),
                       (r'eveniment/(?P<slug>[\w\-]+)/campuri/adauga/$', EvenimentCampuriArbitrareCreate.as_view(), {}, "eveniment_campuri_create"),
                       (r'eveniment/campuri/(?P<pk>\d+)/modifica/$', EvenimentCampuriArbitrareUpdate.as_view(), {}, "eveniment_campuri_update"),

                       (r'eveniment/(?P<slug>[\w\-]+)/participanti/export/$', EvenimentParticipantiExport.as_view(), {}, "eveniment_participanti_export"),

                       (r'eveniment/(?P<slug>[\w\-]+)/raport/$', RaportEvenimentDetail.as_view(), {}, "eveniment_raport_detail"),
                       (r'eveniment/(?P<slug>[\w\-]+)/raport/edit/$', RaportEvenimentUpdate.as_view(), {}, "eveniment_raport_update"),
                       (r'eveniment/(?P<slug>[\w\-]+)/raport/history/$', RaportEvenimentHistory.as_view(), {}, "eveniment_raport_history"),
                       (r'eveniment/(?P<slug>[\w\-]+)/raport/final/$', RaportActivitate.as_view(), {}, "eveniment_raport_complet"),
                       (r'eveniment/(?P<slug>[\w\-]+)/updatecampuri/$', EvenimentUpdateCampuriAditionale.as_view(), {}, "eveniment_camp_update"),

                       (r'set/(?P<pk>\d+)/$', SetPozeUpdate.as_view(), {}, "set_poze_edit"),
                       (r'set/(?P<pk>\d+)/delete/$', SetImaginiDeleteAjax.as_view(), {}, "set_poze_delete_ajax"),
                       (r'set/mine/$', SetImaginiUser.as_view(), {}, "set_poze_user"),
                       (r'set/all/$', SetImaginiToate.as_view(), {}, "set_poze_all"),

                       (r'poza/(?P<pk>\d+)/$', PozaDetail.as_view(), {}, "poza_detail"),
                       (r'poza/(?P<pk>\d+)/rotate/$', RotateImage.as_view(), {}, "poza_rotate"),
                       (r'poza/(?P<pk>\d+)/flag/$', FlagImage.as_view(), {}, "poza_flag"),
                       (r'poza/flag/ajax/$', FlagImageAjax.as_view(), {}, "poza_flag_ajax"),
                       (r'poza/visibility/', ChangeImagineVisibility.as_view(), {}, "poza_visibility"),
                       (r'poza/(?P<pk>\d+)/edit/$', PozaUpdate.as_view(), {}, "poza_edit"),
                       (r'poza/(?P<pk>\d+)/delete/$', PozaDelete.as_view(), {}, "poza_delete"),
                       (r'poza/(?P<pk>\d+)/update_tags/$', PozaUpdateTags.as_view(), {}, "poza_update_tags"),
                       (r'poza/vote/$', PozaVot.as_view(), {}, "poza_vot"),
                       (r'poza/make_cover/$', PozaMakeCover.as_view(), {}, "poza_make_cover"),

                       (r'tag/search/$', ImagineTagSearch.as_view(), {}, "tag_search"),
                       (r'search/$', ImagineSearchJSON.as_view(), {}, "imagine_search_json"),
)
