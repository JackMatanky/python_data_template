# {{ PROJECT_NAME }}

{{ description }}

## Project Overview

This project is structured to support one of three types of workflows:

- `data_science`: Includes model training infrastructure and experiments
- `data_analysis`: Focuses on EDA, reporting, and visualization
- `ad_hoc`: Lightweight, flexible workspaces for quick exploration

## Directory Structure

For `src` layout vs. flat layout tradeoff, see the [Python Packaging User Guide](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)

### Data Science

```
${PROJECT_NAME}/
├── .gitignore                    <- Git exclusions for cache, environments, and temporary files
├── jupytext.toml                 <- Jupytext configuration for notebook pairing (e.g., ipynb <-> py:percent)
├── justfile                      <- Reproducible task runner (e.g., `just init`, `just run`)
├── pyproject.toml                <- Project metadata and dependency specification (PEP 621, used with uv)
├── README.md                     <- Top-level README with setup instructions and project overview
│
├── data/                         <- Data, structured by transformation stage
│   ├── 00_external/              <- External data from APIs, vendors, or third parties
│   ├── 01_raw/                   <- Immutable raw data as originally acquired
│   ├── 02_interim/               <- Data that has been lightly cleaned or reshaped
│   └── 03_processed/             <- Fully cleaned, transformed data used for modeling
│
├── notebooks/                    <- Jupyter notebooks (paired with `.py` files if Jupytext is used)
│   ├── 01_cleaning.ipynb         <- Initial data loading and sanitization
│   ├── 02_exploration.ipynb      <- Exploratory Data Analysis (EDA)
│   ├── 03_features.ipynb         <- Feature engineering and selection
│   └── 04_modeling.ipynb         <- Model development and evaluation
│                                 <- Naming: `NN_description.ipynb` or `NN_initials_description.ipynb`
│
├── reports/                      <- Outputs generated from analysis or notebooks
│   ├── figures/                  <- Plots and visual assets used in reports
│   └── report.md                 <- Summarized findings, insights, or deliverables
│
├── references/                   <- Background material: data dictionaries, papers, manuals, etc.
│
├── models/                       <- Serialized models, intermediate predictions, and metadata
│   └── README.md                 <- Optional: model architecture notes, version history, etc.
│
├── docs/                         <- Optional mkdocs or Sphinx documentation project
│
└── src/                          <- Core logic for data, features, modeling, and plotting
    ├── __init__.py               <- Makes `src` a proper Python module
    ├── config.py                 <- Global configuration (e.g., paths, constants, flags)
    ├── dataset.py                <- Data I/O, acquisition, and initial parsing logic
    ├── features.py               <- Feature engineering methods
    ├── modeling/                 <- Training and inference code
    │   ├── __init__.py
    │   ├── train.py              <- Model fitting logic
    │   └── predict.py            <- Evaluation and inference utilities
    └── plots.py                  <- Plotting and visualization code
```

### Data Analysis

```
${PROJECT_NAME}/
├── .gitignore                    <- Git exclusions for caches, environments, notebook checkpoints, etc.
├── jupytext.toml                 <- Configuration for notebook pairing (.ipynb <-> .py) if Jupytext is used
├── justfile                      <- Task runner for reproducible automation (e.g., `just init`, `just notebooks`)
├── pyproject.toml                <- Project configuration and dependency management (PEP 621, used with uv)
├── README.md                     <- Project overview, setup instructions, and documentation entry point
│
├── data/                         <- Input data organized by level of transformation
│   ├── 00_external/              <- Raw data from third-party sources (e.g., APIs, vendors)
│   ├── 01_raw/                   <- Unmodified original data as received or collected
│   ├── 02_interim/               <- Lightly cleaned or merged data
│   └── 03_processed/             <- Final dataset used in analysis or visualizations
│
├── notebooks/                    <- Jupyter notebooks used to explore and analyze data
│   ├── 01_cleaning.ipynb         <- Data loading, inspection, and basic cleaning steps
│   ├── 02_exploration.ipynb      <- Exploratory data analysis (EDA), correlations, distributions
│   ├── 03_visualization.ipynb    <- Static and interactive plots for storytelling
│   └── 04_summary.ipynb          <- Key takeaways, stakeholder-oriented results
│                                 <- Naming convention: `NN_topic.ipynb` (or `NN_initials_topic.ipynb`)
│
├── reports/                      <- Generated outputs from the analysis
│   ├── figures/                  <- Plots, charts, and visual assets
│   └── report.md                 <- Markdown-based executive summary or technical report
│
├── references/                   <- Contextual and supporting resources: data dictionaries, manuals, papers
│
├── docs/                         <- Optional documentation site (e.g., mkdocs or Sphinx config and source)
│
└── src/                          <- Core reusable analysis logic
    ├── __init__.py               <- Marks `src` as a Python module
    ├── config.py                 <- Centralized configuration (e.g., file paths, options)
    ├── dataset.py                <- Scripts to read, clean, and join data
    ├── features.py               <- Code for engineered or aggregated variables
    └── plots.py                  <- Common chart templates or wrappers (e.g., seaborn, matplotlib)
```

### Ad Hoc Analysis

```
${PROJECT_NAME}/
├── .gitignore                    <- Ignores outputs, checkpoints, and system files
├── jupytext.toml                 <- Optional: notebook pairing config for Jupytext users
├── justfile                      <- Optional: command shortcuts (e.g., `just run`)
├── pyproject.toml                <- Dependency list and minimal project metadata
├── README.md                     <- Brief description or goal of the notebook/project
│
├── data/
│   └── 01_raw/                   <- Manual uploads or copy-paste data dumps used in the analysis
│
├── notebooks/                    <- One or more scratch notebooks
│   └── 01_analysis.ipynb         <- Main exploratory or experimental notebook
│                                 <- You can pair it with a `.py` if using Jupytext
│
└── src/                          <- Lightweight helper code for data loading or preprocessing
    ├── __init__.py
    └── quickload.py              <- One-file utility for reading, renaming, or filtering data
```

## ⚙️ Setup Instructions

Install [uv](https://github.com/astral-sh/uv) if not already:

```bash
pip install uv
```

Then run:

```bash
just init
```

This will:

- Create a virtual environment via `uv`
- Install all dependencies

## 📓 Working with Notebooks

This project uses [Jupytext](https://jupytext.readthedocs.io/en/latest/) to pair Jupyter notebooks (`.ipynb`) with Python scripts (`.py`) using the `percent` format.

To sync notebook pairs:

```bash
just notebooks
```

Jupytext configuration is managed in `jupytext.toml`.

## 🏃 Quick Commands

```bash
just init        # Create virtual environment and install dependencies
just notebooks   # Sync notebooks with paired .py files
just run         # Run main script (customize as needed)
```

## 📦 Dependencies

Dependencies are listed in `pyproject.toml` under `[project]`. Use `uv pip install` to install them after environment creation.

```toml
[project]
dependencies = [
  "pandas",
  "numpy",
  "matplotlib",
  "jupytext",
  ...
]
```

## Notes

- Code formatting is handled with `ruff`
- Dependency management is via `uv` and `pyproject.toml`
- Notebook pairing and scripting is powered by `jupytext`
- Use `just` for all reproducible tasks (init, lint, run)


## 🔗 References

- [uv package manager](https://github.com/astral-sh/uv)
- [Jupytext documentation](https://jupytext.readthedocs.io/)
- [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [Just command runner](https://github.com/casey/just)

## Acknowledgments

- [Cookiecutter](https://cookiecutter.readthedocs.io/)
- [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org)
