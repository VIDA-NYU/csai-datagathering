#!/bin/bash

# Accept parameters from the command line
TOKEN=$1
ORGANIZATION=$2
REPO_NAME=$3
CSV_FILENAME=$4

# Ensure required Python packages are installed
pip install --quiet datasets huggingface_hub

# Run the Python script with the parameters
python upload_csv_hugging_face.py --token "$TOKEN" --organization "$ORGANIZATION" --repo_name "$REPO_NAME" --csv_filename "$CSV_FILENAME"
