from django.urls import path, include
from album.views import AlbumEvenimentDetail, ZiDetail, PozaDetail, \
    RotateImage, EvenimentStats, ZiStats, FlagImage, EvenimentList, \
    SetImaginiUpload, SetImaginiDeleteAjax, SetImaginiToate, \
    SetImaginiUser, EvenimentSeturiUser, EvenimentSeturi, SetPozeUpdate, EvenimentCreate, EvenimentUpdate, \
    EvenimentDetail, EvenimentDelete, PozaUpdate, ZiEdit, PozaDelete, ImagineTagSearch, ImagineSearchJSON, ZiDetailBeta, \
    RaportEvenimentDetail, RaportEvenimentUpdate, RaportEvenimentHistory, CalendarCentruLocal, CalendarEvents, \
    RaportStatus, RaportActivitate, RaportCompletPentruExport, AsociereEvenimentStructuraCreate, EvenimentParticipanti, \
    EvenimentParticipantiCreate, EvenimentParticipantiUpdate, UnitateEvenimentCreate, PatrulaEvenimentCreate, \
    EvenimentCampuriArbitrare, EvenimentCampuriArbitrareCreate, EvenimentCampuriArbitrareUpdate, PozaUpdateTags, \
    FlagImageAjax, EvenimentUpdateCampuriAditionale, EvenimentParticipantNonMembruCreate, \
    EvenimentParticipantNonMembruUpdate, EvenimentParticipantiExport, PozaVot, PozaMakeCover, EventContributionList, \
    EventContributionCreate, EventContributionUpdate, EventPaymentCreate, EventDocumentsView, EventLinkCreate, \
    EventLinkUpdate, EventLinkList
from album.views import ChangeImagineVisibility

