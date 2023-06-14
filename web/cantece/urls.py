from django.urls import path

from cantece.views import CantecList, CantecCreate, CantecDetail, CantecEdit, CarteList, CarteCreate, CarteDetail, \
    CarteEdit

urlpatterns = [
    path('cantec/list/', CantecList.as_view(), name="cantec_list"),
    path('cantec/create/', CantecCreate.as_view(), name="cantec_add"),
    path('cantec/<int:pk>/', CantecDetail.as_view(), name="cantec_detail"),
    path('cantec/<int:pk>/edit/', CantecEdit.as_view(), name="cantec_edit"),

    path('carte/list/', CarteList.as_view(), name="carte_list"),
    path('carte/create/', CarteCreate.as_view(), name="carte_add"),
    path('carte/<int:pk>/', CarteDetail.as_view(), name="carte_detail"),
    path('carte/<int:pk>/edit/', CarteEdit.as_view(), name="carte_edit"),
]
