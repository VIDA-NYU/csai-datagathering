"""
NYC Open Data Metadata Generator - Base Class Implementation

Base class and specific generators for creating metadata YAML files from NYC Open Data.
"""

import argparse
import requests
import yaml
import os
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Optional


class NYCMetadataGenerator(ABC):
    """Base class for NYC Open Data metadata generators"""
    
    def __init__(self, template_path: str = "template_metadata.yaml"):
        # Get the root of the project based on the script's location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, "../../"))
        self.default_output_dir = os.path.join(project_root, "metadata")
        self.template_path = template_path
    
    @property
    @abstractmethod
    def DEFAULT_DATASET_ID(self) -> str:
        """Each subclass must define its default dataset ID"""
        pass
    
    @property
    @abstractmethod
    def DEFAULT_DATA_NAME(self) -> str:
        """Each subclass must define its default data name"""
        pass
    
    @property
    @abstractmethod
    def DATASET_DESCRIPTION(self) -> str:
        """Each subclass must define its dataset description for help text"""
        pass
    
    def load_template(self, path: str) -> dict:
        """Load YAML template file"""
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    def get_dataset_metadata(self, dataset_id: str) -> dict:
        """Fetch dataset metadata from NYC Open Data API"""
        url = f"https://data.cityofnewyork.us/api/views/{dataset_id}.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # DEBUG: Print the structure of data
        import pprint
        pprint.pprint(data)
        
        return data
    
    def detect_geometry_type(self, columns: list) -> str:
        """Detect geometry type from dataset columns"""
        for col in columns:
            dtype = col.get("dataTypeName", "").lower()
            if dtype in ["point", "location", "multipoint"]:
                return "point"
            elif dtype in ["line", "multiline"]:
                return "line"
            elif dtype in ["polygon", "multipolygon"]:
                return "polygon"
        return "unknown"
    
    def generate_metadata(self, dataset_id: str, output_dir: str, 
                         template_path: str, data_name: Optional[str] = None) -> None:
        """Generate metadata YAML file for the dataset"""
        template = self.load_template(template_path)
        data = self.get_dataset_metadata(dataset_id)

        columns = data.get("columns", [])
        geometry_type = self.detect_geometry_type(columns)

        template["dataset_id"] = dataset_id
        template["data_name"] = data_name if data_name else dataset_id
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

        template["implementation"]["downloader_module"] = f"downloaders.{data_name}"
        template["implementation"]["processor_module"] = f"processors.{data_name}"
        template["implementation"]["example_notebook"] = f"examples/{data_name}_example.ipynb"

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

        def str_presenter(dumper, data):
            if isinstance(data, str):
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
            return dumper.represent_scalar('tag:yaml.org,2002:str', data)

        yaml.add_representer(str, str_presenter)
        
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(template, f, sort_keys=False)

        print(f"✅ Metadata saved to {out_path}")
    
    def create_argument_parser(self) -> argparse.ArgumentParser:
        """Create standardized argument parser"""
        parser = argparse.ArgumentParser(
            description=f"Generate metadata YAML for {self.DATASET_DESCRIPTION}"
        )
        parser.add_argument("--dataset_id", 
                          default=self.DEFAULT_DATASET_ID,
                          help=f"NYC Open Data dataset ID (default: {self.DEFAULT_DATASET_ID})")
        parser.add_argument("--output_dir", 
                          default=self.default_output_dir, 
                          help="Directory to save the YAML file")
        parser.add_argument("--template", 
                          default=self.template_path, 
                          help="Path to YAML template")
        parser.add_argument("--data_name", 
                          default=self.DEFAULT_DATA_NAME,
                          help=f"Custom data name for the metadata file (default: {self.DEFAULT_DATA_NAME})")
        return parser
    
    def run(self) -> None:
        """Main execution method"""
        parser = self.create_argument_parser()
        args = parser.parse_args()
        self.generate_metadata(args.dataset_id, args.output_dir, args.template, args.data_name)

# # Specific metadata generator classes
# class SpeedHumpsMetadataGenerator(NYCMetadataGenerator):
#     DEFAULT_DATASET_ID = "jknp-skuy"
#     DEFAULT_DATA_NAME = "speed_humps"
#     DATASET_DESCRIPTION = "NYC DOT Speed Humps dataset"


# class RaisedCrosswalksMetadataGenerator(NYCMetadataGenerator):
#     DEFAULT_DATASET_ID = "uh2s-ftgh"
#     DEFAULT_DATA_NAME = "raised_crosswalks"
#     DATASET_DESCRIPTION = "NYC DOT Raised Crosswalk Locations dataset"


# class VehicleCollisionsMetadataGenerator(NYCMetadataGenerator):
#     DEFAULT_DATASET_ID = "h9gi-nx95"
#     DEFAULT_DATA_NAME = "NYC_vehicle_collisions"
#     DATASET_DESCRIPTION = "NYC Motor Vehicle Collisions - Crashes dataset"


# class NYC311MetadataGenerator(NYCMetadataGenerator):
#     DEFAULT_DATASET_ID = "jrb2-thup"
#     DEFAULT_DATA_NAME = "nyc_311"
#     DATASET_DESCRIPTION = "NYC 311 Service Requests dataset"


# # Individual script entry points
# def main_speed_humps():
#     generator = SpeedHumpsMetadataGenerator()
#     generator.run()


# def main_raised_crosswalks():
#     generator = RaisedCrosswalksMetadataGenerator()
#     generator.run()


# def main_vehicle_collisions():
#     generator = VehicleCollisionsMetadataGenerator()
#     generator.run()


# def main_nyc_311():
#     generator = NYC311MetadataGenerator()
#     generator.run()


# # For running as individual scripts
# if __name__ == "__main__":
#     # This would be different in each individual file
#     # speed_humps.py would call main_speed_humps()
#     # raised_crosswalks.py would call main_raised_crosswalks()
#     # NYC_vehicle_collisions.py would call main_vehicle_collisions()
#     # nyc_311.py would call main_nyc_311()
#     pass