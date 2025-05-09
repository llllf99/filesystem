from enum import Enum


class FileSystemTools(Enum):
    """
    Enum for FileSystemTools.
    """
    READ_FILE = "read_file"
    READ_MULTIPLE_FILES = "read_multiple_files"
    WRITE_FILE = "write_file"
    EDIT_FILE = "edit_file"
    CREATE_DIRECTORY = "create_directory"
    