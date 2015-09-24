# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_vcs', '0002_projectvcs_project_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectvcs',
            old_name='project_type',
            new_name='vcs_type',
        ),
        migrations.AddField(
            model_name='projectvcs',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectvcs',
            name='poll_frequency',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
