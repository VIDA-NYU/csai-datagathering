"""
NYC DOT Raised Crosswalk Locations Data Downloader

Downloads the Raised Crosswalk Locations dataset as a CSV from NYC Open Data.
"""

import requests
import argparse
from typing import Optional


class NYCRaisedCrosswalksDownloader:
    BASE_URL = "https://data.cityofnewyork.us/resource/uh2s-ftgh.csv"

    def __init__(self, app_token: Optional[str] = None):
        self.session = requests.Session()
        if app_token:
            self.session.headers.update({'X-App-Token': app_token})

    def download_csv(self, output_path: str) -> None:
        """Download the CSV file and save it to disk"""
        print(f"📥 Requesting CSV data from: {self.BASE_URL}")
        try:
            response = self.session.get(self.BASE_URL, timeout=10)
            print(f"🔄 Status code: {response.status_code}")
            response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ CSV file successfully downloaded to: {output_path}")
        except requests.RequestException as e:
            print(f"❌ Failed to download CSV: {e}")


def main():
    parser = argparse.ArgumentParser(description="Download NYC Raised Crosswalk Locations CSV data")
    parser.add_argument("-o", "--output", required=True, help="Path to save the downloaded CSV file")
    parser.add_argument("--app-token", help="Optional Socrata API app token")

    args = parser.parse_args()
    downloader = NYCRaisedCrosswalksDownloader(app_token=args.app_token)
    downloader.download_csv(args.output)


if __name__ == "__main__":
    main()
