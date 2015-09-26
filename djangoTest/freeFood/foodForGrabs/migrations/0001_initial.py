# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_when', models.DateTimeField(verbose_name=b'time of the event')),
                ('event_where', models.CharField(max_length=200, verbose_name=b'location of the event')),
                ('event_who', models.CharField(max_length=200, verbose_name=b'group that is hosting the event')),
                ('event_what', models.TextField(verbose_name=b'description of the event')),
            ],
        ),
    ]
