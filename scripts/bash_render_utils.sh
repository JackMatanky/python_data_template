#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# File: scripts/_render_utils.sh
# Description: Shared rendering utilities for Bash-based template engine
# -----------------------------------------------------------------------------

setup_output_dir() {
  # Convert project name to snake_case for folder naming
  PROJECT_PATH="$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/_/g' | sed -E 's/^_+|_+$//g')"
  OUTPUT_DIR="$(pwd)/$PROJECT_PATH"

  # Define source template and structure snippet locations
  TEMPLATE_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")/../template_files" && pwd)"
  STRUCTURE_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")/../directory_structures" && pwd)"

  export PROJECT_PATH OUTPUT_DIR TEMPLATE_DIR STRUCTURE_DIR

  # Avoid overwriting an existing project folder
  if [ -d "$OUTPUT_DIR" ]; then
    echo "⚠️  Output directory '$OUTPUT_DIR' already exists. Remove it to regenerate."
    exit 1
  fi

  mkdir -p "$OUTPUT_DIR"

  # Conditionally inject dependencies for data science projects
  if [[ "$PROJECT_TYPE" == "data_science" ]]; then
    DS_DEPENDENCIES='    "scikit-learn",\n    "xgboost",'
  else
    DS_DEPENDENCIES=""
  fi

  export DS_DEPENDENCIES
}

render_all_templates() {
  while IFS= read -r -d '' file; do
    rel_path="${file#$TEMPLATE_DIR/}"
    dest_file="$OUTPUT_DIR/$rel_path"
    render_template "$file" "$dest_file"
  done < <(find "$TEMPLATE_DIR" -type f -print0)
}

render_template() {
  local src="$1"
  local dst="$2"

  mkdir -p "$(dirname "$dst")"

  # Use envsubst for variable replacement, mask STRUCTURE_BLOCK first
  local rendered
  rendered=$(envsubst < "$src" | sed "s|\${STRUCTURE_BLOCK}|___STRUCTURE_BLOCK___|g")

  # Inject snippet if placeholder is present
  if grep -q "___STRUCTURE_BLOCK___" <<< "$rendered"; then
    local snippet_file="$STRUCTURE_DIR/${PROJECT_TYPE}.md"
    if [[ -f "$snippet_file" ]]; then
      echo "🔧 Injected structure from: $snippet_file"
      rendered="$(echo "$rendered" | sed "/___STRUCTURE_BLOCK___/ {
        r $snippet_file
        d
      }")"
    else
      rendered="${rendered//___STRUCTURE_BLOCK___/<!-- Structure snippet missing -->}"
    fi
  fi

  echo "$rendered" > "$dst"
  echo "✔ Created: $dst"
}
