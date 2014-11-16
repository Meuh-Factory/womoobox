from django import forms
from django.views.decorators.csrf import csrf_exempt
from womoobox.settings import *


# Form to create a new Moo
class MooForm(forms.Form):
    key = forms.CharField(label='API Key', max_length=KEY_LENGTH, min_length=KEY_LENGTH)
    latitude = forms.DecimalField(label='latitude', max_digits=23, decimal_places=20)
    longitude = forms.DecimalField(label='longitude', max_digits=23, decimal_places=20)
    animal = forms.CharField(label='Animal type', max_length=20)


# Form to get last Moo from a datetime
class GetMooForm(forms.Form):
    id = forms.IntegerField(label='Last ID of moo', required=False)


# Form to rename the username linked to an ApiKey
class KeyRename(forms.Form):
    key = forms.CharField(label='API Key', max_length=KEY_LENGTH, min_length=KEY_LENGTH)
    old_username = forms.CharField(label='Old username', max_length=30)
    new_username = forms.CharField(label='New username', max_length=30)

