#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# Bootstrap Script for New Python Project
# -----------------------------------------------------------------------------
# Sets up:
# - Git (optional)
# - PYTHONPATH with direnv
# - src/ layout
# - Python virtual environment (.venv)
# -----------------------------------------------------------------------------

set -e

PROJECT_NAME="${1:-my_project}"
INIT_GIT=true
CREATE_VENV=true

echo "📁 Bootstrapping new Python project: $PROJECT_NAME"
mkdir -p "$PROJECT_NAME/src" "$PROJECT_NAME/notebooks" "$PROJECT_NAME/data"

cd "$PROJECT_NAME"

# ------------------------
# Optional Git Init
# ------------------------
if [ "$INIT_GIT" = true ]; then
  echo "🔧 Initializing Git repository..."
  git init -b main
  echo ".venv/" >> .gitignore
  echo "__pycache__/" >> .gitignore
  echo "*.pyc" >> .gitignore
fi

# ------------------------
# Direnv Setup
# ------------------------
echo "📦 Configuring .envrc for direnv..."
cat <<EOF > .envrc
export PYTHONPATH=./src
EOF

direnv allow

# ------------------------
# Virtual Environment
# ------------------------
if [ "$CREATE_VENV" = true ]; then
  echo "🐍 Creating virtual environment in .venv..."
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
fi

echo "✅ Project bootstrapped!"
echo "➡️  Next steps:"
echo "   - Activate direnv: \`cd $PROJECT_NAME\`"
echo "   - Use \`.venv/bin/activate\` or rely on direnv + justfile integration"
