from django.conf.urls.defaults import patterns
from generic.views import TagsJson
from generic.views import GenericDeleteJavaScript,\
    GenericTabDeleteJavaScript


urlpatterns = patterns('generic.views',
   (r'js/(?P<app_label>\w+)/(?P<model>\w+)/delete.js$', GenericDeleteJavaScript.as_view(), {}, "js_delete"),
   (r'js/tabs/(?P<app_label>\w+)/(?P<model>\w+)/delete.js$', GenericTabDeleteJavaScript.as_view(), {}, "js_tab_delete"),
    (r'ajax/tags/$', TagsJson.as_view(), {}, "tag_list"),
)
