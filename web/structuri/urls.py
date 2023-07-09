# coding: utf8
from django.urls import path, include
from documente.views import DeclaratieCotizatieSocialaAdauga, DeclaratieCotizatieSocialaModifica, MembruAlteDocumente
from structuri.views import CentruLocalCreate, CentruLocalUpdate, \
    CentruLocalDetail, CentruLocalList, CentruLocalMembruCreate, \
    CentruLocalMembruAsociaza, CentruLocalTabBrief, CentruLocalTabUnitati, \
    CentruLocalTabLideri, CentruLocalTabMembri, CentruLocalUnitateCreate, \
    UnitateUpdate, UnitateDetail, UnitateTabBrief, UnitateTabMembri, \
    UnitateTabPatrule, UnitateMembruCreate, UnitateMembruAsociaza, \
    UnitatePatrulaCreate, PatrulaUpdate, PatrulaDetail, PatrulaTabBrief, \
    PatrulaTabMembri, PatrulaMembruCreate, PatrulaMembruAsociaza, MembruUpdate, \
    MembruDetail, MembruCard, MembruProgresPersonal, MembruTabBrief, \
    MembruTabConexiuni, MembruTabIstoric, CentruLocalDelete, UnitateDelete, \
    RegisterMembru, ConfirmMembruRegistration, CentruLocalMembriPending, \
    ForgotPassword, ChangePassword, ConfirmMembruAdmin, ConfirmForgotPassword, \
    UtilizatorHome, UtilizatorEditProfile, UtilizatorEditProfilePicture, \
    UtilizatorHomeTabsBrief, UtilizatorHomeTabsAfiliere, CentruLocalLiderCreate, \
    UnitateLiderCreate, AsociereCreate, AsociereUpdate, PatrulaDelete, \
    CentruLocalMembri, CentruLocalTabContact, CentruLocalContactCreate, \
    MembruContactCreate, CentruLocalContactUpdate, \
    MembruContactUpdate, MembruTabContact, MembruEditProfilePicture, \
    MembruAddFamilie, MembruEditFamilie, MembruTabFamilie, \
    MembruPersoanaDeContactCreate, MembruPersoanaDeContactUpdate, \
    MembriForPatrocle, MembruDestinatarRepr, PersoanaContactDestinatarRepr, \
    MembriFaraAfilieri, GetSpeedList, MembruTabDocumente, SetariSpecialeCentruLocal, MembruConfirmaFacebook, \
    UnitateTabMembriFaraPatrula, MembruTabActivitati, MembruRecalculeazaAcoperire, UnitateTabPatruleInactive, \
    UtilizatorHomeTabsDocumente, UtilizatorHomeTabsActivitati, MembruStergeAcoperire, CentruLocalTabMembriDeSuspendat, \
    MembruAdreseStatus, UnitatiListAPI, UpdateContentObjects, MembruInformatieCreate, MembruInformatieUpdate, \
    MembruTabAlteInformatii, ListaMembriiDreptVot, ListaMembriiDreptVotCentruLocal, MembruTabPlatiCotizatie

