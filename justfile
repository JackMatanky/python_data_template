# -----------------------------------------------------------------------------
# File: justfile
# Description: Template bootstrap system for Python data projects
# -----------------------------------------------------------------------------
# Resource: https://github.com/tataraba/dotfiles/blob/main/justfile

# >>> Global Settings <<<
set dotenv-load := false
set export := true


# >>> Default Configuration <<<
name := "data-project"
layout := "flat"  # Options: flat | src


# >>> Default Task <<<

# Show the list of available tasks when no command is given
@_default:
    just --list


# >>> Internal: Render Logic <<<

# Run the Python-based template renderer script
_render-python:
    #!/usr/bin/env bash
    set -euo pipefail
    python3 render_scripts/python_render.py

# Run the Bash-based template renderer script
_render-bash:
    #!/usr/bin/env bash
    set -euo pipefail
    bash render_scripts/bash_render.sh


# >>> Template Initialization <<<

# Initialize the project structure and copy shared configs
_template-init layout name:
    #!/usr/bin/env bash
    set -euo pipefail

    LAYOUT="{{layout}}"
    PROJECT="{{name}}"

    mkdir -p "$PROJECT"
    cp .template/.gitignore "$PROJECT"/.gitignore
    cat .template/pyproject.shared.toml >> "$PROJECT"/pyproject.toml

    if [ "$LAYOUT" == "src" ]; then
        mkdir -p "$PROJECT"/src/"$PROJECT"
        touch "$PROJECT"/src/"$PROJECT"/__init__.py
        cp .template/main.py "$PROJECT"/src/"$PROJECT"/main.py
    else
        cp .template/main.py "$PROJECT"/main.py
    fi

    cd "$PROJECT"
    touch .envrc && echo "layout python3" >> .envrc
    direnv allow || true


# >>> Install Tooling <<<

# Install pipx if it is not already installed
_install-pipx:
    #!/usr/bin/env bash
    set -euo pipefail
    if ! command -v pipx &> /dev/null; then
        echo "pipx is not installed. Installing..."
        python3 -m pip install --user pipx
        python3 -m pipx ensurepath
    fi

# Install the Jinja2 CLI renderer via pipx
_install-jinja2:
    #!/usr/bin/env bash
    set -euo pipefail
    pipx install jinja2-cli


# >>> Bootstrap Commands <<<

# Full bootstrap: initialize layout and render the project
bootstrap layout name:
    #!/usr/bin/env bash
    set -euxo pipefail
    just _template-init {{ layout }} {{ name }}
    cd {{ name }} && just render-python


# >>> Public Task: Create Project <<<

# Public command to create a new project using layout and name
@create name=name layout="flat":
    mkdir -p {{ name }}
    just bootstrap {{ layout }} {{ name }}


# >>> Renderer Entrypoints <<<

# Manually trigger Python renderer
render-python:
    just _render-python

# Manually trigger Bash renderer
render-bash:
    just _render-bash


# >>> Formatter <<<

# Format this justfile using unstable formatting features
@_fmt:
    just --fmt --unstable

# # Default project initialization command (Python renderer)
# init:
# 	just render-python
#
# # Run the Python-based template renderer
# render-python:
# 	python3 render_scripts/python_render.py
#
# # Run the Bash-based template renderer
# render-bash:
# 	bash render_scripts/bash_render.sh
#
# bootstrap name:
#     bash ./scripts/bootstrap-project.sh {{name}}
