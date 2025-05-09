import os


def normalize_line_endings(text: str) -> str:
    """
    Normalize line endings in a string to Unix-style (\n).
    """
    return text.replace("\r\n", "\n").replace("\r", "\n")


def expand_home(path: str) -> str:
    """
    Expand the user's home directory in a given path.
    """
    if path.startswith("~"):
        return os.path.expanduser(path)
    return path


def normalize_path(path: str) -> str:
    """
    Normalize a file path by expanding the user's home directory 
    and normalizing line endings.
    """
    return os.path.normpath(path)
