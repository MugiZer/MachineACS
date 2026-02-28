from pathlib import Path
from typing import Dict, Tuple, List, Optional

_PATHS_CACHE: Optional[Dict[str, Tuple[List[str], List[Path]]]] = None

SUPPORTED_EXTENSIONS = {
    ".json": "json",
    ".jsonl": "jsonl",
    ".csv": "csv",
    ".txt": "txt",
}


def get_paths(base_file: str = __file__) -> Dict[str, Tuple[List[str], List[Path]]]:
    """
    Discover data files in the data directory.

    Args:
        base_file: Base file path for relative path resolution.

    Returns:
        Dict mapping file type to (filenames, paths) tuples.
    """
    global _PATHS_CACHE
    if _PATHS_CACHE is not None:
        return _PATHS_CACHE

    base = Path(base_file).resolve().parent.parent
    data_dir = base / "data"

    results: Dict[str, Tuple[List[str], List[Path]]] = {
        "json": ([], []),
        "jsonl": ([], []),
        "csv": ([], []),
        "txt": ([], []),
    }

    if not data_dir.exists():
        _PATHS_CACHE = results
        return _PATHS_CACHE

    for file_path in data_dir.iterdir():
        if not file_path.is_file():
            continue

        ext = file_path.suffix.lower()
        kind = SUPPORTED_EXTENSIONS.get(ext)
        if kind:
            results[kind][0].append(file_path.name)
            results[kind][1].append(file_path)

    _PATHS_CACHE = results
    return _PATHS_CACHE


def clear_cache() -> None:
    """Clear the paths cache, useful for testing."""
    global _PATHS_CACHE
    _PATHS_CACHE = None
