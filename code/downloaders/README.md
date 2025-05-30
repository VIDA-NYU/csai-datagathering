
# Data Downloaders

This folder contains Python scripts to **automatically download and save raw data** from various public data sources, including NYC Open Data and others. 

Because data can be provided in multiple formats (CSV, JSON, Parquet, etc.), each dataset has its own dedicated downloader script that handles the specifics of retrieving and saving the data.

## Folder Structure

```
code/downloaders/
├── speed_humps.py               # Download Speed Humps dataset (CSV)
├── raised_crosswalks.py         # Download Raised Crosswalks dataset (CSV)
├── nyc_vehicle_collisions.py    # Download Vehicle Collisions (Crashes) dataset (CSV)
├── nyc_311_data.py              # Download NYC 311 Requests dataset (CSV)
├── README.md                    # This file
└── ...                          # Add one script per dataset as needed
```

## Requirements

- Python 3.7+
- `requests` module
- Additional dependencies may be required depending on the dataset (e.g., `pandas`, `pyarrow` for Parquet)

Install basic dependencies with:

```bash
pip install requests
```

## How to Use

Each script accepts `-o` or `--output` to specify the output file path. The output file format depends on the dataset and script implementation.

Ensure the `data/` folder exists:

```bash
mkdir -p data
```
> 🔒 **Note:** The `data/` folder will not be committed to this repository. Instead, all collected data will be uploaded to a Hugging Face dataset repository for sharing and versioning. If needed, post-processing and format conversions should be handled in [code/processors](./) .

### Example usage:

```bash
python speed_humps.py -o data/speed_humps.csv
python raised_crosswalks.py -o data/raised_crosswalks.csv
python nyc_vehicle_collisions.py -o data/nyc_vehicle_collisions.json
python nyc_311_data.py -o data/nyc_311.json
```

You may optionally provide a Socrata API app token with `--app-token YOUR_TOKEN` to avoid rate limits on some endpoints.

## Notes

- Datasets vary in size and format; some may require significant memory or filtering.
- Downloaders are designed to be minimal, focusing on retrieving raw data.

## Contributing

To add a new downloader:

1. Add a `Python` script in [code/downloaders](./) that fetches and saves the raw dataset.
   - If multiple scripts are needed for one dataset, organize them in a subdirectory named after the dataset ID or source (e.g., `code/downloaders/your_dataset_id/`).
2. Add CLI usage instructions to this `README.md`.
3. Ensure your script handles the dataset's specific format and retrieval method.

---
