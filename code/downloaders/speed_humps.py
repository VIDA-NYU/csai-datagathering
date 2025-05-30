"""
NYC DOT Speed Humps Data Downloader

Downloads the Speed Humps dataset as a CSV from NYC Open Data.
"""

import requests
import pandas as pd
import argparse
from typing import Optional


class NYCSpeedHumpsDownloader:
    BASE_URL = "https://data.cityofnewyork.us/resource/jknp-skuy.csv"

    def __init__(self, app_token: Optional[str] = None):
        self.session = requests.Session()
        if app_token:
            self.session.headers.update({'X-App-Token': app_token})

    def download_csv(self, output_path: str) -> None:
        """Download the CSV file and save to disk"""
        print(f"📥 Requesting CSV data from: {self.BASE_URL}")
        try:
            response = self.session.get(self.BASE_URL)
            print(f"🔄 Status code: {response.status_code}")
            response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ CSV file successfully downloaded to: {output_path}")
        except requests.RequestException as e:
            print(f"❌ Failed to download CSV: {e}")



def main():
    parser = argparse.ArgumentParser(description="Download NYC DOT Speed Humps CSV data")
    parser.add_argument("-o", "--output", required=True, help="Path to save the downloaded CSV file")
    parser.add_argument("--app-token", help="Optional Socrata API app token")

    args = parser.parse_args()
    downloader = NYCSpeedHumpsDownloader(app_token=args.app_token)
    downloader.download_csv(args.output)


if __name__ == "__main__":
    main()
