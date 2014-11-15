# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('womoobox', '0003_auto_20141113_1752'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moo',
            options={'ordering': ['-id']},
        ),
    ]
