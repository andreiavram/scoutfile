from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible
from storages.backends.s3boto import S3BotoStorage
from django.conf import settings

@deconstructible
class DeconstructibleS3BotoStorage(S3BotoStorage):
    pass


class MediaS3BotoStorage(DeconstructibleS3BotoStorage):
    def __init__(self, **kwargs):
        super(MediaS3BotoStorage, self).__init__(location="media", **kwargs)


class ProtectedS3BotoStorage(DeconstructibleS3BotoStorage):
    def __init__(self, **kwargs):
        super(ProtectedS3BotoStorage, self).__init__(acl='private', querystring_auth=True, querystring_expire=120,
                                                     **kwargs)


class LocalStorage(FileSystemStorage):
    def __init__(self, **kwargs):
        super(LocalStorage, self).__init__(location=settings.LOCAL_MEDIA_ROOT, base_url=settings.LOCAL_MEDIA_URL)