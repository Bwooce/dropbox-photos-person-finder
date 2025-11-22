#!/usr/bin/env python3
"""
Script to find all photos containing a specific person from a Dropbox folder.
Uses facial recognition to identify matching faces across photos.
"""

import os
import sys
import time
import requests
import face_recognition
import cv2
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm
import json
from urllib.parse import urlparse, parse_qs
import re
from bs4 import BeautifulSoup


class DropboxPhotoMatcher:
    def __init__(self, dropbox_url, reference_photos_dir="reference_photos", downloads_dir="downloaded_photos", results_dir="matched_photos"):
        self.dropbox_url = dropbox_url
        self.reference_photos_dir = reference_photos_dir
        self.downloads_dir = downloads_dir
        self.results_dir = results_dir
        self.reference_encodings = []
        self.driver = None

        # Create directories
        for dir_path in [self.reference_photos_dir, self.downloads_dir, self.results_dir]:
            os.makedirs(dir_path, exist_ok=True)

    def setup_webdriver(self):
        """Set up Chrome webdriver for Selenium"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            return True
        except Exception as e:
            print(f"Error setting up webdriver: {e}")
            return False

    def extract_dropbox_files(self):
        """Extract file URLs from Dropbox shared folder"""
        if not self.setup_webdriver():
            return []

        try:
            print("Loading Dropbox folder...")
            self.driver.get(self.dropbox_url)

            # Wait for page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Wait a bit more for dynamic content
            time.sleep(5)

            # Try different selectors to find file elements
            file_elements = []

            # Common Dropbox file selectors
            selectors = [
                '[data-testid*="file"]',
                '.browse-file-name',
                '[role="button"][aria-label*=".jpg"]',
                '[role="button"][aria-label*=".jpeg"]',
                '[role="button"][aria-label*=".png"]',
                'a[href*=".jpg"]',
                'a[href*=".jpeg"]',
                'a[href*=".png"]'
            ]

            for selector in selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    file_elements = elements
                    print(f"Found {len(elements)} elements with selector: {selector}")
                    break

            if not file_elements:
                # Fallback: search page source for image URLs
                page_source = self.driver.page_source
                self.driver.quit()
                return self.extract_urls_from_source(page_source)

            # Extract file information
            files = []
            for element in file_elements:
                try:
                    # Get file name
                    file_name = element.get_attribute('aria-label') or element.text

                    # Check if it's an image file
                    if any(ext in file_name.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
                        # Try to get download URL by clicking/inspecting element
                        element.click()
                        time.sleep(1)

                        # Look for download button or direct link
                        download_url = self.get_download_url_for_file(file_name)
                        if download_url:
                            files.append({
                                'name': file_name,
                                'url': download_url
                            })

                except Exception as e:
                    print(f"Error processing element: {e}")
                    continue

            self.driver.quit()
            return files

        except Exception as e:
            print(f"Error extracting files: {e}")
            if self.driver:
                self.driver.quit()
            return []

    def extract_urls_from_source(self, page_source):
        """Fallback method: extract image URLs from page source"""
        files = []

        # Look for common patterns in Dropbox page source
        patterns = [
            r'https://[^"]+\.dropboxusercontent\.com[^"]+\.(jpg|jpeg|png|gif)',
            r'https://[^"]+\.dropbox\.com[^"]+\.(jpg|jpeg|png|gif)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, page_source, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    url = match[0]
                else:
                    url = match

                files.append({
                    'name': os.path.basename(url).split('?')[0],
                    'url': url
                })

        return files

    def get_download_url_for_file(self, filename):
        """Convert Dropbox share URL to direct download URL"""
        # This is a simplified approach - modify the original URL
        try:
            # Replace dl=0 with dl=1 and append filename
            base_url = self.dropbox_url.replace('dl=0', 'dl=1')
            return f"{base_url}/{filename}"
        except:
            return None

    def download_photos(self, files):
        """Download photos from extracted URLs with caching and rate limiting"""
        print(f"Downloading {len(files)} photos...")
        downloaded_files = []

        # Session for connection reuse and better performance
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        for i, file_info in enumerate(tqdm(files, desc="Downloading"), 1):
            try:
                file_path = os.path.join(self.downloads_dir, file_info['name'])

                # Check if file already exists (caching)
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    downloaded_files.append(file_path)
                    continue

                # Rate limiting: wait between downloads to avoid IP bans
                if i > 1:  # Don't wait before first download
                    time.sleep(2)  # 2 second delay between downloads

                response = session.get(file_info['url'], stream=True, timeout=30)

                if response.status_code == 200:
                    temp_path = file_path + '.tmp'  # Download to temp file first
                    with open(temp_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    # Move temp file to final location (atomic operation)
                    os.rename(temp_path, file_path)
                    downloaded_files.append(file_path)

                elif response.status_code == 429:  # Rate limited
                    print(f"Rate limited, waiting 30 seconds...")
                    time.sleep(30)
                    # Retry once
                    response = session.get(file_info['url'], stream=True, timeout=30)
                    if response.status_code == 200:
                        temp_path = file_path + '.tmp'
                        with open(temp_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        os.rename(temp_path, file_path)
                        downloaded_files.append(file_path)
                    else:
                        print(f"Still failed after retry: {file_info['name']}: {response.status_code}")
                else:
                    print(f"Failed to download {file_info['name']}: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Network error downloading {file_info['name']}: {e}")
                time.sleep(5)  # Wait before continuing
            except Exception as e:
                print(f"Error downloading {file_info['name']}: {e}")

        session.close()
        return downloaded_files

    def load_reference_photos(self):
        """Load and encode reference photos of the target person"""
        print("Loading reference photos...")
        self.reference_encodings = []

        if not os.path.exists(self.reference_photos_dir):
            print(f"Reference photos directory '{self.reference_photos_dir}' not found!")
            print("Please create this directory and add photos of the person you want to find.")
            return False

        reference_files = [f for f in os.listdir(self.reference_photos_dir)
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

        if not reference_files:
            print(f"No image files found in '{self.reference_photos_dir}'!")
            print("Please add photos of the person you want to find.")
            return False

        for filename in reference_files:
            try:
                image_path = os.path.join(self.reference_photos_dir, filename)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)

                if encodings:
                    self.reference_encodings.extend(encodings)
                    print(f"Loaded {len(encodings)} face(s) from {filename}")
                else:
                    print(f"No faces found in {filename}")

            except Exception as e:
                print(f"Error processing reference photo {filename}: {e}")

        print(f"Total reference encodings: {len(self.reference_encodings)}")
        return len(self.reference_encodings) > 0

    def find_matching_photos(self, photo_paths):
        """Find photos containing faces that match reference encodings"""
        matching_photos = []

        print("Analyzing photos for face matches...")
        for photo_path in tqdm(photo_paths, desc="Processing"):
            try:
                # Load image
                image = face_recognition.load_image_file(photo_path)

                # Find faces in the image
                face_encodings = face_recognition.face_encodings(image)

                # Compare each face against reference faces
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        self.reference_encodings,
                        face_encoding,
                        tolerance=0.6  # Adjust tolerance as needed
                    )

                    if any(matches):
                        matching_photos.append(photo_path)
                        print(f"Match found: {os.path.basename(photo_path)}")
                        break  # Found a match, no need to check other faces in this photo

            except Exception as e:
                print(f"Error processing {photo_path}: {e}")

        return matching_photos

    def copy_matching_photos(self, matching_photos):
        """Copy matching photos to results directory"""
        print(f"Copying {len(matching_photos)} matching photos to {self.results_dir}...")

        for photo_path in matching_photos:
            try:
                filename = os.path.basename(photo_path)
                dest_path = os.path.join(self.results_dir, filename)

                with open(photo_path, 'rb') as src, open(dest_path, 'wb') as dst:
                    dst.write(src.read())

            except Exception as e:
                print(f"Error copying {photo_path}: {e}")

    def run(self):
        """Main execution method"""
        print("=== Dropbox Photo Person Finder ===")
        print(f"Dropbox URL: {self.dropbox_url}")
        print()

        # Step 1: Load reference photos
        if not self.load_reference_photos():
            return False

        # Step 2: Extract file list from Dropbox
        files = self.extract_dropbox_files()
        if not files:
            print("No photos found in Dropbox folder or couldn't access the folder.")
            print("\nAlternative: You can manually download photos to the 'downloaded_photos' directory")
            print("and run the script again to skip the download step.")

            # Check if manual download exists
            manual_files = [os.path.join(self.downloads_dir, f)
                           for f in os.listdir(self.downloads_dir)
                           if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

            if manual_files:
                print(f"Found {len(manual_files)} manually downloaded photos. Processing...")
                files = manual_files
            else:
                return False
        else:
            # Step 3: Download photos
            downloaded_files = self.download_photos(files)
            files = downloaded_files

        # Step 4: Find matching photos
        matching_photos = self.find_matching_photos(files)

        # Step 5: Copy results
        if matching_photos:
            self.copy_matching_photos(matching_photos)
            print(f"\n✅ Found {len(matching_photos)} photos containing the target person!")
            print(f"Results saved to: {self.results_dir}")
        else:
            print("\n❌ No matching photos found.")

        return True


def main():
    # Dropbox URL from user
    dropbox_url = "https://www.dropbox.com/scl/fo/shu7f7a1zvog4bqjigkyw/ACOmDtVOz6ZSThifYdAwl-A?e=2&mc_cid=398e895742&rlkey=qa787n8g19ohkmui3fqex8mn1&st=5hx01ujz&dl=0"

    print("Dropbox Photo Person Finder")
    print("===========================")
    print()
    print("Setup Instructions:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Add reference photos of the target person to 'reference_photos/' directory")
    print("3. Run this script")
    print()

    # Create matcher instance
    matcher = DropboxPhotoMatcher(dropbox_url)

    # Run the process
    success = matcher.run()

    if not success:
        print("\nTroubleshooting:")
        print("- Ensure you have reference photos in 'reference_photos/' directory")
        print("- Check your internet connection")
        print("- Try manually downloading some photos to 'downloaded_photos/' directory")


if __name__ == "__main__":
    main()