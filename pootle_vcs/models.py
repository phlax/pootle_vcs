from django.db import models

from pootle_project.models import Project
from pootle_store.models import Store

from . import plugins


class StoreVCS(models.Model):
    store = models.ForeignKey(Store, related_name='vcs')
    last_sync_revision = models.IntegerField(blank=True, null=True)
    last_sync_commit = models.CharField(max_length=32, blank=True, null=True)
    path =  models.CharField(max_length=32)

    @property
    def vcs(self):
        return self.store.translation_project.project.vcs.get()

    @property
    def repository_file(self):
        return self.vcs.plugin.file_class(
            self.path,
            self.vcs,
            self.store.translation_project.language.code, 
            self.store.name,
            [s.name for s in self.store.parent.trail()])


class ProjectVCS(models.Model):
    project = models.ForeignKey(Project, related_name='vcs')
    url = models.URLField()
    vcs_type = models.CharField(max_length=32)
    enabled = models.BooleanField(default=True)
    fetch_frequency = models.IntegerField(default=0)
    push_frequency = models.IntegerField(default=0)
    pootle_config = models.CharField(max_length=32, default=".pootle.ini")

    @property
    def plugin(self):
        return plugins[self.vcs_type](self)

    ###########################
    # VCS Plugin implementation

    def pull(self):
        return self.plugin.pull()

    def get_latest_commit(self):
        return self.plugin.get_latest_commit()

    def read_config(self):
        return self.plugin.read_config()

    def status(self):
        return self.plugin.status()

    def pull_translation_files(self):
        return self.plugin.pull_translation_files()

    # VCS Plugin implementation
    ###########################
