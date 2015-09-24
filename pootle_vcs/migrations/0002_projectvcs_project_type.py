# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_vcs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectvcs',
            name='project_type',
            field=models.CharField(default='git', max_length=32),
            preserve_default=False,
        ),
    ]
