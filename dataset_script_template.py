import datasets

# Define metadata for your dataset
_DESCRIPTION = """
This dataset contains ...
(Add a description here – purpose, source, size, etc.)
"""

_HOMEPAGE = "https://github.com/your-username/your-repo"
_LICENSE = "MIT"  # Or "CC-BY-4.0", etc.
_CITATION = """
@article{yourcitation2024,
  title={Your Title},
  author={Author Name},
  journal={...},
  year={2024}
}
"""

# Path or URLs to the dataset files
_DATA_URLS = {
    "train": "data/train.csv",
    "test": "data/test.csv"
}

class YourDatasetName(datasets.GeneratorBasedBuilder):
    def _info(self):
        # Define the schema (features) of your dataset
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({
                "id": datasets.Value("string"),
                "text": datasets.Value("string"),
                "label": datasets.ClassLabel(names=["positive", "negative", "neutral"]),  # change as needed
            }),
            supervised_keys=("text", "label"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # Download and extract data
        data_files = dl_manager.download_and_extract(_DATA_URLS)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": data_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": data_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        # Generate examples from CSV
        import csv
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                yield idx, {
                    "id": row.get("id", str(idx)),
                    "text": row["text"],
                    "label": row["label"],
                }
