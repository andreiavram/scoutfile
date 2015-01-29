#coding: utf8
from django.conf.urls import patterns
from documente.views import DeclaratieCotizatieSocialaAdauga, DeclaratieCotizatieSocialaModifica, MembruAlteDocumente
from structuri.views import CentruLocalCreate, CentruLocalUpdate,\
    CentruLocalDetail, CentruLocalList, CentruLocalMembruCreate,\
    CentruLocalMembruAsociaza, CentruLocalTabBrief, CentruLocalTabUnitati,\
    CentruLocalTabLideri, CentruLocalTabMembri, CentruLocalUnitateCreate,\
    UnitateUpdate, UnitateDetail, UnitateTabBrief, UnitateTabMembri,\
    UnitateTabPatrule, UnitateMembruCreate, UnitateMembruAsociaza,\
    UnitatePatrulaCreate, PatrulaUpdate, PatrulaDetail, PatrulaTabBrief,\
    PatrulaTabMembri, PatrulaMembruCreate, PatrulaMembruAsociaza, MembruUpdate,\
    MembruDetail, MembruCard, MembruProgresPersonal, MembruTabBrief,\
    MembruTabConexiuni, MembruTabIstoric, CentruLocalDelete, UnitateDelete,\
    RegisterMembru, ConfirmMembruRegistration, CentruLocalMembriPending,\
    ForgotPassword, ChangePassword, ConfirmMembruAdmin, ConfirmForgotPassword,\
    UtilizatorHome, UtilizatorEditProfile, UtilizatorEditProfilePicture,\
    UtilizatorHomeTabsBrief, UtilizatorHomeTabsAfiliere, CentruLocalLiderCreate,\
    UnitateLiderCreate, AsociereCreate, AsociereUpdate, PatrulaDelete,\
    CentruLocalMembri, CentruLocalTabContact, CentruLocalContactCreate,\
    ContactUpdate, ContactDelete, MembruContactCreate, CentruLocalContactUpdate,\
    MembruContactUpdate, MembruTabContact, MembruEditProfilePicture,\
    MembruAddFamilie, MembruEditFamilie, MembruTabFamilie,\
    MembruPersoanaDeContactCreate, MembruPersoanaDeContactUpdate,\
    MembriForPatrocle, MembruDestinatarRepr, PersoanaContactDestinatarRepr,\
    MembriFaraAfilieri, GetSpeedList, MembruTabDocumente, SetariSpecialeCentruLocal, MembruConfirmaFacebook, \
    UnitateTabMembriFaraPatrula, MembruTabActivitati, MembruRecalculeazaAcoperire, UnitateTabPatruleInactive, \
    UtilizatorHomeTabsDocumente, UtilizatorHomeTabsActivitati, MembruStergeAcoperire, CentruLocalTabMembriDeSuspendat, \
    MembruAdreseStatus