urlpatterns = [
    path('centrulocal/adauga/', CentruLocalCreate.as_view(), name="cl_add"),
    path('centrulocal/<int:pk>/schimba/', CentruLocalUpdate.as_view(), name="cl_edit"),
    path('centrulocal/<int:pk>/schimba/special/', SetariSpecialeCentruLocal.as_view(), name="cl_edit_special"),
    path('centrulocal/<int:pk>/', CentruLocalDetail.as_view(), name="cl_detail"),
    path('centrulocal/list/', CentruLocalList.as_view(), name="cl_list"),
    path('centrulocal/<int:pk>/sterge/', CentruLocalDelete.as_view(), name="cl_delete"),

    path('centrulocal/<int:pk>/membri/pending/', CentruLocalMembriPending.as_view(), name="cl_membri_pending"),

    path('centrulocal/<int:pk>/membru/adauga/', CentruLocalMembruCreate.as_view(), name="cl_membru_add"),
    path('centrulocal/<int:pk>/lider/adauga/', CentruLocalLiderCreate.as_view(), name="cl_lider_add"),
    path('centrulocal/membru/asociaza/', CentruLocalMembruAsociaza.as_view(), name="cl_membru_asociaza"),

    path('centrulocal/<int:pk>/tab/brief/', CentruLocalTabBrief.as_view(), name="cl_tab_brief"),
    path('centrulocal/<int:pk>/tab/unitati/', CentruLocalTabUnitati.as_view(), name="cl_tab_unitati"),
    path('centrulocal/<int:pk>/tab/lideri/', CentruLocalTabLideri.as_view(), name="cl_tab_lideri"),
    path('centrulocal/<int:pk>/tab/contact/', CentruLocalTabContact.as_view(), name="cl_tab_contact"),
    path('centrulocal/<int:pk>/tab/membri/', CentruLocalTabMembri.as_view(), name="cl_tab_membri"),
    path('centrulocal/<int:pk>/tab/membri/de_suspendat/', CentruLocalTabMembriDeSuspendat.as_view(),
         name="cl_tab_membri_de_suspendat"),

    path('centrulocal/<int:pk>/membri/', CentruLocalMembri.as_view(), name="cl_membri"),
    path('centrulocal/<int:pk>/contact/add/', CentruLocalContactCreate.as_view(), name="cl_contact_add"),
    path('centrulocal/contact/<int:pk>/edit/', CentruLocalContactUpdate.as_view(), name="cl_contact_edit"),

    #     path('centrulocal/<int:pk>/documente/cotizatii/', CentruLocalCotizatii.as_view(), name="cl_cotizatii"),
    #     path('centrulocal/<int:pk>/documente/registre/', CentruLocalRegistre.as_view(), name="cl_registre"),
    #     path('centrulocal/<int:pk>/documente/altele/', CentruLocalAlteDocumente.as_view(), name="cl_alte_documente"),

    path('centrulocal/<int:pk>/unitate/adauga/', CentruLocalUnitateCreate.as_view(), name="cl_unitate_add"),
    path('centrulocal/unitate/<int:pk>/schimba/', UnitateUpdate.as_view(), name="unitate_edit"),
    path('centrulocal/unitate/<int:pk>/', UnitateDetail.as_view(), name="unitate_detail"),
    path('centrulocal/unitate/<int:pk>/sterge/', UnitateDelete.as_view(), name="unitate_delete"),

    path('centrulocal/unitate/<int:pk>/tab/brief/', UnitateTabBrief.as_view(), name="unitate_tab_brief"),
    path('centrulocal/unitate/<int:pk>/tab/patrule/', UnitateTabPatrule.as_view(), name="unitate_tab_patrule"),
    path('centrulocal/unitate/<int:pk>/tab/patrule/inactive/', UnitateTabPatruleInactive.as_view(),
         name="unitate_tab_patrule_inactive"),
    path('centrulocal/unitate/<int:pk>/tab/membri/', UnitateTabMembri.as_view(), name="unitate_tab_membri"),
    path('centrulocal/unitate/<int:pk>/tab/membri/farapatrula/', UnitateTabMembriFaraPatrula.as_view(),
         name="unitate_tab_membri_fara_patrula"),

    path('centrulocal/unitate/<int:pk>/membru/adauga/', UnitateMembruCreate.as_view(), name="unitate_membru_add"),
    path('centrulocal/unitate/<int:pk>/membru/asociaza/', UnitateMembruAsociaza.as_view(),
         name="unitate_membru_asociaza"),

    path('centrulocal/unitate/<int:pk>/patrula/adauga/', UnitatePatrulaCreate.as_view(), name="unitate_patrula_add"),
    path('centrulocal/unitate/patrula/<int:pk>/edit/', PatrulaUpdate.as_view(), {}, 'patrula_edit'),
    path('centrulocal/unitate/patrula/<int:pk>/', PatrulaDetail.as_view(), {}, 'patrula_detail'),

    path('centrulocal/unitate/patrula/<int:pk>/tab/brief/', PatrulaTabBrief.as_view(), {}, 'patrula_tab_brief'),
    path('centrulocal/unitate/patrula/<int:pk>/tab/membri/', PatrulaTabMembri.as_view(), {}, 'patrula_tab_membri'),

    path('centrulocal/unitate/patrula/<int:pk>/membru/adauga/', PatrulaMembruCreate.as_view(), {},
         'patrula_membru_adauga'),
    path('centrulocal/unitate/patrula/<int:pk>/membru/asociaza/', PatrulaMembruAsociaza.as_view(), {},
         'patrula_membru_asociaza'),
    path('centrulocal/unitate/patrula/<int:pk>/delete/', PatrulaDelete.as_view(), name="patrula_delete"),

    path('centrulocal/unitate/<int:pk>/membru/adauga/', UnitateMembruCreate.as_view(), name="unitate_membru_add"),
    path('centrulocal/unitate/<int:pk>/lider/adauga/', UnitateLiderCreate.as_view(), name="unitate_lider_add"),

    path('membru/<int:pk>/schimba/', MembruUpdate.as_view(), name="membru_edit"),
    path('membru/<int:pk>/', MembruDetail.as_view(), name="membru_detail"),
    path('membru/<int:pk>/card/', MembruCard.as_view(), name="membru_card"),
    path('membru/<int:pk>/progres_personal/', MembruProgresPersonal.as_view(), name="membru_pp"),

    path('membru/<int:pk>/tab/brief/', MembruTabBrief.as_view(), name="membru_tab_brief"),
    path('membru/<int:pk>/tab/conexiuni/', MembruTabConexiuni.as_view(), name="membru_tab_afilieri"),
    path('membru/<int:pk>/tab/istoric/', MembruTabIstoric.as_view(), name="membru_tab_istoric"),
    path('membru/<int:pk>/tab/contact/', MembruTabContact.as_view(), name="membru_tab_contact"),
    path('membru/<int:pk>/tab/alteinfo/', MembruTabAlteInformatii.as_view(), name="membru_tab_altele"),
    path('membru/<int:pk>/tab/familie/', MembruTabFamilie.as_view(), name="membru_tab_familie"),
    path('membru/<int:pk>/tab/documente/', MembruTabDocumente.as_view(), name="membru_tab_documente"),
    path('membru/<int:pk>/tab/activitati/', MembruTabActivitati.as_view(), name="membru_tab_activitati"),
    path('membru/<int:pk>/tab/platicotizatie/', MembruTabPlatiCotizatie.as_view(), name="membru_tab_plati_cotizatie"),

    path('membru/<int:pk>/recalculeaza_acoperire/', MembruRecalculeazaAcoperire.as_view(),
         name="membru_recalculeaza_acoperire"),
    path('membru/<int:pk>/reseteaza_acoperire/', MembruStergeAcoperire.as_view(), name="membru_reseteaza_acoperire"),
    path('membru/<int:pk>/contact/add/', MembruContactCreate.as_view(), name="membru_contact_add"),
    path('membru/contact/<int:pk>/edit/', MembruContactUpdate.as_view(), name="membru_contact_edit"),
    path('membru/<int:pk>/alteinfo/add/', MembruInformatieCreate.as_view(), name="membru_altele_add"),
    path('membru/alteinfo/<int:pk>/edit/', MembruInformatieUpdate.as_view(), name="membru_altele_edit"),
    path('membru/<int:pk>/picture/', MembruEditProfilePicture.as_view(), name="membru_admin_edit_profile_picture"),

    path('membru/inregistrare/', RegisterMembru.as_view(), name="membru_register"),
    path('membru/inregistrare/confirmare/<str:hash>/', ConfirmMembruRegistration.as_view(),
         name="membru_confirm_registration"),
    path('membru/<int:pk>/adminconfirm/', ConfirmMembruAdmin.as_view(), name="membru_confirm_admin"),
    path('membru/inregistrare/resetpassword/', ForgotPassword.as_view(), name="membru_forgot_password"),
    path('membru/inregistrare/resetpassword/<str:hash>/', ConfirmForgotPassword.as_view(),
         name="membru_confirm_forgot_password"),
    path('membru/changepassword/', ChangePassword.as_view(), name="membru_change_password"),

    path('membru/profile/', UtilizatorHome.as_view(), name="membru_profil"),
    path('membru/profile/tab/brief/', UtilizatorHomeTabsBrief.as_view(), name="membru_profil_tab_brief"),
    path('membru/profile/tab/afiliere/', UtilizatorHomeTabsAfiliere.as_view(), name="membru_profil_tab_afiliere"),
    path('membru/profile/tab/activitati/', UtilizatorHomeTabsActivitati.as_view(), name="membru_profil_tab_activitati"),
    path('membru/profile/tab/documente/', UtilizatorHomeTabsDocumente.as_view(), name="membru_profil_tab_documente"),

    path('membru/profile/edit/', UtilizatorEditProfile.as_view(), name="membru_edit_profile"),
    path('membru/profile/edit/picture/', UtilizatorEditProfilePicture.as_view(), name="membru_edit_profile_picture"),

    path('membru/<int:pk>/afiliere/adauga/', AsociereCreate.as_view(), name="membru_afiliere_add"),
    path('membru/afiliere/<int:pk>/modifica/', AsociereUpdate.as_view(), name="membru_afiliere_edit"),

    path('membru/<int:pk>/familie/adauga/', MembruAddFamilie.as_view(), name="membru_add_familie"),
    path('membru/<int:mpk>/<int:pk>/familie/edit/', MembruEditFamilie.as_view(), name="membru_edit_familie"),
    path('membru/<int:pk>/pdc/adauga/', MembruPersoanaDeContactCreate.as_view(), name="membru_add_pdc"),
    path('membru/<int:mpk>/pdc/<int:pk>/edit/', MembruPersoanaDeContactUpdate.as_view(), name="membru_edit_pdc"),

    path('membru/<int:pk>/alte_documente/', MembruAlteDocumente.as_view(), name="membru_alte_documente"),
    path('membru/<int:pk>/cotizatie-sociala/adauga/', DeclaratieCotizatieSocialaAdauga.as_view(),
         name="membru_cotizatiesociala_adauga"),
    path('membru/cotizatie-sociala/<int:pk>/modifica/', DeclaratieCotizatieSocialaModifica.as_view(),
         name="membru_cotizatiesociala_modifica"),

    path('membru/fb/confirm/', MembruConfirmaFacebook.as_view(), name="membru_confirma_facebook"),

    path('ajax/membri/list/', MembriForPatrocle.as_view(), name="ajax_patrocle_membri"),
    path('ajax/membri/detail/', MembruDestinatarRepr.as_view(), name="ajax_membru_detail"),
    path('ajax/persoanacontact/detail/', PersoanaContactDestinatarRepr.as_view(), name="ajax_persoana_contact_detail"),
    # path('contact/<int:pk>/delete/', ContactDelete.as_view(), name="contact_delete"),
    path('membru/list/lost/', MembriFaraAfilieri.as_view(), name="membri_pierduti_list"),
    path('ajax/speeddial/', GetSpeedList.as_view(), name="speedlist"),

    path('adrese/status/', MembruAdreseStatus.as_view(), name="membru_adrese_status"),
    path('dreptvot/', ListaMembriiDreptVotCentruLocal.as_view(), name="membrii_drept_vot_full"),
    path('dreptvot/<str:rdv_slug>/', ListaMembriiDreptVot.as_view(), name="membrii_drept_vot"),

    path('api/get_unitati/', UnitatiListAPI.as_view(), name="get_unitati"),
    path('api/update_content_objects/', UpdateContentObjects.as_view(), name="update_content_objects")
]
