from django.core.files.storage import FileSystemStorage
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaFilesStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION


class StaticFilesStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class LocalStorage(FileSystemStorage):
    def __init__(self, **kwargs):
        super(LocalStorage, self).__init__(location=settings.LOCAL_MEDIA_ROOT, base_url=settings.LOCAL_MEDIA_URL)