urlpatterns = patterns('structuri.views',
    (r'centrulocal/adauga/$', CentruLocalCreate.as_view(), {}, "cl_add"),
    (r'centrulocal/(?P<pk>\d+)/schimba/$', CentruLocalUpdate.as_view(), {}, "cl_edit"),
    (r'centrulocal/(?P<pk>\d+)/schimba/special/$', SetariSpecialeCentruLocal.as_view(), {}, "cl_edit_special"),
    (r'centrulocal/(?P<pk>\d+)/$', CentruLocalDetail.as_view(), {}, "cl_detail"),
    (r'centrulocal/list/$', CentruLocalList.as_view(), {}, "cl_list"),
    (r'centrulocal/(?P<pk>\d+)/sterge/$', CentruLocalDelete.as_view(), {}, "cl_delete"),
    
    (r'centrulocal/(?P<pk>\d+)/membri/pending/$', CentruLocalMembriPending.as_view(), {}, "cl_membri_pending"),
    
    (r'centrulocal/(?P<pk>\d+)/membru/adauga/$', CentruLocalMembruCreate.as_view(), {}, "cl_membru_add"),
    (r'centrulocal/(?P<pk>\d+)/lider/adauga/$', CentruLocalLiderCreate.as_view(), {}, "cl_lider_add"),
    (r'centrulocal/membru/asociaza/$', CentruLocalMembruAsociaza.as_view(), {}, "cl_membru_asociaza"),
    
    (r'centrulocal/(?P<pk>\d+)/tab/brief/$', CentruLocalTabBrief.as_view(), {}, "cl_tab_brief"),
    (r'centrulocal/(?P<pk>\d+)/tab/unitati/$', CentruLocalTabUnitati.as_view(), {}, "cl_tab_unitati"),
    (r'centrulocal/(?P<pk>\d+)/tab/lideri/$', CentruLocalTabLideri.as_view(), {}, "cl_tab_lideri"),
    (r'centrulocal/(?P<pk>\d+)/tab/contact/$', CentruLocalTabContact.as_view(), {}, "cl_tab_contact"),
    (r'centrulocal/(?P<pk>\d+)/tab/membri/$', CentruLocalTabMembri.as_view(), {}, "cl_tab_membri"),
    (r'centrulocal/(?P<pk>\d+)/tab/membri/de_suspendat/$', CentruLocalTabMembriDeSuspendat.as_view(), {}, "cl_tab_membri_de_suspendat"),
    
    (r'centrulocal/(?P<pk>\d+)/membri/$', CentruLocalMembri.as_view(), {}, "cl_membri"),
    (r'centrulocal/(?P<pk>\d+)/contact/add/$', CentruLocalContactCreate.as_view(), {}, "cl_contact_add"),
    (r'centrulocal/contact/(?P<pk>\d+)/edit/$', CentruLocalContactUpdate.as_view(), {}, "cl_contact_edit"),
    
#     (r'centrulocal/(?P<pk>\d+)/documente/cotizatii/$', CentruLocalCotizatii.as_view(), {}, "cl_cotizatii"),
#     (r'centrulocal/(?P<pk>\d+)/documente/registre/$', CentruLocalRegistre.as_view(), {}, "cl_registre"),
#     (r'centrulocal/(?P<pk>\d+)/documente/altele/$', CentruLocalAlteDocumente.as_view(), {}, "cl_alte_documente"),
    
    (r'centrulocal/(?P<pk>\d+)/unitate/adauga/$', CentruLocalUnitateCreate.as_view(), {}, "cl_unitate_add"),
    (r'centrulocal/unitate/(?P<pk>\d+)/schimba/$', UnitateUpdate.as_view(), {}, "unitate_edit"),
    (r'centrulocal/unitate/(?P<pk>\d+)/$', UnitateDetail.as_view(), {}, "unitate_detail"),
    (r'centrulocal/unitate/(?P<pk>\d+)/sterge/$', UnitateDelete.as_view(), {}, "unitate_delete"),
    
    (r'centrulocal/unitate/(?P<pk>\d+)/tab/brief/$', UnitateTabBrief.as_view(), {}, "unitate_tab_brief"),
    (r'centrulocal/unitate/(?P<pk>\d+)/tab/patrule/$', UnitateTabPatrule.as_view(), {}, "unitate_tab_patrule"),
    (r'centrulocal/unitate/(?P<pk>\d+)/tab/patrule/inactive/$', UnitateTabPatruleInactive.as_view(), {}, "unitate_tab_patrule_inactive"),
    (r'centrulocal/unitate/(?P<pk>\d+)/tab/membri/$', UnitateTabMembri.as_view(), {}, "unitate_tab_membri"),
    (r'centrulocal/unitate/(?P<pk>\d+)/tab/membri/farapatrula/$', UnitateTabMembriFaraPatrula.as_view(), {}, "unitate_tab_membri_fara_patrula"),
    
    (r'centrulocal/unitate/(?P<pk>\d+)/membru/adauga/$', UnitateMembruCreate.as_view(), {}, "unitate_membru_add"),
    (r'centrulocal/unitate/(?P<pk>\d+)/membru/asociaza/$', UnitateMembruAsociaza.as_view(), {}, "unitate_membru_asociaza"),
    
    (r'centrulocal/unitate/(?P<pk>\d+)/patrula/adauga/$', UnitatePatrulaCreate.as_view(), {}, "unitate_patrula_add"),
    (r'centrulocal/unitate/patrula/(?P<pk>\d+)/edit/$', PatrulaUpdate.as_view(), {}, 'patrula_edit'),
    (r'centrulocal/unitate/patrula/(?P<pk>\d+)/$', PatrulaDetail.as_view(), {}, 'patrula_detail'),
    
    (r'centrulocal/unitate/patrula/(?P<pk>\d+)/tab/brief/$', PatrulaTabBrief.as_view(), {}, 'patrula_tab_brief'),
    (r'centrulocal/unitate/patrula/(?P<pk>\d+)/tab/membri/$', PatrulaTabMembri.as_view(), {}, 'patrula_tab_membri'),
    
    (r'centrulocal/unitate/patrula/(?P<pk>\d+)/membru/adauga/$', PatrulaMembruCreate.as_view(), {}, 'patrula_membru_adauga'),
    (r'centrulocal/unitate/patrula/(?P<pk>\d+)/membru/asociaza/$', PatrulaMembruAsociaza.as_view(), {}, 'patrula_membru_asociaza'),
    (r'centrulocal/unitate/patrula/(?P<pk>\d+)/delete/$', PatrulaDelete.as_view(), {}, "patrula_delete"),

    (r'centrulocal/unitate/(?P<pk>\d+)/membru/adauga/$', UnitateMembruCreate.as_view(), {}, "unitate_membru_add"),
    (r'centrulocal/unitate/(?P<pk>\d+)/lider/adauga/$', UnitateLiderCreate.as_view(), {}, "unitate_lider_add"),
    
    (r'membru/(?P<pk>\d+)/schimba/$', MembruUpdate.as_view(), {}, "membru_edit"),
    (r'membru/(?P<pk>\d+)/$', MembruDetail.as_view(), {}, "membru_detail"),
    (r'membru/(?P<pk>\d+)/card/$', MembruCard.as_view(), {}, "membru_card"),
    (r'membru/(?P<pk>\d+)/progres_personal/$', MembruProgresPersonal.as_view(), {}, "membru_pp"),
    
    
    (r'membru/(?P<pk>\d+)/tab/brief/$', MembruTabBrief.as_view(), {}, "membru_tab_brief"),
    (r'membru/(?P<pk>\d+)/tab/conexiuni/$', MembruTabConexiuni.as_view(), {}, "membru_tab_afilieri"),
    (r'membru/(?P<pk>\d+)/tab/istoric/$', MembruTabIstoric.as_view(), {}, "membru_tab_istoric"),
    (r'membru/(?P<pk>\d+)/tab/contact/$', MembruTabContact.as_view(), {}, "membru_tab_contact"),
    (r'membru/(?P<pk>\d+)/tab/familie/$', MembruTabFamilie.as_view(), {}, "membru_tab_familie"),
    (r'membru/(?P<pk>\d+)/tab/documente/$', MembruTabDocumente.as_view(), {}, "membru_tab_documente"),
    (r'membru/(?P<pk>\d+)/tab/activitati/$', MembruTabActivitati.as_view(), {}, "membru_tab_activitati"),
    
    (r'membru/(?P<pk>\d+)/recalculeaza_acoperire/$', MembruRecalculeazaAcoperire.as_view(), {}, "membru_recalculeaza_acoperire"),
    (r'membru/(?P<pk>\d+)/reseteaza_acoperire/$', MembruStergeAcoperire.as_view(), {}, "membru_reseteaza_acoperire"),
    (r'membru/(?P<pk>\d+)/contact/add/$', MembruContactCreate.as_view(), {}, "membru_contact_add"),
    (r'membru/contact/(?P<pk>\d+)/edit/$', MembruContactUpdate.as_view(), {}, "membru_contact_edit"),
    (r'membru/(?P<pk>\d+)/picture/$', MembruEditProfilePicture.as_view(), {}, "membru_admin_edit_profile_picture"),
    
    (r'membru/inregistrare/$', RegisterMembru.as_view(), {}, "membru_register"),
    (r'membru/inregistrare/confirmare/(?P<hash>[0-9a-zA-Z]+)/', ConfirmMembruRegistration.as_view(), {}, "membru_confirm_registration"),
    (r'membru/(?P<pk>\d+)/adminconfirm/$', ConfirmMembruAdmin.as_view(), {}, "membru_confirm_admin"),
    (r'membru/inregistrare/resetpassword/$', ForgotPassword.as_view(), {}, "membru_forgot_password"),
    (r'membru/inregistrare/resetpassword/(?P<hash>[0-9a-zA-Z]+)/$', ConfirmForgotPassword.as_view(), {}, "membru_confirm_forgot_password"),
    (r'membru/changepassword/$', ChangePassword.as_view(), {}, "membru_change_password"),
    
    (r'membru/profile/$', UtilizatorHome.as_view(), {}, "membru_profil"),
    (r'membru/profile/tab/brief/$', UtilizatorHomeTabsBrief.as_view(), {}, "membru_profil_tab_brief"),
    (r'membru/profile/tab/afiliere/$', UtilizatorHomeTabsAfiliere.as_view(), {}, "membru_profil_tab_afiliere"),
    (r'membru/profile/tab/activitati/$', UtilizatorHomeTabsActivitati.as_view(), {}, "membru_profil_tab_activitati"),
    (r'membru/profile/tab/documente/$', UtilizatorHomeTabsDocumente.as_view(), {}, "membru_profil_tab_documente"),

    (r'membru/profile/edit/$', UtilizatorEditProfile.as_view(), {}, "membru_edit_profile"),
    (r'membru/profile/edit/picture/$', UtilizatorEditProfilePicture.as_view(), {}, "membru_edit_profile_picture"),
    
    (r'membru/(?P<pk>\d+)/afiliere/adauga/$', AsociereCreate.as_view(), {}, "membru_afiliere_add"),
    (r'membru/afiliere/(?P<pk>\d+)/modifica/$', AsociereUpdate.as_view(), {}, "membru_afiliere_edit"),
    
    (r'membru/(?P<pk>\d+)/familie/adauga/$', MembruAddFamilie.as_view(), {}, "membru_add_familie"),
    (r'membru/(?P<mpk>\d+)/(?P<pk>\d+)/familie/edit/$', MembruEditFamilie.as_view(), {}, "membru_edit_familie"),
    (r'membru/(?P<pk>\d+)/pdc/adauga/$', MembruPersoanaDeContactCreate.as_view(), {}, "membru_add_pdc"),
    (r'membru/(?P<mpk>\d+)/pdc/(?P<pk>\d+)/edit/$', MembruPersoanaDeContactUpdate.as_view(), {}, "membru_edit_pdc"),

    (r'membru/(?P<pk>\d+)/alte_documente/$', MembruAlteDocumente.as_view(), {}, "membru_alte_documente"),
    (r'membru/(?P<pk>\d+)/cotizatie-sociala/adauga/$', DeclaratieCotizatieSocialaAdauga.as_view(), {}, "membru_cotizatiesociala_adauga"),
    (r'membru/cotizatie-sociala/(?P<pk>\d+)/modifica/$', DeclaratieCotizatieSocialaModifica.as_view(), {}, "membru_cotizatiesociala_modifica"),

    (r'membru/fb/confirm/$', MembruConfirmaFacebook.as_view(), {}, "membru_confirma_facebook"),


    (r'ajax/membri/list/$', MembriForPatrocle.as_view(), {}, "ajax_patrocle_membri"),   
    (r'ajax/membri/detail/$', MembruDestinatarRepr.as_view(), {}, "ajax_membru_detail"), 
    (r'ajax/persoanacontact/detail/$', PersoanaContactDestinatarRepr.as_view(), {}, "ajax_persoana_contact_detail"),
    #(r'contact/(?P<pk>\d+)/delete/$', ContactDelete.as_view(), {}, "contact_delete"),
    
    (r'membru/list/lost/$', MembriFaraAfilieri.as_view(), {}, "membri_pierduti_list"),
    (r'ajax/speeddial/$', GetSpeedList.as_view(), {}, "speedlist"),

    (r'adrese/status/$', MembruAdreseStatus.as_view(), {}, "membru_adrese_status"),
    
)
