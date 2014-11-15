# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=50, verbose_name='API key', unique=True)),
                ('creation_date', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('blacklisted', models.BooleanField(default=False, verbose_name='Blacklisted key?')),
                ('user_agent', models.CharField(max_length=100, verbose_name='User Agent')),
                ('user_name', models.CharField(max_length=30, null=True, verbose_name='Username', blank=True, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
