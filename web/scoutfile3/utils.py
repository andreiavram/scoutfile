from django.conf import settings
import os

def photologue_path(instance, filename):
    return os.path.join(settings.SCOUTFILE_ALBUM_STORAGE_ROOT, filename)
