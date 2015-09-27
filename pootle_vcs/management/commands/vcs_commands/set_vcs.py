#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

from django.core.management.base import CommandError

from pootle_vcs import plugins
from pootle_vcs.management.commands import SubCommand
from pootle_vcs.models import ProjectVCS


class SetVCSCommand(SubCommand):
    help = "Status of vcs repositories."

    def handle(self, project, *args, **options):
        if not args or not len(args) == 2:
            raise CommandError("You must a VCS type and VCS url")

        try:
            vcs_type = plugins[args[0]]
        except KeyError:
            raise CommandError("Unrecognised VCS type: %s" % args[0])

        try:            
            vcs = project.vcs.get()
        except ProjectVCS.DoesNotExist:
            vcs = project.vcs.create()

        vcs.vcs_type = args[0]
        vcs.url = args[1]
        vcs.save()
