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
from optparse import NO_DEFAULT

# This must be run before importing Django.
os.environ['DJANGO_SETTINGS_MODULE'] = 'pootle.settings'

from django.core.management.base import BaseCommand, CommandError

from pootle_project.models import Project

from pootle_vcs.models import ProjectVCS

from .vcs_commands.info import ProjectInfoCommand
from .vcs_commands.fetch_translations import FetchTranslationsCommand
from .vcs_commands.files import FilesCommand
from .vcs_commands.pull_translations import PullTranslationsCommand
from .vcs_commands.set_vcs import SetVCSCommand
from .vcs_commands.status import StatusCommand


logger = logging.getLogger('pootle.vcs')


class Command(BaseCommand):
    help = "Pootle VCS."
    subcommands = {
        "info": ProjectInfoCommand,
        "fetch_translations": FetchTranslationsCommand,
        "files": FilesCommand,
        "pull_translations": PullTranslationsCommand,
        "set_vcs": SetVCSCommand,
        "status": StatusCommand}

    def handle_subcommand(self, project, command, *args, **options):
        try:
            subcommand = self.subcommands[command]()
        except KeyError:
            raise CommandError("Unrecognised command: %s" % command)
        defaults = {}
        for opt in subcommand.option_list:
            if opt.default is NO_DEFAULT:
                defaults[opt.dest] = None
            else:
                defaults[opt.dest] = opt.default
        defaults.update(options)
        return subcommand.execute(project, *args, **defaults)

    def handle(self, *args, **kwargs):
        if args:
            project_code = args[0]
            args = args[1:]
            try:
                project = Project.objects.get(code=project_code)
            except Project.DoesNotExist:
                project = None

            if project:
                return self.handle_subcommand(
                    project, *(args or ['info']), **kwargs)
        else:
            for project in Project.objects.all():
                try:
                    self.stdout.write(
                        "%s\t%s"
                        % (project.code, project.vcs.get().url))
                except ProjectVCS.DoesNotExist:
                    pass
