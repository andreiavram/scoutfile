# coding: utf-8

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic.base import View
import urllib
import urlparse
import logging
from django.conf import settings
from utils.models import FacebookSession

logger = logging.getLogger(__name__)


class FacebookConnectView(View):
    def get_access_token(self):
        if 'error' in self.request.GET:
            raise Exception(
                "Facebook denied access error code {0}, error reason {1}, error description {2}".format(
                    self.request.GET['error'], self.request.GET['error_reason'], self.request.GET['error_description']))

        if 'code' not in self.request.GET:
            raise ValueError("No code in request.GET")

        facebook_oauth_args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': self.request.GET['code'],
            'redirect_uri': self.get_redirect_url(self.request)
        }

        facebook_oauth_url = 'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(facebook_oauth_args)
        response = urlparse.parse_qs(urllib.urlopen(facebook_oauth_url).read())

        try:
            access_token = response['access_token'][0]
            expires = response['expires'][0]
        except KeyError, e:
            logger.error(
                "{0}: problem getting access token for code {1}".format(self.__class__.__name__,
                                                                        self.request.GET['code']))
            raise e

        return access_token, expires

    def user_action(self, *args, **kwargs):
        raise ImproperlyConfigured("This method has to be overridden!")

    @classmethod
    def get_redirect_url(cls, request):
        # protocol = "http" + ("s" if self.request.is_secure() else "") + "://"
        # return protocol + self.request.get_host() + reverse("facebook_auth")
        raise ImproperlyConfigured("This method has to be overridden")

    @classmethod
    def get_facebook_endpoint(cls, request):
        return "https://www.facebook.com/dialog/oauth?client_id={0}&redirect_uri={1}&scope={2}&response_type=code".format(
            settings.FACEBOOK_APP_ID, urllib.quote(cls.get_redirect_url(request)),
            ",".join(settings.FACEBOOK_PERMISSIONS))

    def get_success_url(self):
        raise ImproperlyConfigured("This method has to be overridden")

    def get_error_url(self):
        if hasattr(settings, "FACEBOOK_ERROR_URL"):
            try:
                return reverse(settings.FACEBOOK_ERROR_URL)
            except Exception:
                pass
        raise ImproperlyConfigured("This method has to be implemented")

    def get(self, request, *args, **kwargs):
        self.request = request
        try:
            access_token, expires = self.get_access_token()
        except Exception, e:
            messages.error(self.request, u"Eroare la comunicarea cu Facebook ({0})".format(e))
            return HttpResponseRedirect(self.get_error_url())

        try:
            user = self.user_action(access_token=access_token, expires=expires)
        except Exception, e:
            messages.error(self.request, u"Autentificarea cu Facebook a eșuat ({0})".format(e))
            return HttpResponseRedirect(self.get_error_url())

        if user is None or not user.is_active:
            messages.error(self.request, u"Autentificaea cu Facebook a eșuat (userul nu este conectat)")
            return HttpResponseRedirect(self.get_error_url())

        return HttpResponseRedirect(self.get_success_url())


class FacebookLoginView(FacebookConnectView):
    def user_action(self, access_token=None, expires=None):
        profile = FacebookSession._query(access_token, 'me')
        #   create or connect user to Facebook

        facebook_session, created_fb_session = FacebookSession.objects.get_or_create(uid=profile['id'])
        facebook_session.access_token = access_token
        facebook_session.expires = expires
        facebook_session.save()

        # try:
        #     user = User.objects.get(id = facebook_session.user_id)
        # except User.DoesNotExist:
        #     return HttpResponseForbidden()

        user = auth.authenticate(token=access_token)
        auth.login(self.request, user)
        return user

    def get_success_url(self):
        return reverse("index")

    @classmethod
    def get_redirect_url(cls, request):
        protocol = "http" + ("s" if request.is_secure() else "") + "://"
        return protocol + request.get_host() + reverse("utils:facebook_login")


class FacebookUserConnectView(FacebookConnectView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FacebookUserConnectView, self).dispatch(request, *args, **kwargs)

    def user_action(self, access_token=None, expires=None):
        profile = FacebookSession._query(access_token, 'me')

        try:
            facebook_session, created_fb_session = FacebookSession.objects.get_or_create(user=self.request.user,
                                                                                         uid=profile['id'])
        except Exception, e:
            raise ValueError(u"Există alt utilizator autentificat deja cu Facebook cu acest cont.")

        facebook_session.access_token = access_token
        facebook_session.expires = expires
        facebook_session.save()

        messages.success(self.request, u"Contul de Facebook a fost conectat cu succes!")
        return self.request.user

    def get_success_url(self):
        return reverse(settings.FACEBOOK_LOGIN_REDIRECT)

    @classmethod
    def get_redirect_url(cls, request):
        protocol = "http" + ("s" if request.is_secure() else "") + "://"
        return protocol + request.get_host() + reverse("utils:facebook_connect")

    def get_error_url(self):
        return reverse("index")