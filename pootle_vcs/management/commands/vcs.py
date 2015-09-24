#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

import logging
import os

# This must be run before importing Django.
os.environ['DJANGO_SETTINGS_MODULE'] = 'pootle.settings'

from django.core.management.base import BaseCommand

from pootle_project.models import Project

from pootle_vcs.models import ProjectVCS


logger = logging.getLogger('pootle.vcs')


class Command(BaseCommand):
    help = "Pootle VCS."

    def handle_project(self, project):
        try:
            vcs = project.vcs.get()
        except ProjectVCS.DoesNotExist:
            vcs = None
        if vcs:
            self.stdout.write("%s\t%s" % (project.code, project.vcs.get().url))

    def handle_project_info(self, project):
        try:
            vcs = project.vcs.get()
        except ProjectVCS.DoesNotExist:
            vcs = None
        if vcs:
            self.stdout.write("Project: %s" % project.code)
            self.stdout.write("type: %s" % vcs.vcs_type)
            self.stdout.write("URL: %s" % vcs.url)
            self.stdout.write("enabled: %s" % vcs.enabled)
            self.stdout.write("latest commit: %s" % vcs.get_latest_commit())
            self.stdout.write("fetch frequency: %s" % vcs.fetch_frequency)
            self.stdout.write("push frequency: %s" % vcs.push_frequency)

    def handle_pull_translations(self, project):
        try:
            vcs = project.vcs.get()
        except ProjectVCS.DoesNotExist:
            vcs = None
        vcs.pull_translation_files()

    def handle_commit_changes(self, project):
        pass

    def handle_read_config(self, project):
        try:
            vcs = project.vcs.get()
        except ProjectVCS.DoesNotExist:
            vcs = None
        config = vcs.read_config()
        

    def handle(self, *args, **kwargs):

        if args:
            project_code = args[0]
            args = args[1:]
            try:
                project = Project.objects.get(code=project_code)
            except Project.DoesNotExist:
                project = None

            if project:
                if args:
                    command = args[0]
                    handler = getattr(self, "handle_%s" % command, None)
                    if handler:
                        handler(project)
                else:
                    self.handle_project_info(project)

        else:
            for project in Project.objects.all():
                self.handle_project(project)
