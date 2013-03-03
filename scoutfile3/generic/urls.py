from django.conf.urls.defaults import patterns
from scoutfile3.generic.views import GenericDeleteJavaScript,\
    GenericTabDeleteJavaScript


urlpatterns = patterns('scoutfile3.generic.views',
   (r'js/(?P<app_label>\w+)/(?P<model>\w+)/delete.js$', GenericDeleteJavaScript.as_view(), {}, "js_delete"),
   (r'js/tabs/(?P<app_label>\w+)/(?P<model>\w+)/delete.js$', GenericTabDeleteJavaScript.as_view(), {}, "js_tab_delete"),
)
