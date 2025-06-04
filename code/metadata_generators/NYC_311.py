# NYC_311.py
from nyc_metadata_base import NYCMetadataGenerator

"""
NYC 311 Service Requests Metadata Generator       
Generates metadata for the NYC 311 Service Requests dataset.
This script is part of the NYC Open Data project and is used to create
metadata files for the 311 Service Requests dataset.
"""

class NYC311MetadataGenerator(NYCMetadataGenerator):
    DEFAULT_DATASET_ID = "jrb2-thup"  # NYC OpenData 311 Service Requests dataset ID
    DEFAULT_DATA_NAME = "NYC_311"
    DATASET_DESCRIPTION = "NYC 311 Service Requests dataset"

def main():
    generator = NYC311MetadataGenerator()
    generator.run()

if __name__ == "__main__":
    main()