# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import womoobox.models


class Migration(migrations.Migration):

    dependencies = [
        ('womoobox', '0002_moo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(verbose_name='API key', default=womoobox.models._createKey, max_length=50, unique=True),
        ),
    ]
