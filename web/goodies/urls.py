__author__ = 'andrei'

from django.urls import path
from goodies.views import TagsJson, GenericDeleteAPI
from goodies.views import GenericDeleteJavaScript, \
    GenericTabDeleteJavaScript

urlpatterns = [
    path('js/<str:app_label>/<str:model>/delete.js', GenericDeleteJavaScript.as_view(), name="js_delete"),
    path('js/tabs/<str:app_label>/<str:model>/delete.js', GenericTabDeleteJavaScript.as_view(),
         name="js_tab_delete"),
    path('js/generic/delete', GenericDeleteAPI.as_view(), name="js_ajax_delete"),
    path('ajax/tags/', TagsJson.as_view(), name="tag_list"),
]
