# raised_crosswalks.py
from nyc_metadata_base import NYCMetadataGenerator

"""
NYC Raised Crosswalks Metadata Generator       
Generates metadata for the NYC DOT Raised Crosswalk Locations dataset.
This script is part of the NYC Open Data project and is used to create
metadata files for the Raised Crosswalk Locations dataset.
"""

class RaisedCrosswalksMetadataGenerator(NYCMetadataGenerator):
    DEFAULT_DATASET_ID = "uh2s-ftgh"  # NYC OpenData Raised Crosswalk Locations dataset ID
    DEFAULT_DATA_NAME = "raised_crosswalks"
    DATASET_DESCRIPTION = "NYC DOT Raised Crosswalk Locations dataset"

def main():
    generator = RaisedCrosswalksMetadataGenerator()
    generator.run()

if __name__ == "__main__":
    main()