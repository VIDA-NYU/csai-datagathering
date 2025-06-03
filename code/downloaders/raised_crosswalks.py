# raised_crosswalks.py
from nyc_base_downloader import NYCDataDownloader

class NYCRaisedCrosswalksDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/resource/uh2s-ftgh.csv"
    DATASET_NAME = "DOT Raised Crosswalk Locations"

def main():
    downloader = NYCRaisedCrosswalksDownloader()
    downloader.run()

if __name__ == "__main__":
    main()