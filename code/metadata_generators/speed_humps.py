import argparse
import requests
import yaml
import os
from datetime import datetime

# Get the root of the project based on the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../../"))

# Resolve output directory from the project root
default_output_dir = os.path.join(project_root, "metadata")

def load_template(path="template_metadata.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_dataset_metadata(dataset_id):
    url = f"https://data.cityofnewyork.us/api/views/{dataset_id}.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # DEBUG: Print the structure of data
    import pprint
    pprint.pprint(data)
    
    return data

def detect_geometry_type(columns):
    for col in columns:
        dtype = col.get("dataTypeName", "").lower()
        if dtype in ["point", "location", "multipoint"]:
            return "point"
        elif dtype in ["line", "multiline"]:
            return "line"
        elif dtype in ["polygon", "multipolygon"]:
            return "polygon"
    return "unknown"

def generate_metadata(dataset_id, output_dir=".", template_path="template_metadata.yaml", data_name=None):
    template = load_template(template_path)
    data = get_dataset_metadata(dataset_id)

    columns = data.get("columns", [])
    geometry_type = detect_geometry_type(columns)

    template["dataset_id"] = dataset_id
    template["data_name"] = data_name if data_name else dataset_id  # Add data_name field
    template["name"] = data.get("name", "")
    template["description"] = data.get("description", "")
    template["source_organization"] = data.get("metadata", {}).get("owner", {}).get("displayName", "")
    template["domain"] = data.get("category", "unknown").lower()
    template["last_updated"] = datetime.utcfromtimestamp(data.get("rowsUpdatedAt", 0)).strftime('%Y-%m-%d')
    template["update_frequency"] = "unknown"

    template["access"]["primary_url"] = f"https://data.cityofnewyork.us/d/{dataset_id}"
    template["access"]["api_endpoint"] = f"https://data.cityofnewyork.us/resource/{dataset_id}.json"
    template["access"]["license"] = data.get("metadata", {}).get("license", {}).get("name", "Unknown")
    template["access"]["file_format"] = ["CSV", "JSON"]
    template["access"]["rate_limits"] = "Unknown"

    template["spatial"]["geometry_type"] = geometry_type
    template["spatial"]["coordinate_system"] = "EPSG:4326"
    template["spatial"]["coverage_area"] = "NYC"

    template["temporal"]["temporal_type"] = "static"
    template["temporal"]["temporal_resolution"] = "N/A"
    template["temporal"]["time_column"] = ""

    template["implementation"]["downloader_module"] = f"downloaders.{dataset_id}"
    template["implementation"]["processor_module"] = f"processors.{dataset_id}"
    template["implementation"]["example_notebook"] = f"examples/{dataset_id}_example.ipynb"

    template["integration_opportunities"]["spatial_joins"] = []
    template["integration_opportunities"]["temporal_alignment"] = []

    template["map_algebra"]["raster_conversion"] = {
        "suitable_for_rasterization": False,
        "recommended_cell_size": "",
        "interpolation_method": ""
    }

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{data_name}.yaml" if data_name else f"{dataset_id}.yaml"
    out_path = os.path.join(output_dir, filename)

    import yaml

    def str_presenter(dumper, data):
        if isinstance(data, str):
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    yaml.add_representer(str, str_presenter)

    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(template, f, sort_keys=False)

    print(f"✅ Metadata saved to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate metadata YAML for NYC Open Data dataset")
    parser.add_argument("--dataset_id", required=True, help="NYC Open Data dataset ID (e.g., jknp-skuy)")
    parser.add_argument("--output_dir", default=default_output_dir, help="Directory to save the YAML file")
    parser.add_argument("--template", default="template_metadata.yaml", help="Path to YAML template")
    parser.add_argument("--data_name", default=None, help="Custom data name for the metadata file (e.g., speed_humps)")

    args = parser.parse_args()
    generate_metadata(args.dataset_id, args.output_dir, args.template, args.data_name)
