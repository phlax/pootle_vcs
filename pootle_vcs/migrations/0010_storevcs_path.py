# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_vcs', '0009_auto_20150926_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='storevcs',
            name='path',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
    ]
