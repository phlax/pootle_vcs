# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_vcs', '0003_auto_20150923_2155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectvcs',
            old_name='poll_frequency',
            new_name='pull_frequency',
        ),
    ]
