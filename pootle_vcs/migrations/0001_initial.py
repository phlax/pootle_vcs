# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_project', '0002_auto_20150923_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectVCS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('project', models.ForeignKey(related_name='vcs', to='pootle_project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
