import os
from typing import List, Dict, Optional, Set

def filter_commits_by_filetype(
    commit_file_map: Dict[str, List[str]],
    commit_data: List[Dict],
    file_extensions: Optional[Set[str]] = None
) -> List[Dict]:
    """
    Filters commit_data to only include commits that modified files with given extensions.
    commit_file_map: dict mapping commit hash to list of file paths changed in that commit.
    commit_data: list of dicts, each with at least 'hash' key.
    file_extensions: set of extensions (e.g., {'.py', '.js'}). If None, no filtering.
    Returns filtered list of commit_data dicts.
    """
    if not file_extensions:
        return commit_data
    filtered = []
    for entry in commit_data:
        commit_hash = entry.get('hash')
        files = commit_file_map.get(commit_hash, [])
        for f in files:
            _, ext = os.path.splitext(f)
            if ext.lower() in file_extensions:
                filtered.append(entry)
                break
    return filtered

def filter_commits_by_directory(
    commit_file_map: Dict[str, List[str]],
    commit_data: List[Dict],
    directories: Optional[Set[str]] = None
) -> List[Dict]:
    """
    Filters commit_data to only include commits that modified files within given directories.
    commit_file_map: dict mapping commit hash to list of file paths changed in that commit.
    commit_data: list of dicts, each with at least 'hash' key.
    directories: set of directory paths (relative, e.g., {'src/', 'tests/'}). If None, no filtering.
    Returns filtered list of commit_data dicts.
    """
    if not directories:
        return commit_data
    norm_dirs = {os.path.normpath(d).rstrip(os.sep) + os.sep for d in directories}
    filtered = []
    for entry in commit_data:
        commit_hash = entry.get('hash')
        files = commit_file_map.get(commit_hash, [])
        for f in files:
            norm_f = os.path.normpath(f)
            for d in norm_dirs:
                if norm_f.startswith(d):
                    filtered.append(entry)
                    break
            else:
                continue
            break
    return filtered

def build_commit_file_map(
    commit_file_records: List[Dict[str, object]]
) -> Dict[str, List[str]]:
    """
    Builds a mapping from commit hash to list of changed file paths.
    commit_file_records: list of dicts with keys 'hash' and 'files' (list of str)
    Returns dict: {commit_hash: [file1, file2, ...], ...}
    """
    result = {}
    for rec in commit_file_records:
        h = rec.get('hash')
        files = rec.get('files', [])
        if h and isinstance(files, list):
            result[h] = files
    return result
