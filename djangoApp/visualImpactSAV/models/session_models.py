# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Base pour créer des objets en Session tel que les adresses mail et telephones à contacter
# pour les dossiers SAV 
class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class SessionMailAndPhone(SingletonModel):
    pass
    