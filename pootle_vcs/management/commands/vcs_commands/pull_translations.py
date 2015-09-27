#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

from pootle_vcs.management.commands import SubCommand


class PullTranslationsCommand(SubCommand):
    help = "Pull translations into Pootle from VCS."

    def handle(self, project, *args, **options):
        self.get_vcs(project).pull_translation_files()
