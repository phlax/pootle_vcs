import io
import logging
import os
import re
from ConfigParser import ConfigParser

from pootle_language.models import Language

from .files import RepositoryFile

logger = logging.getLogger(__name__)


class Plugin(object):
    name = None
    file_class = RepositoryFile

    def __init__(self, vcs):
        self.vcs = vcs

    @property
    def local_repo_path(self):
        vcs_path = "/tmp"
        return os.path.join(vcs_path, self.vcs.project.code)

    @property
    def is_cloned(self):
        if os.path.exists(self.local_repo_path):
            return True
        return False

    def find_translation_files(self):
        config = self.read_config()

        for section in config.sections():
            translation_path = os.path.join(self.local_repo_path,
                                            config.get(section,
                                                       "translation_path"))
            file_root = translation_path.split("<")[0]
            if not file_root.endswith("/"):
                file_root = "/".join(file_root.split("/")[:-1])

            match = (translation_path.replace(".", "\.")
                                     .replace("<lang>",
                                              "(?P<lang>[\w]*)")
                                     .replace("<filename>",
                                              "(?P<filename>[\w]*)")
                                     .replace("<directory_path>",
                                              "(?P<directory_path>[\w\/]*)"))

            match = re.compile(match)
            if section == "default":
                section_subdirs = []
            else:
                section_subdirs = section.split("/")
            # TODO: make sure translation_path has no ..
            for root, dirs, files in os.walk(file_root):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    matches = match.match(file_path)
                    subdirs = section_subdirs + [
                        m for m in
                        matches.groupdict().get('directory_path',
                                                '').strip("/").split("/")
                        if m]
                    if matches:
                        # TODO: extension matching?
                        lang_code = matches.groupdict()['lang']
                        try:
                            yield self.file_class(file_path,
                                                  self.vcs,
                                                  lang_code,
                                                  filename,
                                                  subdirs)
                        except Language.DoesNotExist:
                            logger.warning("Language does not exist for %s: %s"
                                           % (self.vcs,
                                              lang_code))

    def pull_translation_files(self):
        for repo_file in self.find_translation_files():
            repo_file.sync()

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


class Plugins(object):

    def __init__(self):
        self.__plugins__ = {}

    def register(self, plugin):
        self.__plugins__[plugin.name] = plugin

    def __getitem__(self, k):
        return self.__plugins__[k]
