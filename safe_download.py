#!/usr/bin/env python3
"""
Safe download script with aggressive rate limiting and caching to avoid IP bans.
Use this script if you're concerned about being blocked by Dropbox.
"""

import os
import time
import json
import hashlib
import requests
from urllib.parse import urlparse
import random
from tqdm import tqdm


class SafeDropboxDownloader:
    def __init__(self, config_file="config.json"):
        self.load_config(config_file)
        self.session = self.create_session()
        self.cache_dir = "download_cache"
        os.makedirs(self.cache_dir, exist_ok=True)

    def load_config(self, config_file):
        """Load configuration settings"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            self.config = config
        except FileNotFoundError:
            print(f"Config file {config_file} not found, using defaults")
            self.config = {
                "download_settings": {
                    "delay_between_downloads": 5,  # More conservative
                    "rate_limit_retry_delay": 60,
                    "max_retries": 3,
                    "timeout_seconds": 30
                }
            }

    def create_session(self):
        """Create a requests session with random user agent"""
        session = requests.Session()

        # Rotate user agents to appear less bot-like
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        ]

        session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        return session

    def get_cache_path(self, url, filename):
        """Generate cache file path based on URL hash"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        cache_filename = f"{url_hash}_{filename}"
        return os.path.join(self.cache_dir, cache_filename)

    def is_cached(self, url, filename):
        """Check if file is already cached"""
        cache_path = self.get_cache_path(url, filename)
        return os.path.exists(cache_path) and os.path.getsize(cache_path) > 0

    def safe_download(self, url, filename, dest_dir):
        """Safely download a single file with extensive rate limiting"""
        cache_path = self.get_cache_path(url, filename)
        final_path = os.path.join(dest_dir, filename)

        # Check cache first
        if self.is_cached(url, filename):
            print(f"Using cached: {filename}")
            with open(cache_path, 'rb') as src, open(final_path, 'wb') as dst:
                dst.write(src.read())
            return final_path

        # Add random delay to appear more human-like
        delay = self.config["download_settings"]["delay_between_downloads"]
        time.sleep(delay + random.uniform(1, 3))

        max_retries = self.config["download_settings"]["max_retries"]
        retry_delay = self.config["download_settings"]["rate_limit_retry_delay"]

        for attempt in range(max_retries):
            try:
                print(f"Downloading: {filename} (attempt {attempt + 1})")

                response = self.session.get(
                    url,
                    stream=True,
                    timeout=self.config["download_settings"]["timeout_seconds"]
                )

                if response.status_code == 200:
                    # Save to cache first
                    with open(cache_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    # Copy to final destination
                    with open(cache_path, 'rb') as src, open(final_path, 'wb') as dst:
                        dst.write(src.read())

                    return final_path

                elif response.status_code == 429:
                    print(f"Rate limited! Waiting {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue

                elif response.status_code == 403:
                    print(f"Access forbidden for {filename}")
                    return None

                else:
                    print(f"HTTP {response.status_code} for {filename}")

            except requests.exceptions.RequestException as e:
                print(f"Network error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)

        print(f"Failed to download {filename} after {max_retries} attempts")
        return None

    def batch_download(self, url_list, dest_dir="downloaded_photos", batch_size=10):
        """Download files in small batches to reduce load"""
        os.makedirs(dest_dir, exist_ok=True)
        downloaded_files = []

        print(f"Downloading {len(url_list)} files in batches of {batch_size}")

        for i in range(0, len(url_list), batch_size):
            batch = url_list[i:i + batch_size]
            print(f"\nProcessing batch {i//batch_size + 1}/{(len(url_list) + batch_size - 1)//batch_size}")

            for url_info in tqdm(batch, desc="Batch progress"):
                result = self.safe_download(
                    url_info['url'],
                    url_info['name'],
                    dest_dir
                )
                if result:
                    downloaded_files.append(result)

            # Longer break between batches
            if i + batch_size < len(url_list):
                print("Waiting between batches...")
                time.sleep(30 + random.uniform(10, 20))

        return downloaded_files


def convert_dropbox_urls_for_download(base_url, filenames):
    """Convert Dropbox share URLs to direct download URLs"""
    urls = []

    # Method 1: Try to construct direct download URLs
    for filename in filenames:
        # Convert share URL to direct download
        direct_url = base_url.replace('?dl=0', f'/{filename}?dl=1')
        urls.append({
            'name': filename,
            'url': direct_url
        })

    return urls


def main():
    print("Safe Dropbox Downloader")
    print("=" * 30)
    print("This script uses aggressive rate limiting to avoid IP bans.")
    print()

    # Example usage
    dropbox_base_url = "https://www.dropbox.com/scl/fo/shu7f7a1zvog4bqjigkyw/ACOmDtVOz6ZSThifYdAwl-A?e=2&mc_cid=398e895742&rlkey=qa787n8g19ohkmui3fqex8mn1&st=5hx01ujz&dl=0"

    # You would need to manually get the list of filenames from the Dropbox folder
    # This is a placeholder - in reality you'd need to either:
    # 1. Manually list the files
    # 2. Use the web scraping approach (but more carefully)
    # 3. Ask the user to provide a list

    print("IMPORTANT: You need to manually provide the list of photo filenames.")
    print("Visit the Dropbox link and create a list of filenames to download.")
    print()
    print("Example:")
    print("photo_filenames = [")
    print("    'IMG_001.jpg',")
    print("    'IMG_002.jpg',")
    print("    'photo.png'")
    print("]")
    print()

    # Example implementation:
    photo_filenames = []  # User would populate this

    if not photo_filenames:
        print("Please edit this script and add the photo filenames you want to download.")
        return

    # Convert to download URLs
    url_list = convert_dropbox_urls_for_download(dropbox_base_url, photo_filenames)

    # Download safely
    downloader = SafeDropboxDownloader()
    downloaded_files = downloader.batch_download(url_list, batch_size=5)

    print(f"\nDownloaded {len(downloaded_files)} files successfully!")
    print("Files saved to 'downloaded_photos/' directory")


if __name__ == "__main__":
    main()