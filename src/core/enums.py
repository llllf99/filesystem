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
    LIST_DIRECTORY = "list_directory"
    LIST_DIRECTORY_WITH_SIZE = "list_directory_with_size"
    DIRECTORY_TREE = "directory_tree"
