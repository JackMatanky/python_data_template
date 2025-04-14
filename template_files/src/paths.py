"""
paths.py
~~~~~~~~

Centralised, *typed* path definitions for the project.

Why keep paths in one module?
-----------------------------
* **Single source of truth** – change the folder structure once, not in every
  notebook / script.
* **Cross‑platform** – `pathlib.Path` joins segments with the correct
  separator for Windows, macOS, Linux.
* **Static‑analysis friendly** – with `Final` type hints, mypy/pyright will
  warn if you accidentally re‑assign a constant.

Typical usage
-------------
>>> from paths import RAW_DIR, CLEANED_PATH
>>> df = pd.read_csv(RAW_DIR / "polling_stations.csv")   # Path object
>>> legacy_tool(CLEANED_PATH)                            # plain str
"""

from pathlib import Path
from typing import Final, Tuple

# ─────────────────────────────────────────────────────────────
# 1.  Resolve the project’s *base* directory
# ─────────────────────────────────────────────────────────────
# __file__   : …/my_project/src/paths.py
# parents[1] : …/my_project/          (one level above src/)
BASE_DIR: Final[Path] = Path(__file__).resolve().parents[1]

# Folder that holds all data sets (raw → cleaned → processed → results )
DATA_DIR: Final[Path] = BASE_DIR / "data"

# ─────────────────────────────────────────────────────────────
# 2.  Stage‑specific sub‑directories
# ─────────────────────────────────────────────────────────────
RAW_DIR: Final[Path] = DATA_DIR / "01_raw"  # untouched source files
CLEANED_DIR: Final[Path] = DATA_DIR / "02_cleaned"  # after initial wrangling
PROCESSED_DIR: Final[Path] = (
    DATA_DIR / "03_processed"
)  # ready for modelling / viz
RESULTS_DIR: Final[Path] = DATA_DIR / "04_results"

# ─────────────────────────────────────────────────────────────
# 3.  String aliases (some older libraries still need str)
# ─────────────────────────────────────────────────────────────
RAW_PATH: Final[str] = str(RAW_DIR)
CLEANED_PATH: Final[str] = str(CLEANED_DIR)
PROCESSED_PATH: Final[str] = str(PROCESSED_DIR)
RESULTS_PATH: Final[str] = str(RESULTS_DIR)

# ─────────────────────────────────────────────────────────────
# 4.  Re‑export for “from paths import *”
# ─────────────────────────────────────────────────────────────
__all__: Tuple[str, ...] = (
    "BASE_DIR",
    "DATA_DIR",
    "RAW_DIR",
    "CLEANED_DIR",
    "PROCESSED_DIR",
    "RESULTS_DIR",
    "RAW_PATH",
    "CLEANED_PATH",
    "PROCESSED_PATH",
    "RESULTS_PATH",
)
