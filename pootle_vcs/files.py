import os

from pootle_store.models import Store
from pootle_translationproject.models import TranslationProject


class RepositoryFile(object):

    def __init__(self, vcs, path, language, filename, directory_path=None):
        self.vcs = vcs
        self.language = language
        self.filename = filename
        if directory_path is not None:
            self.directory_path = '/'.join(directory_path)
        else:
            self.directory_path = []
        self.path = path

    def __str__(self):
        return "<%s: %s>" % (self.__name__, self.pootle_path)

    @property
    def pootle_path(self):
        return "/".join(
            ['']
            + [x for x in
               [self.language.code,
                self.project.code,
                self.directory_path,
                self.filename]
               if x])

    @property
    def file_path(self):
        return os.path.join(
            self.vcs.plugin.local_repo_path,
            self.path.strip("/"))

    @property
    def project(self):
        return self.vcs.project

    @property
    def translation_project(self):
        try:
            return self.project.translationproject_set.get(
                language=self.language)
        except TranslationProject.DoesNotExist:
            return TranslationProject.objects.create(
                project=self.vcs.project,
                language=self.language)

    @property
    def directory(self):
        directory = self.translation_project.directory
        if self.directory_path:
            for subdir in self.directory_path.split("/"):
                (directory,
                 created) = directory.child_dirs.get_or_create(name=subdir)
        return directory

    @property
    def store(self):
        store, created = Store.objects.get_or_create(
            parent=self.directory,
            translation_project=self.translation_project,
            name=self.filename)
        if created:
            store.save()
        return store

    @property
    def store_vcs(self):
        from pootle_vcs.models import StoreVCS
        store_vcs, created = StoreVCS.objects.get_or_create(
            store=self.store)
        return store_vcs

    @property
    def latest_commit(self):
        raise NotImplementedError

    def pull(self):
        store_vcs = self.store_vcs
        store_vcs.path = self.path
        store_vcs.last_sync_commit = self.latest_commit
        store_vcs.last_sync_revision = self.store.get_max_unit_revision()
        store_vcs.save()

    def read(self):
        # self.vcs.pull()
        with open(self.file_path) as f:
            return f.read()
