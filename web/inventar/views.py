# Create your views here.
import json

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View

# deprecated on upgrade to python3
# from fabric.tasks import execute
# from inventar.fabfile import open_gate


class LocatieAccess(TemplateView):
    template_name = "inventar/access_locatie.html"

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(LocatieAccess, self).dispatch(request, *args, **kwargs)


class LocatieAccessAction(View):
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(LocatieAccessAction, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            # res = execute(open_gate, host=settings.GATEKEEPER_CONNECTION_STRING)
            res = "DISABLED"
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({"result": "%s" % e}))
        return HttpResponse(json.dumps({"result": res}))

