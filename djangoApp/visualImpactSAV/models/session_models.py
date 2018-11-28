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

    @classmethod
    def load_all_mail_and_phones(cls):
        obj = SessionMailAndPhone.load()
        return obj.mailAndPhones.all()

    @classmethod
    def load_and_delete_all_mail_and_phones(cls):
        obj = SessionMailAndPhone.load()
        obj.mailAndPhones.all().delete()
        return obj

    @classmethod
    def load_and_unlink_all_mail_and_phones(cls):
        obj = SessionMailAndPhone.load()
        obj.mailAndPhones.all().update(in_session=None)
