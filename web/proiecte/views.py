# Create your views here.
from django.views.generic import ListView, DetailView

from proiecte.models import Project


class ProjectListView(ListView):
    queryset = Project.objects.all()
    template_name = 'proiecte/project_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'proiecte/project_detail.html'
