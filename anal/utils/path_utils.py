import os
from pathlib import Path


def get_project_root() -> Path:
    """Get project root directory (parent of anal/).

    Returns:
        Path: Project root directory
    """
    # utils dir -> anal dir -> project root
    script_dir = Path(__file__).parent.parent
    return script_dir.parent


def get_raw_data_path(subpath: str = "") -> Path:
    """Get path to raw-data directory.

    Args:
        subpath: Optional subdirectory or file within raw-data

    Returns:
        Path: Full path to raw-data directory or file
    """
    root = get_project_root()
    if subpath:
        return root / "raw-data" / subpath
    return root / "raw-data"


def get_data_path(filename: str = "") -> Path:
    """Get path to data directory.

    Args:
        filename: Optional filename within data directory

    Returns:
        Path: Full path to data directory or file
    """
    root = get_project_root()
    if filename:
        return root / "data" / filename
    return root / "data"


def get_output_path(filename: str = "") -> Path:
    """Get path to output directory (anal directory).

    Args:
        filename: Optional filename within anal directory

    Returns:
        Path: Full path to anal directory or file
    """
    script_dir = Path(__file__).parent.parent  # anal dir
    if filename:
        return script_dir / filename
    return script_dir
