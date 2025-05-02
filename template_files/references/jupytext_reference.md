# 📓 Jupytext Integration

> Sync notebooks and Python scripts for better version control and collaboration.

## ✅ What Problem Does Jupytext Solve?

Jupyter notebooks are powerful but:
- Hard to version control
- Difficult to diff and review
- Cluttered with outputs and metadata

**Jupytext** pairs notebooks (`.ipynb`) with lightweight Python scripts (`.py`) using cell markers like `# %%`, making them easier to track, diff, and lint in code reviews.

---

## 🛠️ Use Cases

- Clean diffs and Git history for notebooks
- Code reviews in plain Python
- Script–notebook duality (write as `.py`, run as `.ipynb`)
- Cleaner collaboration in data science and ML workflows

---

## 🚀 How It Works

This project uses **percent format** pairing:
- Jupyter notebooks live in: `notebooks/`
- Paired scripts live in: `_scripts/`

Configured in `pyproject.toml`:
```toml
[tool.jupytext]
formats = "ipynb,py:percent"
[tool.jupytext.formats]
"notebooks/" = "ipynb"
"_scripts/" = "py:percent"
```

To sync both versions:

```sh
jupytext --sync notebooks/**/*.ipynb
```

## 📌 Best Practices

- Sync after editing (`jupytext --sync`)
- Don’t edit `.ipynb` and `.py` at the same time
- Use `.py` for review, `.ipynb` for execution
- Optionally ignore `.ipynb` in Git if not needed

---

## 🔗 Resources

- Docs: [jupytext.readthedocs.io](https://jupytext.readthedocs.io/)
- Formats: [Jupytext pairing modes](https://jupytext.readthedocs.io/en/latest/formats.html)
- VS Code: [Jupytext in VS Code](https://marketplace.visualstudio.com/items?itemName=donjayamanne.jupytext)

## 🔄 Pre-Commit Integration

To ensure `.ipynb` and `.py` notebook pairs stay in sync, we use a [pre-commit](https://pre-commit.com/) hook that runs `jupytext --sync` before each commit.

### 📁 Configuration

Add the following to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/mwouts/jupytext
  rev: "1.17.0"  # Use the version matching your setup
  hooks:
    - id: jupytext
      name: jupytext sync
      entry: jupytext --sync
      language: python
      types: [python, jupyter]
      files: ^notebooks/.*\.ipynb$
```

This syncs all `.ipynb` notebooks under `notebooks/` with their paired `.py` scripts.

### ⚙️ Setup

Run the following in your project root:

```bash
pip install pre-commit jupytext
pre-commit install
pre-commit autoupdate
```

### ✅ Benefits

- Prevents stale `.py` or `.ipynb` files
- Catches unsynced changes before commit
- Encourages clean, version-controlled notebooks
