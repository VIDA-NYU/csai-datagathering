from nyc_base_downloader import NYCDataDownloader

class NYCSpeedHumpsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/resource/jknp-skuy.csv"
    DATASET_NAME = "DOT Speed Humps"

def main():
    downloader = NYCSpeedHumpsDownloader()
    downloader.run()

if __name__ == "__main__":
    main()