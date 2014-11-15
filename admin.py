from django.contrib import admin
from womoobox.models import *


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('key','blacklisted', 'user_name', 'creation_date')
    readonly_fields = ['creation_date']

admin.site.register(ApiKey, ApiKeyAdmin)


class MooAdmin(admin.ModelAdmin):
    list_display = ('key','animal_type','creation_date')
    readonly_fields = ['creation_date']

    fieldsets = [
        ('Creation', {'fields': ['key', 'creation_date']}),
        ('Infos', {'fields': ['latitude', 'longitude', 'animal_type']})
    ]
admin.site.register(Moo, MooAdmin)
