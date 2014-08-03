# Create your views here.

#
# urlpatterns = patterns('cantece.views',
#     url(r'cantec/list/$', CantecList.as_view(), name="cantec_list"),
#     url(r'cantec/create/$', CantecCreate.as_view(), name="cantec_add"),
#     url(r'cantec/(?P<pk>\d+)/$', CantecDetail.as_view(), name="cantec_detail"),
#     url(r'cantec/(?P<pk>\d+)/edit/$', CantecEdit.as_view(), name="cantec_edit"),
#
#     url(r'carte/list/$', CarteList.as_view(), name="carte_list"),
#     url(r'carte/create/$', CarteCreate.as_view(), name="carte_add"),
#     url(r'carte/(?P<pk>\d+)/$', CarteDetail.as_view(), name="carte_detail"),
#     url(r'carte/(?P<pk>\d+)/edit/$', CarteEdit.as_view(), name="carte_edit"),
# )
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from cantece.forms import CantecForm, CarteCanteceForm
from cantece.models import Cantec, CarteCantece


class CantecList(ListView):
    model = Cantec
    template_name = "cantece/cantec_list.html"


class CantecCreate(CreateView):
    model = Cantec
    template_name = "cantece/cantec_form.html"
    form_class = CantecForm


class CantecEdit(UpdateView):
    model = Cantec
    template_name = "cantece/cantec_form.html"
    form_class = CantecForm


class CantecDetail(DetailView):
    model = Cantec
    template_name = "cantece/cantec_detail.html"


class CarteList(ListView):
    model = CarteCantece
    template_name = "cantece/cartecantece_list.html"


class CarteCreate(CreateView):
    model = CarteCantece
    template_name = "cantece/cartecantece_form.html"
    form_class = CarteCanteceForm


class CarteEdit(UpdateView):
    model = CarteCantece
    template_name = "cantece/cartecantece_form.html"
    form_class = CarteCanteceForm

class CarteDetail(DetailView):
    model = CarteCantece
    templatE_name = "cantece/cartecantece_detail.html"


