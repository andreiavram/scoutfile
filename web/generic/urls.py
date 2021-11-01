from goodies.views import TagsJson
from goodies.views import GenericDeleteJavaScript, \
    GenericTabDeleteJavaScript
from django.urls import path

urlpatterns = [
    path(r'js/<str:app_label>/<str:model>/delete.js', GenericDeleteJavaScript.as_view(), name="js_delete"),
    path(r'js/tabs/<str:app_label>/<str:model>/delete.js', GenericTabDeleteJavaScript.as_view(), name="js_tab_delete"),
    path(r'ajax/tags/', TagsJson.as_view(), name="tag_list"),
]
