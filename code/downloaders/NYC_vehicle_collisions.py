# NYC_vehicle_collisions.py
"""
NYC Motor Vehicle Collisions (Crashes) Data Downloader

Downloads the Motor Vehicle Collisions dataset as a CSV from NYC Open Data.
"""

from nyc_base_downloader import NYCDataDownloader

class NYCVehicleCollisionsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/resource/h9gi-nx95.csv"
    DATASET_NAME = "Motor Vehicle Collisions (Crashes)"

def main():
    downloader = NYCVehicleCollisionsDownloader()
    downloader.run()

if __name__ == "__main__":
    main()