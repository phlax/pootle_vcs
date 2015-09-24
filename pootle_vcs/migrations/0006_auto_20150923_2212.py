# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_vcs', '0005_projectvcs_push_frequency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectvcs',
            old_name='pull_frequency',
            new_name='fetch_frequency',
        ),
    ]
