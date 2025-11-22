#!/usr/bin/env python3
"""
Alternative script for when manual download is needed.
Run this if the automated Dropbox download doesn't work.
"""

import os
import face_recognition
import shutil
from tqdm import tqdm


def process_manual_photos():
    """Process manually downloaded photos"""
    reference_dir = "reference_photos"
    download_dir = "downloaded_photos"
    results_dir = "matched_photos"

    # Create directories
    os.makedirs(results_dir, exist_ok=True)

    print("Manual Photo Processing")
    print("======================")
    print()

    # Check for reference photos
    if not os.path.exists(reference_dir):
        print(f"❌ No reference photos directory found: {reference_dir}")
        print("Please create this directory and add photos of the target person.")
        return False

    reference_files = [f for f in os.listdir(reference_dir)
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    if not reference_files:
        print(f"❌ No reference photos found in {reference_dir}")
        return False

    # Check for downloaded photos
    if not os.path.exists(download_dir):
        print(f"❌ No downloaded photos directory found: {download_dir}")
        print("Please create this directory and manually download photos from Dropbox.")
        print("Steps:")
        print("1. Open the Dropbox link in your browser")
        print("2. Download individual photos or select all and download as zip")
        print("3. Extract photos to the 'downloaded_photos' directory")
        return False

    download_files = [f for f in os.listdir(download_dir)
                     if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    if not download_files:
        print(f"❌ No photos found in {download_dir}")
        print("Please download photos from Dropbox and place them in this directory.")
        return False

    print(f"✅ Found {len(reference_files)} reference photos")
    print(f"✅ Found {len(download_files)} photos to process")
    print()

    # Load reference encodings
    print("Loading reference photos...")
    reference_encodings = []

    for filename in reference_files:
        try:
            image_path = os.path.join(reference_dir, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                reference_encodings.extend(encodings)
                print(f"  ✅ {filename}: {len(encodings)} face(s)")
            else:
                print(f"  ⚠️  {filename}: No faces detected")

        except Exception as e:
            print(f"  ❌ {filename}: Error - {e}")

    if not reference_encodings:
        print("❌ No valid reference faces found!")
        return False

    print(f"📊 Total reference encodings: {len(reference_encodings)}")
    print()

    # Process downloaded photos
    matching_photos = []
    print("Analyzing downloaded photos...")

    for filename in tqdm(download_files, desc="Processing"):
        try:
            image_path = os.path.join(download_dir, filename)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)

            # Compare each face against reference faces
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    reference_encodings,
                    face_encoding,
                    tolerance=0.6
                )

                if any(matches):
                    matching_photos.append(filename)
                    break  # Found a match, no need to check other faces

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Copy matching photos
    if matching_photos:
        print(f"\n✅ Found {len(matching_photos)} matching photos!")
        print("Copying to results directory...")

        for filename in matching_photos:
            src_path = os.path.join(download_dir, filename)
            dst_path = os.path.join(results_dir, filename)
            shutil.copy2(src_path, dst_path)
            print(f"  📷 {filename}")

        print(f"\n🎉 Results saved to: {results_dir}")

    else:
        print("\n❌ No matching photos found.")
        print("\nTips:")
        print("- Check if reference photos clearly show the person's face")
        print("- Try adjusting tolerance in the script (currently 0.6)")
        print("- Ensure downloaded photos contain the target person")

    return True


if __name__ == "__main__":
    success = process_manual_photos()

    if success:
        print("\n📋 Summary:")
        print("- Reference photos are in 'reference_photos/'")
        print("- Downloaded photos are in 'downloaded_photos/'")
        print("- Matching photos are in 'matched_photos/'")
    else:
        print("\n🔧 Setup Help:")
        print("1. mkdir reference_photos downloaded_photos")
        print("2. Add photos of the target person to 'reference_photos/'")
        print("3. Download Dropbox photos to 'downloaded_photos/'")
        print("4. Run this script again")