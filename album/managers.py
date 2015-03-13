__author__ = 'andrei'
from django.db import models


class RaportEvenimentManager(models.Manager):
    def get_queryset(self):
        return super(RaportEvenimentManager, self).get_queryset().filter(is_leaf=True)

    def version_history(self, eveniment, **kwargs):
        kwargs['eveniment'] = eveniment
        return super(RaportEvenimentManager, self).get_queryset().filter(**kwargs)