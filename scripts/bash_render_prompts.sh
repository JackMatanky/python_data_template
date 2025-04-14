#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# File: scripts/_prompts.sh
# Description: Prompt user for project metadata and set environment variables
# -----------------------------------------------------------------------------

prompt_project_metadata() {
  read -rp "Project Name: " PROJECT_NAME
  read -rp "Author Name: " AUTHOR_NAME
  read -rp "Description: " DESCRIPTION

  printf "\nSelect project type:\n"
  echo "1 - Data Science (Default)"
  echo "2 - Data Analysis"
  echo "3 - Ad Hoc"
  read -rp "Choose from [1/2/3]: " TYPE_CHOICE
  TYPE_CHOICE=${TYPE_CHOICE:-1}

  case "$TYPE_CHOICE" in
    1) PROJECT_TYPE="data_science";;
    2) PROJECT_TYPE="data_analysis";;
    3) PROJECT_TYPE="ad_hoc";;
    *) PROJECT_TYPE="data_science";;
  esac

  printf "\nSelect Python version:\n"
  echo "1 - >=3.10 (Default)"
  echo "2 - 3.11"
  echo "3 - 3.12"
  read -rp "Choose from [1/2/3]: " PYVER_CHOICE
  PYVER_CHOICE=${PYVER_CHOICE:-1}

  case "$PYVER_CHOICE" in
    1) PYTHON_VERSION=">=3.10";;
    2) PYTHON_VERSION="3.11";;
    3) PYTHON_VERSION="3.12";;
    *) PYTHON_VERSION=">=3.10";;
  esac

  export PROJECT_NAME AUTHOR_NAME DESCRIPTION PROJECT_TYPE PYTHON_VERSION
}
