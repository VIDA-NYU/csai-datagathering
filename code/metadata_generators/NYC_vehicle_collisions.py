# NYC_vehicle_collisions.py
from nyc_metadata_base import NYCMetadataGenerator

"""
NYC Vehicle Collisions Metadata Generator       
Generates metadata for the NYC Motor Vehicle Collisions - Crashes dataset.
This script is part of the NYC Open Data project and is used to create
metadata files for the Motor Vehicle Collisions dataset.
"""

class VehicleCollisionsMetadataGenerator(NYCMetadataGenerator):
    DEFAULT_DATASET_ID = "h9gi-nx95"  # NYC OpenData Motor Vehicle Collisions dataset ID
    DEFAULT_DATA_NAME = "NYC_vehicle_collisions"
    DATASET_DESCRIPTION = "NYC Motor Vehicle Collisions - Crashes dataset"

def main():
    generator = VehicleCollisionsMetadataGenerator()
    generator.run()

if __name__ == "__main__":
    main()