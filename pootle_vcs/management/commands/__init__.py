#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

from django.core.management.base import BaseCommand, CommandError

from pootle_vcs.models import ProjectVCS


class SubCommand(BaseCommand):

    requires_system_checks = False

    def get_vcs(self, project):
        try:
            return project.vcs.get()
        except ProjectVCS.DoesNotExist:
            raise CommandError(
                "Project (%s) is not managed in VCS"
                % project.code)
