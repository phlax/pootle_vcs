#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

from pootle_vcs.management.commands import SubCommand


class ProjectInfoCommand(SubCommand):
    help = "List VCS translations files managed by Pootle."

    def handle(self, project, *args, **options):
        vcs = self.get_vcs(project)
        self.stdout.write("Project: %s" % project.code)
        self.stdout.write("type: %s" % vcs.vcs_type)
        self.stdout.write("URL: %s" % vcs.url)
        self.stdout.write("enabled: %s" % vcs.enabled)
        self.stdout.write("latest commit: %s" % vcs.get_latest_commit())
        self.stdout.write("fetch frequency: %s" % vcs.fetch_frequency)
        self.stdout.write("push frequency: %s" % vcs.push_frequency)
