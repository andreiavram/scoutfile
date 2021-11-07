from future import standard_library
standard_library.install_aliases()
from django.db import models
from django.contrib.auth.models import User

class FacebookSessionError(Exception):
    def __init__(self, error_type, message):
        self.message = message
        self.type = error_type
  
    def get_message(self):
        return self.message

    def get_type(self):
        return self.type

    def __str__(self):
        return u'%s: "%s"' % (self.type, self.message)

class FacebookSession(models.Model):
    access_token = models.CharField(max_length=1024)
    expires = models.IntegerField(null=True)

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    uid = models.BigIntegerField(unique=True, null=True)

    #class Meta:
    #    unique_together = (('user', 'uid'), ('access_token', 'expires'))
    
    @classmethod
    def _query(cls, access_token, object_id, connection_type=None, metadata=False):
        import urllib.request, urllib.parse, urllib.error
        import json

        url = 'https://graph.facebook.com/%s' % object_id
        if connection_type:
            url += '/%s' % connection_type

        params = {'access_token': access_token}
        if metadata:
            params['metadata'] = 1

        url += '?' + urllib.parse.urlencode(params)
        response = json.load(urllib.request.urlopen(url))
        if 'error' in response:
            error = response['error']
            raise FacebookSessionError(error['type'], error['message'])
        return response

    def query(self, access_token, object_id, connection_type=None, metadata=False):
        return self.__class__._query(access_token, object_id)
        
    def __str__(self):
        return u'%s' % self.uid
