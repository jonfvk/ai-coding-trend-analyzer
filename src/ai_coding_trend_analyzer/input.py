import os

class ProjectDirectoryInputError(Exception):
    pass

def validate_project_directory(path):
    """
    Validates that the given path is an existing directory.
    Raises ProjectDirectoryInputError if invalid.
    Returns the absolute path if valid.
    """
    if not isinstance(path, str):
        raise ProjectDirectoryInputError("Path must be a string.")
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        raise ProjectDirectoryInputError(f"Directory does not exist: {abs_path}")
    if not os.path.isdir(abs_path):
        raise ProjectDirectoryInputError(f"Path is not a directory: {abs_path}")
    return abs_path
