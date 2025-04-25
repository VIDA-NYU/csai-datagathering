import argparse
from datasets import load_dataset, Dataset
import pandas as pd
import os
import csv
import datasets
from huggingface_hub import HfApi, create_repo, login

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Upload CSV to Hugging Face Hub")
parser.add_argument("--token", required=True, help="Hugging Face token")
parser.add_argument("--organization", required=True, help="Hugging Face organization name")
parser.add_argument("--repo_name", required=True, help="Repository name")
parser.add_argument("--csv_filename", required=True, help="Path to the CSV file")
args = parser.parse_args()

# Use the arguments
token_value = args.token
organization = args.organization
repo_name = args.repo_name
csv_filename = args.csv_filename
repo_id = f"{organization}/{repo_name}"

# Login to Hugging Face
login(token=token_value)
api = HfApi()

# Create the repository only if it doesn't already exist
try:
    create_repo(repo_id, repo_type="dataset", exist_ok=True)
    print(f"Repository '{repo_id}' is ready.")
except Exception as e:
    print(f"An error occurred while creating the repository: {e}")

try:
    # Attempt to load the dataset directly from the CSV file
    dataset = Dataset.from_csv(csv_filename)
except Exception as e1:
    # If the first attempt fails, print the error and try to load it using pandas
    print(f"First attempt Failed to create dataset from CSV file: {e1}")
    try:
        # Second attempt to create the dataset using pandas
        df_data = pd.read_csv(csv_filename)
        dataset = Dataset.from_pandas(df_data)
    except Exception as e2:
        print(f"Second attempt to create dataset from pandas DataFrame failed: {e2}")
        try:
            # Third Attempt to create the dataset definng the features
            # This is a fallback method to ensure the dataset can be created
            # even if the CSV file is not well-formed
            # This method uses the csv module to read the CSV file and define the features
            # based on the first row of the CSV file
            # Ensure the CSV file is in the same directory as the script
            # or provide the full path to the CSV file
            csv_path = os.path.join(os.path.dirname(csv_filename), os.path.basename(csv_filename))
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                fieldnames = reader.fieldnames

            features_code = ",\n                ".join([
                f'"{col}": datasets.Value("string")' for col in fieldnames
            ])
            features = datasets.Features({
                **{col: datasets.Value("string") for col in fieldnames}
            })
            dataset = Dataset.from_csv(csv_filename, features=features)
        except Exception as e3:
            # If all attempts fail, print the error and raise an exception
            # to indicate that the dataset could not be created
            # This is the last fallback method to ensure the dataset can be created
            print(f"Third attempt: Failed to create dataset from CSV file with fallback method: {e3}")
            raise

# Push the CSV file directly to the repository
try:
    api.upload_file(
        path_or_fileobj=csv_filename,
        path_in_repo=os.path.basename(csv_filename),
        repo_id=repo_id,
        repo_type="dataset"
    )
    print(f"CSV file '{csv_filename}' has been pushed to the repository.")
except Exception as e:
    print(f"An error occurred while pushing the CSV file: {e}")

# Push the dataset to the repository
dataset.push_to_hub(repo_id)