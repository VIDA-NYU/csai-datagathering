# nyc_311.py
"""
NYC 311 Data Downloader

Downloads the NYC 311 Service Requests dataset as a CSV from NYC Open Data.
"""

from nyc_base_downloader import NYCDataDownloader

class NYC311DataDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/resource/jrb2-thup.csv"
    DATASET_NAME = "311 Service Requests"

def main():
    downloader = NYC311DataDownloader()
    downloader.run()

if __name__ == "__main__":
    main()