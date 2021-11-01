from builtins import object
from django.contrib.auth.models import User

from utils.models import FacebookSession


class FacebookBackend(object):
    def authenticate(self, token=None):
        try:
            return FacebookSession.objects.select_related('user').get(access_token=token).user
        except Exception as e:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
