from django.db import models
from womoobox.settings import *
import random
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

# Generate a random hash with HASH_LENGTH characters from HASH_REF_SETS
def _createKey():
    while True:
        # build a random hash
        key_hash = ''.join([random.choice(KEY_REF_SETS) for n in range(KEY_LENGTH)])
        # test if hash is already in Short table
        if not ApiKey.objects.filter(key=key_hash):
            return key_hash # if not, return


# Default user_name
def _defaultUsername(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.user_name:
        instance.user_name = "User_" + str(instance.id)
        instance.save()


# API key are used to identify the Moo creators
class ApiKey(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(_('API key'), max_length=KEY_LENGTH, default=_createKey, unique=True)
    creation_date = models.DateTimeField(_('Creation date'), auto_now_add=True)
    blacklisted = models.BooleanField(_('Blacklisted key?'), default=False)
    user_agent = models.CharField(_('User Agent'), max_length=100)
    user_name = models.CharField(_('Username'), max_length=30, unique=True, blank=True, null=True)

    def __str__(self):
        return self.key


# Add a default user_name
post_save.connect(_defaultUsername, sender=ApiKey)


# Moo in the world
class Moo(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.ForeignKey(ApiKey, verbose_name=_("Used API Key"))
    latitude = models.DecimalField(_('Latitude'), max_digits=23, decimal_places=20)
    longitude = models.DecimalField(_('Longitude'), max_digits=23, decimal_places=20)
    animal_type = models.CharField(_('Animal type'), max_length=20)
    creation_date = models.DateTimeField(_('Creation date'), auto_now_add=True)

    class Meta:
        ordering = ['-id']
