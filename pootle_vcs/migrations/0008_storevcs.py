# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_store', '0002_make_suggestion_user_not_null'),
        ('pootle_vcs', '0007_projectvcs_pootle_config'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreVCS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_sync_revision', models.IntegerField(null=True, blank=True)),
                ('last_sync_commit', models.CharField(max_length=32)),
                ('store', models.ForeignKey(related_name='vcs', to='pootle_store.Store')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
