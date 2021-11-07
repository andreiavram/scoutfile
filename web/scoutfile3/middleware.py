from builtins import object
from django.contrib.auth.models import User

__author__ = 'andrei'


class ImpersonateUserMiddleware:
    def __init__(self, get_reponse):
        self.get_response = get_reponse

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            if request.GET.get("impersonate__id"):
                request.session["impersonate__id"] = int(request.GET.get("impersonate__id"))

            if "impersonate__clear" in request.GET:
                if "impersonate__id" in request.session:
                    del request.session["impersonate__id"]

            try:
                if "impersonate__id" in request.session:
                    request.user = User.objects.get(id=request.session.get("impersonate__id"))
            except User.DoesNotExist:
                pass

        response = self.get_response(request)
        return response
