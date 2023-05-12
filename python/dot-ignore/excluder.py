import logging
from os import path, listdir, rmdir
from typing import Optional

from matcher import extract_matcher


class Excluder:

    def __init__(self, ignore_content: list[str], title: str):
        self.logger = logging.getLogger(f'exclude-{title}')
        self.matchers = []

        for line in ignore_content:
            matcher = extract_matcher(line)
            if matcher is not None:
                self.matchers.append(matcher)

    def find_excluded(self, target_path: str) -> Optional[list[str]]:
        if not path.exists(target_path):
            self.logger.error(f'target path "{target_path}" does not exist')
            return None
        return self.__find_ignored_recursive__(target_path)

    def __find_ignored_recursive__(self, target_path: str) -> list[str]:
        if path.isfile(target_path):
            return [target_path] if self.is_ignored(target_path) else []

        ignored = []

        sub_path_names = listdir(target_path)
        for sub_path_name in sub_path_names:
            sub_path = path.join(target_path, sub_path_name)
            if self.is_ignored(sub_path):
                ignored.append(sub_path)
            elif path.isdir(sub_path):
                ignored.extend(self.__find_ignored_recursive__(sub_path))
        return ignored

    def is_ignored(self, target_path: str):
        for matcher in self.matchers:
            if matcher.does_match(target_path):
                return True

    def erase_ignored(self, target_path: str):
        ignored_paths = self.find_excluded(target_path)

        if ignored_paths is None or len(ignored_paths) == 0:
            self.logger.info('no ignored files found')
            return None

        for ignored_path in ignored_paths:
            if path.isdir(ignored_path):
                rmdir(ignored_path)

    @staticmethod
    def __get_excluding_content_lines_from_file__(ignore_file_path: str) -> list[str]:
        ignoreContent = []
        if not path.exists(ignore_file_path):
            return ignoreContent

        with open(ignore_file_path, 'r') as ignoreFile:
            for line in ignoreFile:
                line = line.strip()
                if line != '' and not line.startswith('#'):
                    ignoreContent.append(line)
        return ignoreContent

    @staticmethod
    def build(excluding_template_file: str, title: str = 'exclude'):
        lines = Excluder.__get_excluding_content_lines_from_file__(excluding_template_file)
        return Excluder(lines, title)
