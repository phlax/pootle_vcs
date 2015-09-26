from import_export.utils import import_file

from pootle_language.models import Language
from pootle_store.models import Store
from pootle_translationproject.models import TranslationProject


class RepositoryFile(object):

    def __init__(self, path, vcs, language, filename, directory_path=[]):
        self.vcs = vcs
        self.language = Language.objects.get(code=language)
        self.filename = filename
        self.directory_path = '/'.join(directory_path)
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
    def project(self):
        return self.vcs.project

    @property
    def translation_project(self):
        return self.project.translationproject_set.get(language=self.language)

    @property
    def latest_commit(self):
        raise NotImplementedError

    def pull(self):
        try:
            tp = self.translation_project
        except TranslationProject.DoesNotExist:
            tp = TranslationProject.objects.create(
                project=self.vcs.project,
                language=self.language)

        directory = tp.directory
        if self.directory_path:
            for subdir in self.directory_path.split("/"):
                (directory,
                 created) = directory.child_dirs.get_or_create(name=subdir)

        store, created = Store.objects.get_or_create(
            parent=directory, translation_project=tp, name=self.filename)
        if created:
            store.save()

        from pootle_vcs.models import StoreVCS
        store_vcs, created = StoreVCS.objects.get_or_create(
            store=store)

        with open(self.path) as f:
            import_file(
                f,
                pootle_path=self.pootle_path,
                rev=store.get_max_unit_revision())
        store_vcs.latest_sync_commit = self.latest_commit
        store_vcs.latest_sync_revision = store.get_max_unit_revision()
        store_vcs.save()

    def read(self):
        # self.vcs.pull()
        with open(self.path) as f:
            return f.read()
