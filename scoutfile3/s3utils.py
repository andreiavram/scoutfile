from django.core.files.storage import FileSystemStorage

__author__ = 'andrei'


from storages.backends.s3boto import S3BotoStorage
from django.conf import settings

MediaS3BotoStorage = lambda: S3BotoStorage(location='media')

ProtectedS3BotoStorage = lambda: S3BotoStorage(
  acl='private',
  querystring_auth=True,
  querystring_expire=120, # 10 minutes, try to ensure people won't/can't share
)

LocalStorage = lambda: FileSystemStorage(
    location = settings.LOCAL_MEDIA_ROOT,
    base_url = settings.LOCAL_MEDIA_URL,
)