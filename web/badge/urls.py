# coding: utf8
from django.urls import path, include
from badge.views import BadgeList, BadgeCreate, BadgeDetail, BadgeUpdate

urlpatterns = [
    path('adauga/', BadgeCreate.as_view(), name="badge_add"),
    path('<int:pk>/', BadgeDetail.as_view(), name="badge_detail"),
    path('<int:pk>/edit/', BadgeUpdate.as_view(), name="badge_edit"),
    path('', BadgeList.as_view(), name="badge_list"),
]
