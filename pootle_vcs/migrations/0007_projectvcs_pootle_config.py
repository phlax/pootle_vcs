# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_vcs', '0006_auto_20150923_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectvcs',
            name='pootle_config',
            field=models.CharField(default=b'.pootle.ini', max_length=32),
            preserve_default=True,
        ),
    ]
