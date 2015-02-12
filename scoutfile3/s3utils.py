from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible
from storages.backends.s3boto import S3BotoStorage
from django.conf import settings

@deconstructible
class DeconstructableS3BotoStorage(S3BotoStorage):
    pass

MediaS3BotoStorage = DeconstructableS3BotoStorage(location='media')

ProtectedS3BotoStorage = DeconstructableS3BotoStorage(
    acl='private',
    querystring_auth=True,
    querystring_expire=120,     # 10 minutes, try to ensure people won't/can't share
)

LocalStorage = FileSystemStorage(
    location=settings.LOCAL_MEDIA_ROOT,
    base_url=settings.LOCAL_MEDIA_URL,
)