from django.views.generic import ListView, DetailView, CreateView

from voting.forms import TopicForm
from voting.models import Topic


class TopicListView(ListView):
    model = Topic
    template_name = 'voting/topic_list.html'


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'voting/topic_detail.html'


class TopicCreateView(CreateView):
    model = Topic
    form_class = TopicForm
    template_name = "voting/topic_form.html"

