#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

from pootle_vcs.models import ProjectVCS

from pootle_vcs.management.commands import SubCommand


class StatusCommand(SubCommand):
    help = "Status of vcs repositories."

    def handle(self, project, *args, **options):
        try:
            vcs = project.vcs.get()
        except ProjectVCS.DoesNotExist:
            vcs = None
        status = vcs.status()
        synced = (
            not status['CONFLICT']
            and not status['POOTLE_AHEAD']
            and not status['VCS_AHEAD'])
        if synced:
            self.stdout.write("Everything up-to-date")
            return
        if status["CONFLICT"]:
            self.stdout.write("Both changed:")
            for repo_file in status["CONFLICT"]:
                self.stdout.write(repo_file)
        if status["POOTLE_AHEAD"]:
            self.stdout.write("Pootle changed:")
            for repo_file in status["POOTLE_AHEAD"]:
                self.stdout.write(repo_file)
        if status["VCS_AHEAD"]:
            for store_vcs in status["VCS_AHEAD"]:
                self.stdout.write(
                    " %-32s %-32s %-25s\n"
                    % (store_vcs.path,
                       store_vcs.store.pootle_path,
                       "VCS updated: %s...%s"
                       % (store_vcs.last_sync_commit[:8],
                          store_vcs.repository_file.latest_commit[:8])))
            self.stdout.write("\n")
