# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('womoobox', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('latitude', models.DecimalField(decimal_places=20, verbose_name='Latitude', max_digits=23)),
                ('longitude', models.DecimalField(decimal_places=20, verbose_name='Longitude', max_digits=23)),
                ('animal_type', models.CharField(verbose_name='Animal type', max_length=20)),
                ('creation_date', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('key', models.ForeignKey(verbose_name='Used API Key', to='womoobox.ApiKey')),
            ],
            options={
                'ordering': ['-creation_date', 'id'],
            },
            bases=(models.Model,),
        ),
    ]
