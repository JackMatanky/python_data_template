# -----------------------------------------------------------------------------
# File: src/shared/paths.py
# Description: Centralized, typed project paths based on root detection
# -----------------------------------------------------------------------------

"""
paths.py
~~~~~~~~

Typed, centralized paths for project-wide file organization.

This module defines the core directory structure for your project — from
data intake to cleaned outputs, final results, and source code.

The project root is dynamically located by searching for a marker file
such as `pyproject.toml` or a `.git` directory.

Usage:
    >>> from utils.paths import RAW_DIR, RESULTS_DIR
    >>> df = pd.read_csv(RAW_DIR / "input.csv")
    >>> results_path = RESULTS_DIR / "summary_table.xlsx"
"""

from collections.abc import Sequence
from pathlib import Path
from typing import Final

# -----------------------------------------------
# Dynamic Project Root Resolution
# -----------------------------------------------
# Default markers used to identify the project root
DEFAULT_MARKERS: Final[tuple[str, ...]] = ("pyproject.toml", ".git")


def find_project_root(markers: Sequence[str] | None = None) -> Path:
    """
    Recursively walk up parent directories to locate the project root.

    The project root is identified by the presence of one of the default
    marker files, such as "pyproject.toml" or ".git".

    Args:
        markers: Marker filenames to look for. Defaults to DEFAULT_MARKERS.

    Returns:
        Path object pointing to the detected project root directory.

    Raises:
        RuntimeError: If no marker is found in the current path or its parents.
    """
    resolved_markers: Sequence[str] = (
        markers if markers is not None else DEFAULT_MARKERS
    )
    current_path: Path = Path(__file__).resolve()
    search_paths: list[Path] = [current_path, *current_path.parents]

    for ancestor_dir in search_paths:
        if any((ancestor_dir / marker).exists() for marker in resolved_markers):
            return ancestor_dir

    raise RuntimeError(
        "Could not find project root (missing one of: ",
        ", ".join(resolved_markers),
    )


# -----------------------------------------------
# Project Root & Core Directories
# -----------------------------------------------
BASE_DIR: Final[Path] = find_project_root()
SRC_DIR: Final[Path] = BASE_DIR / "src"
DATA_DIR: Final[Path] = BASE_DIR / "data"
RESULTS_DIR: Final[Path] = BASE_DIR / "results"
REFERENCE_DIR: Final[Path] = BASE_DIR / "references"
DOCS_DIR: Final[Path] = BASE_DIR / "docs"
TESTS_DIR: Final[Path] = BASE_DIR / "tests"

# -----------------------------------------------
# Data Directory Structure
# -----------------------------------------------

# Raw → Cleaned → Processed pipeline
EXTERNAL_DIR: Final[Path] = DATA_DIR / "00_external"
RAW_DIR: Final[Path] = DATA_DIR / "01_raw"
CLEANED_DIR: Final[Path] = DATA_DIR / "02_cleaned"
PROCESSED_DIR: Final[Path] = DATA_DIR / "03_processed"

# Column dictionaries and persistent cache files
DICTIONARY_DIR: Final[Path] = DATA_DIR / "dictionaries"
CACHE_DIR: Final[Path] = DATA_DIR / "cache"
CACHE_DICT_DIR: Final[Path] = CACHE_DIR / "dictionaries"

# -----------------------------------------------
# String fallbacks
# -----------------------------------------------

RAW_PATH: Final[str] = str(RAW_DIR)
CLEANED_PATH: Final[str] = str(CLEANED_DIR)
PROCESSED_PATH: Final[str] = str(PROCESSED_DIR)
RESULTS_PATH: Final[str] = str(RESULTS_DIR)
DICTIONARY_PATH: Final[str] = str(DICTIONARY_DIR)
SRC_PATH: Final[str] = str(SRC_DIR)

# -----------------------------------------------
# Public API
# -----------------------------------------------

__all__: Final[tuple[str, ...]] = (
    # Core Directories
    "BASE_DIR",
    "SRC_DIR",
    "DATA_DIR",
    "RESULTS_DIR",
    "REFERENCE_DIR",
    "DOCS_DIR",
    "TESTS_DIR",
    # Primary Data Directories
    "RAW_DIR",
    "RAW_GEOENTITY_DIR",
    "CLEANED_DIR",
    "PROCESSED_DIR",
    # Cache and Dictionary Directories
    "DICTIONARY_DIR",
    "CACHE_DIR",
    "CACHE_DICT_DIR",
    "CACHE_GEOENTITY_DIR",
    # String Fallbacks
    "RAW_PATH",
    "CLEANED_PATH",
    "PROCESSED_PATH",
    "RESULTS_PATH",
    "DICTIONARY_PATH",
    "SRC_PATH",
)