urlpatterns = [
    path('eveniment/list/', EvenimentList.as_view(), name="index"),
    path('eveniment/raport/status/', RaportStatus.as_view(), name="raport_status"),
    path('eveniment/raport/export/', RaportCompletPentruExport.as_view(), name="raport_export"),
    path('eveniment/<slug:slug>/album/', AlbumEvenimentDetail.as_view(), name="eveniment_album"),
    path('eveniment/<int:pk>/stats/', EvenimentStats.as_view(), name="eveniment_stats"),
    path('eveniment/zi/<int:pk>/', ZiDetail.as_view(), name="zi_detail_old"),
    path('eveniment/zi/<int:pk>/beta/', ZiDetailBeta.as_view(), name="zi_detail"),
    path('eveniment/zi/<int:pk>/stats/', ZiStats.as_view(), name="zi_stats"),
    path('eveniment/zi/<int:pk>/edit/', ZiEdit.as_view(), name="zi_edit"),
    path('eveniment/<slug:slug>/upload/', SetImaginiUpload.as_view(), name="eveniment_upload"),
    path('eveniment/<slug:slug>/seturi/', EvenimentSeturi.as_view(), name="eveniment_seturi_toate"),
    path('eveniment/<slug:slug>/mine/', EvenimentSeturiUser.as_view(), name="eveniment_seturi_user"),
    path('eveniment/<slug:slug>/asocieri/', AsociereEvenimentStructuraCreate.as_view(),
         name="eveniment_asociere_structura_create"),

    path('eveniment/<int:pk>/calendar/', CalendarCentruLocal.as_view(), name="calendar_centru_local"),
    path('eveniment/<int:pk>/calendar/events/', CalendarEvents.as_view(), name="events_centru_local"),

    path('eveniment/create/', EvenimentCreate.as_view(), name="eveniment_create"),
    path('eveniment/unitate/<int:pk>/create/', UnitateEvenimentCreate.as_view(), name="unitate_eveniment_create"),
    path('eveniment/patrula/<int:pk>/create/', PatrulaEvenimentCreate.as_view(), name="patrula_eveniment_create"),
    path('eveniment/<slug:slug>/edit/', EvenimentUpdate.as_view(), name="eveniment_update"),
    path('eveniment/<slug:slug>/delete/', EvenimentDelete.as_view(), name="eveniment_delete"),
    path('eveniment/<slug:slug>/', EvenimentDetail.as_view(), name="eveniment_detail"),
    path('eveniment/<slug:slug>/documents/', EventDocumentsView.as_view(), name="eveniment_documents"),

    path('eveniment/<slug:slug>/participanti/list/', EvenimentParticipanti.as_view(),
         name="eveniment_participanti_list"),
    path('eveniment/<slug:slug>/participanti/adauga/', EvenimentParticipantiCreate.as_view(),
         name="eveniment_participanti_adauga"),
    path('eveniment/participanti/<int:pk>/modifica/', EvenimentParticipantiUpdate.as_view(),
         name="eveniment_participanti_modifica"),
    path('eveniment/<slug:slug>/participanti/adauga/nonmembru/', EvenimentParticipantNonMembruCreate.as_view(),
         name="eveniment_participanti_nonmembru_adauga"),
    path('eveniment/participanti/<int:pk>/modifica/nonmembru/', EvenimentParticipantNonMembruUpdate.as_view(),
         name="eveniment_participanti_nonmembru_modifica"),

    path('eveniment/<slug:slug>/campuri/', EvenimentCampuriArbitrare.as_view(), name="eveniment_campuri_list"),
    path('eveniment/<slug:slug>/campuri/adauga/', EvenimentCampuriArbitrareCreate.as_view(),
         name="eveniment_campuri_create"),
    path('eveniment/campuri/<int:pk>/modifica/', EvenimentCampuriArbitrareUpdate.as_view(),
         name="eveniment_campuri_update"),

    path('eveniment/<slug:slug>/tipcontributii/', EventContributionList.as_view(), name="eveniment_tipcontributii_list"),
    path('eveniment/<slug:slug>/tipcontributii/adauga/', EventContributionCreate.as_view(), name="eveniment_tipcontributii_create"),
    path('eveniment/tipcontributii/<int:pk>/modifica/', EventContributionUpdate.as_view(), name="eveniment_tipcontributii_update"),

    path('eveniment/<slug:slug>/urls/', EventLinkList.as_view(), name="eveniment_url_list"),
    path('eveniment/<slug:slug>/urls/adauga/', EventLinkCreate.as_view(), name="eveniment_url_create"),
    path('eveniment/urls/<int:pk>/modifica/', EventLinkUpdate.as_view(), name="eveniment_url_update"),

    path('eveniment/participanti/<int:pk>/plata/', EventPaymentCreate.as_view(), name="eveniment_payment"),

    path('eveniment/<slug:slug>/participanti/export/', EvenimentParticipantiExport.as_view(),
         name="eveniment_participanti_export"),

    path('eveniment/<slug:slug>/raport/', RaportEvenimentDetail.as_view(), name="eveniment_raport_detail"),
    path('eveniment/<slug:slug>/raport/edit/', RaportEvenimentUpdate.as_view(), name="eveniment_raport_update"),
    path('eveniment/<slug:slug>/raport/history/', RaportEvenimentHistory.as_view(),
         name="eveniment_raport_history"),
    path('eveniment/<slug:slug>/raport/final/', RaportActivitate.as_view(), name="eveniment_raport_complet"),
    path('eveniment/<slug:slug>/updatecampuri/', EvenimentUpdateCampuriAditionale.as_view(),
         name="eveniment_camp_update"),

    path('set/<int:pk>/', SetPozeUpdate.as_view(), name="set_poze_edit"),
    path('set/<int:pk>/delete/', SetImaginiDeleteAjax.as_view(), name="set_poze_delete_ajax"),
    path('set/mine/', SetImaginiUser.as_view(), name="set_poze_user"),
    path('set/all/', SetImaginiToate.as_view(), name="set_poze_all"),

    path('poza/<int:pk>/', PozaDetail.as_view(), name="poza_detail"),
    path('poza/<int:pk>/rotate/', RotateImage.as_view(), name="poza_rotate"),
    path('poza/<int:pk>/flag/', FlagImage.as_view(), name="poza_flag"),
    path('poza/flag/ajax/', FlagImageAjax.as_view(), name="poza_flag_ajax"),
    path('poza/visibility/', ChangeImagineVisibility.as_view(), name="poza_visibility"),
    path('poza/<int:pk>/edit/', PozaUpdate.as_view(), name="poza_edit"),
    path('poza/<int:pk>/delete/', PozaDelete.as_view(), name="poza_delete"),
    path('poza/<int:pk>/update_tags/', PozaUpdateTags.as_view(), name="poza_update_tags"),
    path('poza/vote/', PozaVot.as_view(), name="poza_vot"),
    path('poza/make_cover/', PozaMakeCover.as_view(), name="poza_make_cover"),

    path('tag/search/', ImagineTagSearch.as_view(), name="tag_search"),
    path('search/', ImagineSearchJSON.as_view(), name="imagine_search_json"),
]
