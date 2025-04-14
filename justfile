# -----------------------------------------------------------------------------
# File: justfile
# Description: Task runner to render a project template using Bash or Python
# -----------------------------------------------------------------------------

# Default project initialization command (Python renderer)
init:
	just render-python

# Run the Python-based template renderer
render-python:
	python3 render_scripts/python_render.py

# Run the Bash-based template renderer
render-bash:
	bash render_scripts/bash_render.sh
