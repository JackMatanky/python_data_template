# -----------------------------------------------------------------------------
# File: python_render/render.py
# Description: Python-based template renderer for data projects
# -----------------------------------------------------------------------------

import os
from pathlib import Path

# Constants for available options
PROJECT_TYPE_LIST: dict[str, str] = {
    "data_science": "Data Science",
    "data_analysis": "Data Analysis",
    "ad_hoc": "Ad Hoc",
}

PYTHON_VERSION_LIST: list[str] = [
    ">=3.10",
    "3.10",
    "3.11",
    "3.12",
]


def enumerated_prompt(
    options: list[str] | dict[str, str], prompt: str, default_choice: str
) -> str:
    """
    Present an enumerated list prompt to the user.

    Args:
        options: A list of strings to choose from, or a dict with keys
                 as return values and values as display labels.
        prompt: The prompt to display.
        default_choice: The default index (as string) to fall back to if
                        no input is given.

    Returns:
        The selected option (either from the list or the key from the dict).
    """
    values = list(options.values()) if isinstance(options, dict) else options
    keys = list(options.keys()) if isinstance(options, dict) else options

    for i, val in enumerate(values, 1):
        print(f"{i} - {val}")

    choice = (
        input(
            f"{prompt} (Choose from [1-{len(values)}] (Default: {default_choice}): "
        ).strip()
        or default_choice
    )

    return (
        keys[int(choice) - 1]
        if choice.isdigit() and 1 <= int(choice) <= len(keys)
        else keys[int(default_choice) - 1]
    )


def prompt_vars() -> dict[str, str]:
    """
    Prompt user for all required metadata for the project.

    Returns:
        A dictionary of input values keyed by their variable names.
    """
    print("🔧 Fill in the project metadata:")
    project_type = enumerated_prompt(
        PROJECT_TYPE_LIST, "Select project_type", "1"
    )
    python_version = enumerated_prompt(
        PYTHON_VERSION_LIST, "Select Python version", "1"
    )
    project_name = input("project_name: ").strip()

    # Conditional dependency logic for pyproject.toml
    ds_dependencies = ""
    if project_type == "data_science":
        ds_dependencies = '    "scikit-learn",\n    "xgboost",'  # Newline and indentation preserved

    return {
        "PROJECT_NAME": project_name,
        "AUTHOR_NAME": input("author_name: ").strip(),
        "PROJECT_TYPE": project_type,
        "DESCRIPTION": input("description: ").strip(),
        "PYTHON_VERSION": python_version,
        "PROJECT_PATH": project_name,  # used for file paths
        "DS_DEPENDENCIES": ds_dependencies,
    }


def render_template(content: str, variables: dict[str, str]) -> str:
    """
    Replace all ${VAR} placeholders in a file's content with actual values.

    Args:
        content: The raw string content of the template file.
        variables: Dictionary of variable replacements.

    Returns:
        The content with placeholders substituted.
    """
    if "${STRUCTURE_BLOCK}" in content:
        snippet_path = (
            Path(__file__).parent.parent
            / "template_files"
            / "dir_structures"
            / f"{variables['PROJECT_TYPE']}.md"
        )
        if snippet_path.exists():
            structure_block = snippet_path.read_text(encoding="utf-8")
            content = content.replace("${STRUCTURE_BLOCK}", structure_block)
        else:
            content = content.replace(
                "${STRUCTURE_BLOCK}", "<!-- Structure snippet missing -->"
            )

    for key, val in variables.items():
        content = content.replace(f"${{{key}}}", val)
    return content


def render_directory(
    template_dir: Path, output_dir: Path, variables: dict[str, str]
) -> None:
    """
    Recursively render the contents of the template directory into a new project.

    Args:
        template_dir: Path to the directory containing template files.
        output_dir: Path where the rendered project will be created.
        variables: Dictionary of variable substitutions.
    """
    for root, dirs, files in os.walk(template_dir):
        rel_path = os.path.relpath(root, template_dir)
        target_dir = os.path.join(output_dir, rel_path)
        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)

            with open(src_file, "r", encoding="utf-8") as f:
                content = f.read()

            rendered = render_template(content, variables)

            with open(dst_file, "w", encoding="utf-8") as f:
                f.write(rendered)

            print(f"✔ Created: {dst_file}")


if __name__ == "__main__":
    """
    Entry point: Gather variables, verify output folder, and render project files.
    """
    base_dir = Path(__file__).parent
    template_dir = base_dir.parent / "template_files"

    variables = prompt_vars()
    output_dir = Path.cwd() / variables["PROJECT_PATH"]

    if output_dir.exists():
        print(
            f"⚠️  Output directory '{output_dir}' already exists. Remove it to regenerate."
        )
        exit(1)

    render_directory(template_dir, output_dir, variables)
    print(f"\n✅ Python-rendered project created in: {output_dir}\n")
