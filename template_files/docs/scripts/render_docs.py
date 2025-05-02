# -----------------------------------------------------------------------------
# File: docs/scripts/render_docs.py
# Description: Generate Markdown documentation for all source modules using pdoc.
# -----------------------------------------------------------------------------

"""
render_docs.py
~~~~~~~~~~~~~~

Generates Markdown documentation for all packages in the source directory
using `pdoc`. This script is project-agnostic and uses centralized paths
from the `shared.paths` module to determine output locations.

The output Markdown files are saved to `docs/`.

Usage:
    python docs/scripts/render_docs.py
"""

from pathlib import Path
import subprocess

from shared.paths import DOCS_DIR, SRC_DIR


# -----------------------------------------------------------------------------
# Main Logic
# -----------------------------------------------------------------------------
def render_pdoc_docs(output_dir: str, source_dir: str) -> None:
    """
    Run pdoc to generate Markdown documentation.

    Args:
        output_dir: Directory where Markdown files will be written.
        source_dir: Root source directory to document.
    """
    print("📘 Generating Markdown documentation with pdoc...")
    print(f"📁 Source Directory: {source_dir}")
    print(f"📂 Output Directory: {output_dir}")

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    _ = subprocess.run(
        [
            "pdoc",
            "--output-dir",
            output_dir,
            "--template-dir",
            "docs/_pdoc_templates",  # Optional custom templates
            "--docformat",
            "google",  # Supports "google", "numpy", or "restructuredtext"
            source_dir,
        ],
        check=True,
    )

    print("✅ Documentation generation complete.")


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
def main() -> None:
    """Entrypoint for script execution."""
    render_pdoc_docs(output_dir=DOCS_DIR, source_dir=SRC_DIR)


if __name__ == "__main__":
    main()
