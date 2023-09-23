from django.urls import path

from locuri.views import GPXTrackList, GPXTrackCreate, GPXTrackEdit, GPXTrackDetail, LocuriDashboard

urlpatterns = [
    path('dashboard/', LocuriDashboard.as_view(), name="dashboard"),
    path('tracks/', GPXTrackList.as_view(), name="gpx_track_list"),
    path('tracks/create/', GPXTrackCreate.as_view(), name="gpx_track_create"),
    path('tracks/<int:pk>/', GPXTrackDetail.as_view(), name="gpx_track_detail"),
    path('tracks/<int:pk>/edit/', GPXTrackEdit.as_view(), name="gpx_track_edit"),
]
