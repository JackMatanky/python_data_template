# -----------------------------------------------------------------------------
# File: docs/scripts/render_erds.py
# Description: Generate ERDs of all Pydantic models in the codebase using erdantic.
# -----------------------------------------------------------------------------

"""
render_erds.py
~~~~~~~~~~~~~~

Recursively scans a Python project for Pydantic models and generates
entity-relationship diagrams using `erdantic`.

Supports:
- Global ERD for all models
- Package-specific ERDs (optional)
- Skips auxiliary directories like __pycache__, .egg-info, and old/

The output is saved as PNGs in `docs/assets/`.

Usage:
    python docs/scripts/render_erds.py
"""

import importlib
import inspect
from pathlib import Path
import sys
from types import ModuleType
from typing import Any, Final

import erdantic as erd
from pydantic import BaseModel, create_model

from shared.paths import DOCS_DIR, SRC_DIR

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
EXCLUDED_DIRS: Final[set[str]] = {"__pycache__", "_old", "old"}
EXCLUDED_SUFFIXES: Final[set[str]] = {".egg-info"}

ASSETS_DIR: Final[Path] = DOCS_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# Directory Filtering
# -----------------------------------------------------------------------------
def is_excluded(path: Path) -> bool:
    """
    Return True if the given path is inside an excluded directory
    or has a disallowed suffix.
    """
    return any(
        part in EXCLUDED_DIRS
        or any(part.endswith(suffix) for suffix in EXCLUDED_SUFFIXES)
        for part in path.parts
    )


# -----------------------------------------------------------------------------
# Model Discovery
# -----------------------------------------------------------------------------
def find_pydantic_models(package_root: Path) -> list[type[BaseModel]]:
    """
    Traverse a package directory and collect all subclasses of `BaseModel`.

    Args:
        package_root: The path to the Python package under `src/`.

    Returns:
        A list of all discovered Pydantic model classes.
    """
    models: list[type[BaseModel]] = []

    for file_path in package_root.rglob("*.py"):
        if file_path.name.startswith("_") or is_excluded(file_path):
            continue

        module_path: str = ".".join(
            file_path.relative_to(SRC_DIR).with_suffix("").parts
        )

        try:
            module: ModuleType = importlib.import_module(module_path)
        except Exception as e:
            print(f"[!] Skipping module {module_path} due to import error: {e}")
            continue

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseModel) and obj is not BaseModel:
                models.append(obj)

    return models


# -----------------------------------------------------------------------------
# Diagram Rendering
# -----------------------------------------------------------------------------
def render_erd(models: list[type[BaseModel]], output_path: Path) -> None:
    """
    Render and save the ERD diagram for the given models.

    Args:
        models: List of model classes to include in the diagram.
        output_path: Location to save the rendered image.
    """
    if not models:
        print(f"⚠️  No models to render for {output_path.name}")
        return

    # Dynamically create a synthetic model to link all discovered models together
    field_defs: dict[str, tuple[Any, Any]] = {
        f"model_{i}": (model, ...) for i, model in enumerate(models)
    }

    SyntheticModel = create_model("SyntheticModel", **field_defs)  # pyright: ignore

    diagram: erd.EntityRelationshipDiagram = erd.create(SyntheticModel)
    diagram.draw(output_path)
    print(f"✅ Saved: {output_path}")


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
def main() -> None:
    print("📊 Rendering ERDs from Pydantic models...")
    sys.path.insert(0, str(SRC_DIR))

    all_models: list[type[BaseModel]] = []

    for subpackage_dir in SRC_DIR.iterdir():
        if not subpackage_dir.is_dir() or is_excluded(subpackage_dir):
            continue

        models = find_pydantic_models(subpackage_dir)
        print(f"🔍 Found {len(models)} models in: {subpackage_dir.name}")

        if models:
            output_file: Path = ASSETS_DIR / f"{subpackage_dir.name}_erd.png"
            render_erd(models, output_file)
            all_models.extend(models)

    if all_models:
        global_erd_path: Path = ASSETS_DIR / "full_codebase_erd.png"
        render_erd(all_models, global_erd_path)


# -----------------------------------------------------------------------------
# Script Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
