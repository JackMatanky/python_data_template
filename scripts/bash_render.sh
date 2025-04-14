#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# File: scripts/bash_render.sh
# Description: Entry point for Bash-based project rendering
# -----------------------------------------------------------------------------

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source "$SCRIPT_DIR/bash_render_prompts.sh"
source "$SCRIPT_DIR/bash_render_utils.sh"

# Collect user inputs (project name, type, version, etc.)
prompt_project_metadata

# Set up output path, directory names, etc.
setup_output_dir

# Render the entire project from template directory
render_all_templates

echo -e "\n✅ Bash-rendered project created in: $OUTPUT_DIR\n"
