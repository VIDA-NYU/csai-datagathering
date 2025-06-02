"""
Upload CSV-based datasets to Hugging Face Datasets Hub.

Instructions:
1. Place your CSV file in a folder (e.g., traffic_data/)
3. Ensure you have a Hugging Face token. Contact OSCUR members or Sonia Castelo (scq202@nyu.edu) to get the token.
2. Modify the following variables:
   - local_dataset_path
   - csv_filename
   - repo_id
   - dataset_title
   - dataset_description
4. Run: python upload.py
"""

import os
import csv
from huggingface_hub import HfApi

# === Load Hugging Face token ===
# api = HfApi(token=os.getenv("HF_TOKEN"))  # Make sure HF_TOKEN is exported

# === Define paths and metadata (only modify these!) ===
api = HfApi(token="<hf_your_actual_token_here>")
local_dataset_path = "<path-to-folder-containing-data>"  # Path to folder with your dataset
csv_filename = "<data.csv>"  # Your CSV file
repo_id = "<your-username/hugging-face-dataset-repository>"  # Hugging Face dataset repo ID
dataset_title = "<Dataset Title>"  # For README title
dataset_description = "<This dataset contains ....>"  # For README

# === Ensure README.md exists ===
readme_path = os.path.join(local_dataset_path, "README.md")
if not os.path.exists(readme_path):
    with open(readme_path, "w", encoding="utf-8") as readme:
        readme.write(f"# {dataset_title}\n\n")
        readme.write(dataset_description + "\n")

# === Auto-generate dataset_script.py ===
csv_path = os.path.join(local_dataset_path, csv_filename)
with open(csv_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames

features_code = ",\n                ".join([
    f'"{col}": datasets.Value("string")' for col in fieldnames
])

dataset_script_content = f'''\
import csv
import datasets

class GenericCSVLoader(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="Generic CSV loader script for Hugging Face Datasets.",
            features=datasets.Features({{
                {features_code}
            }}),
            supervised_keys=None,
        )

    def _split_generators(self, dl_manager):
        data_path = dl_manager.download_and_extract("{csv_filename}")
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={{"filepath": data_path}})
        ]

    def _generate_examples(self, filepath):
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                yield i, row
'''

script_path = os.path.join(local_dataset_path, "dataset_script.py")
with open(script_path, "w", encoding="utf-8") as script_file:
    script_file.write(dataset_script_content)

print("✅ dataset_script.py generated.")

# === Upload everything to Hugging Face Hub ===
api.upload_folder(
    folder_path=local_dataset_path,
    repo_id=repo_id,
    repo_type="dataset",
)

print(f"✅ Dataset uploaded to https://huggingface.co/datasets/{repo_id}")
