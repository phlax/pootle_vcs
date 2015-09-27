import io
import logging
import os
from ConfigParser import ConfigParser

from pootle_language.models import Language
from pootle_store.models import Store

from .files import RepositoryFile
from .finder import TranslationFileFinder


logger = logging.getLogger(__name__)


class Plugin(object):
    name = None
    file_class = RepositoryFile

    def __init__(self, vcs):
        self.vcs = vcs

    @property
    def is_cloned(self):
        if os.path.exists(self.local_repo_path):
            return True
        return False

    @property
    def local_repo_path(self):
        vcs_path = "/tmp"
        return os.path.join(vcs_path, self.vcs.project.code)

    @property
    def project(self):
        return self.vcs.project

    @property
    def stores(self):
        return Store.objects.filter(
            translation_project__project=self.project)

    @property
    def translation_files(self):
        from .models import StoreVCS
        return StoreVCS.objects.filter(
            store__translation_project__project=self.project)

    def fetch_translation_files(self):
        for repo_file in self.find_translation_files():
            repo_file.fetch()

    def find_translation_files(self):
        config = self.read_config()

        for section in config.sections():
            if section == "default":
                section_subdirs = []
            else:
                section_subdirs = section.split("/")

            finder = TranslationFileFinder(
                os.path.join(
                    self.local_repo_path,
                    config.get(section, "translation_path")))
            for file_path, matched in finder.find():
                lang_code = matched['lang']
                try:
                    language = Language.objects.get(code=lang_code)
                except Language.DoesNotExist:
                    logger.warning(
                        "Language does not exist for %s: %s"
                        % (self.vcs, lang_code))
                subdirs = (
                    section_subdirs
                    + [m for m in
                       matched.get('directory_path', '').strip("/").split("/")
                       if m])
                filename = (
                    matched.get("filename") or os.path.basename(file_path))
                yield self.file_class(
                    self.vcs,
                    file_path.replace(self.local_repo_path, ""),
                    language,
                    filename,
                    subdirs)

    def pull_translation_files(self):
        for repo_file in self.find_translation_files():
            repo_file.pull()

    def pull(self):
        raise NotImplementedError

    def push(self):
        raise NotImplementedError

    def read(self, path):
        target = os.path.join(self.local_repo_path, path)
        with open(target) as f:
            content = f.read()
        return content

    def read_config(self):
        self.pull()
        config = ConfigParser()
        config.readfp(io.BytesIO(self.read(self.vcs.pootle_config)))
        return config

    def status(self):
        self.pull()
        status = dict(
            CONFLICT=[],
            VCS_ADDED=[],
            VCS_AHEAD=[],
            POOTLE_AHEAD=[])

        for store_vcs in self.translation_files:
            repo_file = store_vcs.repository_file            
            repo_removed = not repo_file.exists
            repo_added = (
                store_vcs.last_sync_commit is None)
            repo_changed = (
                store_vcs.last_sync_commit is not None
                and (repo_file.latest_commit
                     != store_vcs.last_sync_commit))
            pootle_changed = (
                store_vcs.last_sync_commit is not None
                and (store_vcs.store.get_max_unit_revision()
                     != store_vcs.last_sync_revision))
            if repo_removed:
                status['VCS_REMOVED'].append(store_vcs)
            elif repo_added:
                status['VCS_ADDED'].append(store_vcs)
            elif repo_changed and pootle_changed:
                status['CONFLICT'].append(store_vcs)
            elif repo_changed:
                status['VCS_AHEAD'].append(store_vcs)
            elif pootle_changed:
                status['POOTLE_AHEAD'].append(store_vcs)

        status['POOTLE_ADDED'] = self.stores.filter(vcs__isnull=True)

        return status


class Plugins(object):

    def __init__(self):
        self.__plugins__ = {}

    def register(self, plugin):
        self.__plugins__[plugin.name] = plugin

    def __getitem__(self, k):
        return self.__plugins__[k]

    def __contains__(self, k):
        return k in self.__plugins__

