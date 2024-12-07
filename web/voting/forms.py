from crispy_forms.helper import FormHelper
from django.forms import ModelForm

from goodies.forms import CrispyBaseForm
from voting.models import Topic


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
