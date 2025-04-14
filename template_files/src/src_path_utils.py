"""
src_path_utils.py

Utility to locate the project root and add the top-level 'src/' folder to sys.path.
Useful in Jupyter notebooks where the working directory may be deeply nested.

Usage:
    import src_path_utils
    src_path_utils.add_src_to_sys_path()

    # or use the magic command after registering:
    %load_ext src_path_utils
    %add_src_path
"""

from pathlib import Path
import sys


def find_project_root(markers: list[str] | None) -> Path:
    """
    Traverse upward from the current working directory to find the project
    root by looking for specific marker files or directories
    (e.g. .git, pyproject.toml, src).

    Args:
        markers (List[str] | None): List of marker filenames or directory
                                    names that identify the project root.
                                    Defaults to common ones.

    Returns:
        Path: The path to the project root.

    Raises:
        FileNotFoundError: If no marker is found in any parent directories.
    """
    if markers is None:
        markers = ["pyproject.toml", ".git", "src"]

    current: Path = Path().resolve()
    for parent in [current] + list(current.parents):
        if any((parent / marker).exists() for marker in markers):
            return parent

    raise FileNotFoundError(
        f"Could not find any of the project markers: {markers}"
    )


def add_src_to_sys_path(verbose: bool = True) -> None:
    """
    Add the top-level 'src/' directory to sys.path for importing modules.

    Args:
        verbose (bool): If True, prints what was added or warns if not found.
    """
    try:
        project_root: Path = find_project_root()
        src_path: Path = project_root / "src"

        if not src_path.exists():
            if verbose:
                print(f"[!] 'src/' directory not found at: {src_path}")
            return

        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
            if verbose:
                print(f"[✓] Added to sys.path: {src_path}")
        elif verbose:
            print(f"[i] src/ path already in sys.path: {src_path}")

    except FileNotFoundError as e:
        if verbose:
            print(f"[!] {e}")


# ---- Jupyter magic command support ----
def load_ipython_extension(ipython):
    """
    Register %add_src_path magic for use in Jupyter notebooks.
    Called automatically by `%load_ext src_path_utils`.
    """
    from IPython.core.magic import register_line_magic

    @register_line_magic
    def add_src_path(line):
        """
        Line magic to add the project's 'src/' folder to sys.path.

        Usage:
            %add_src_path
        """
        add_src_to_sys_path()

    if hasattr(ipython, "register_magic_function"):
        ipython.register_magic_function(add_src_path, "line")
