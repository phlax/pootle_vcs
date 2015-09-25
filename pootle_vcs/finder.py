import os
import re


class TranslationFileFinder(object):

    def __init__(self, translation_path):
        self.translation_path = translation_path

    @property
    def regex(self):
        return re.compile(
            self.translation_path.replace(".", "\.")
                                 .replace("<lang>",
                                          "(?P<lang>[\w]*)")
                                 .replace("<filename>",
                                          "(?P<filename>[\w]*)")
                                 .replace("<directory_path>",
                                          "(?P<directory_path>[\w\/]*)"))

    @property
    def file_root(self):
        file_root = self.translation_path.split("<")[0]
        if not file_root.endswith("/"):
            file_root = "/".join(file_root.split("/")[:-1])
        return file_root

    def find(self):
        # TODO: make sure translation_path has no ..
        for root, dirs, files in os.walk(self.file_root):
            for filename in files:
                matches = self.regex.match(file_path)
                if matches:
                    yield os.path.join(root, filename), matches.groupdict()

