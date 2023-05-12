import os.path
from typing import Optional


class Matcher:
    def __init__(self):
        self.inverted = False

    def does_match(self, matching_path: str) -> bool:
        return False

    def is_inverted(self):
        return self.inverted

    def set_inverted(self, inverted: bool):
        self.inverted = inverted


class IllegalMatcher(Matcher):
    def does_match(self, matching_path: str) -> bool:
        return False


class DirMatchingHelper:
    @staticmethod
    def extract_dirs(matching_path: str) -> list[str]:
        if not os.path.exists(matching_path) or not os.path.isdir(matching_path):
            return []
        formatted = matching_path.strip().replace('\\', '/').replace('//', '/')
        if formatted.endswith('/'):
            formatted = formatted[:-1]

        return formatted.split('/')


class SingleDirMatcher(Matcher):
    def __init__(self, dir_name: str):
        super().__init__()
        self.dir = dir_name.strip().lower()

    def does_match(self, matching_path: str) -> bool:
        dirs = DirMatchingHelper.extract_dirs(matching_path)

        if len(dirs) == 0:
            return False

        last_dir = dirs[-1]
        return last_dir.lower() == self.dir


def extract_dir_matcher(pattern) -> Optional[Matcher]:
    parts = pattern[:-1].split('/')
    if len(parts) == 0:
        return None

    if len(parts) == 1:
        return SingleDirMatcher(parts[0])


def extract_mixed_matcher(pattern) -> Optional[Matcher]:
    return None


def extract_matcher(pattern: str) -> Optional[Matcher]:
    pattern = pattern.strip()
    if pattern == '' or pattern.startswith('#'):
        return None

    inverted = False
    if pattern.startswith('!'):
        inverted = True
        pattern = pattern[1:]

    if pattern.endswith('/'):
        matcher = extract_dir_matcher(pattern)
        if matcher is None:
            return None
    else:
        matcher = extract_mixed_matcher(pattern)

    # matcher.set_inverted(inverted)
    return matcher
