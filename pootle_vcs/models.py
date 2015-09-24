from django.db import models

from pootle_project.models import Project

from pootle_vcs import plugins


class ProjectVCS(models.Model):
    project = models.ForeignKey(Project, related_name='vcs')
    url = models.URLField()
    vcs_type = models.CharField(max_length=32)
    enabled = models.BooleanField(default=True)
    fetch_frequency = models.IntegerField(default=0)
    push_frequency = models.IntegerField(default=0)

    @property
    def plugin(self):
        return plugins[self.vcs_type](self)

    ###########################
    # VCS Plugin implementation

    def pull(self):
        return self.plugin.pull()

    def get_latest_commit(self):
        return self.plugin.get_latest_commit()

    # VCS Plugin implementation
    ###########################
