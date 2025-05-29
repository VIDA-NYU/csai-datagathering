import argparse
import json
import pandas as pd
from huggingface_hub import HfApi, login, hf_hub_download
import datamart_profiler  # Import datamart-profiler

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate and add profiling JSON to an existing Hugging Face dataset repository")
parser.add_argument("--token", required=True, help="Hugging Face token")
parser.add_argument("--repo_id", required=True, help="Hugging Face repository ID (e.g., 'oscur/pluto')")
parser.add_argument("--csv_filename", required=True, help="Name of the CSV file in the repository")
args = parser.parse_args()

# Use the arguments
token_value = args.token
repo_id = args.repo_id
csv_filename = args.csv_filename

# Login to Hugging Face
login(token=token_value)
api = HfApi()

# Download the CSV file from the Hugging Face repository
try:
    csv_path = hf_hub_download(repo_id=repo_id, filename=csv_filename, repo_type="dataset")
    print(f"CSV file '{csv_filename}' has been downloaded from the repository.")
except Exception as e_download:
    print(f"An error occurred while downloading the CSV file: {e_download}")
    exit(1)

# Generate the profiling JSON
try:
    df_data = pd.read_csv(csv_path)
    profile = datamart_profiler.process_dataset(csv_path, include_sample=True, plots=True)
    profile_json = json.dumps(profile, indent=4)
    profile_filename = "profiling_metadata.json"
    print(f"Profiling JSON data has been generated.")
except Exception as e_profile:
    print(f"An error occurred while generating the profiling JSON: {e_profile}")
    exit(1)

# Upload the profiling JSON data to the repository
try:
    api.upload_file(
        path_or_fileobj=profile_json.encode("utf-8"),  # Convert JSON string to bytes
        path_in_repo=profile_filename,
        repo_id=repo_id,
        repo_type="dataset"
    )
    print(f"Profiling JSON data has been uploaded to the repository '{repo_id}' as '{profile_filename}'.")
except Exception as e_upload:
    print(f"An error occurred while uploading the profiling JSON data: {e_upload}")

###############################################################################
########## Uploading profiling metadata to Hugging Face repository ############

# Note: This script assumes that the Hugging Face repository already exists and contains the specified CSV file.
# run this `python` script to generates profiling metadata for a CSV file in a Hugging Face dataset repository
# and uploads it as a JSON file named 'profiling_metadata.json'.
# Usage:
# python add_profiling_to_hugging_face.py --token <your_token> --repo_id <your_repo_id> --csv_filename <your_csv_filename>
# Example usage:                
# python add_profiling_to_hugging_face.py --token <your_token> --repo_id oscur/taxisvis1M --csv_filename taxisvis1M.csv
###############################################################################