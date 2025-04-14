# ${PROJECT_NAME}

${DESCRIPTION}

---

## Project Structure

The following structure is automatically generated based on the selected project type:

${STRUCTURE_BLOCK}

---

## Setup Instructions

```bash
# Create virtual environment and install dependencies (requires uv)
just init
```

---

## Common Tasks

```bash
# Pair Jupyter notebooks with scripts
just notebooks

# Lint and format code
just lint
just format

# Run your main application logic
just run
```

---

## Tooling

This project uses:
- [uv](https://github.com/astral-sh/uv) — dependency management
- [ruff](https://docs.astral.sh/ruff/) — linter and formatter
- [jupytext](https://jupytext.readthedocs.io/) — notebook syncing

---

## Acknowledgements

- Project inspired by [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)
- Documentation template from [GitHub Docs](https://docs.github.com/en)
