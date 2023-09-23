from django.urls import re_path, path

from proiecte.views import ProjectListView, ProjectDetailView

urlpatterns = [
    path('projects/centru_local/', ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name="project_detail"),
]
