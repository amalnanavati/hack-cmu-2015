# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodForGrabs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_what',
            new_name='what',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='event_when',
            new_name='when',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='event_where',
            new_name='where',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='event_who',
            new_name='who',
        ),
    ]
