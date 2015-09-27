#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

from pootle_vcs.management.commands import SubCommand


class FilesCommand(SubCommand):
    help = "List VCS translations files managed by Pootle."

    def handle(self, project, *args, **options):
        vcs = self.get_vcs(project)
        files = vcs.list_translation_files()
        for store_vcs in files.order_by("path").iterator():
            self.stdout.write(
                " %-50s %-50s %-12s %-12s \n"
                % (store_vcs.path,
                   store_vcs.store.pootle_path,
                   store_vcs.last_sync_revision,
                   store_vcs.last_sync_commit[:8]))
