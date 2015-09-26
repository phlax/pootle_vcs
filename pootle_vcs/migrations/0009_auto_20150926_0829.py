# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_vcs', '0008_storevcs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storevcs',
            name='last_sync_commit',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
    ]
