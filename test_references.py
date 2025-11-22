#!/usr/bin/env python3
"""
Test script to verify reference photos are good quality for facial recognition.
Run this before processing your full photo collection.
"""

import os
import face_recognition
from PIL import Image
import numpy as np


def test_reference_photos(reference_dir="reference_photos"):
    """Test all reference photos for face detection quality"""
    print("Testing Reference Photos")
    print("=" * 30)

    if not os.path.exists(reference_dir):
        print(f"❌ Reference directory '{reference_dir}' not found!")
        print("Create the directory and add photos of the target person.")
        return False

    # Get all image files
    image_files = [f for f in os.listdir(reference_dir)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    if not image_files:
        print(f"❌ No image files found in '{reference_dir}'!")
        return False

    print(f"Found {len(image_files)} reference photos to test:")
    print()

    good_photos = []
    all_encodings = []

    for filename in image_files:
        filepath = os.path.join(reference_dir, filename)
        print(f"📷 Testing: {filename}")

        try:
            # Load image
            image = face_recognition.load_image_file(filepath)
            height, width = image.shape[:2]

            # Check basic image properties
            print(f"   Resolution: {width}x{height} pixels")

            # Check if too small
            if width < 200 or height < 200:
                print("   ⚠️  Image resolution is quite small")

            # Find faces
            face_locations = face_recognition.face_locations(image)
            print(f"   Faces detected: {len(face_locations)}")

            if len(face_locations) == 0:
                print("   ❌ No faces found!")
                continue
            elif len(face_locations) > 1:
                print("   ⚠️  Multiple faces detected - will use largest")

            # Get face encodings
            face_encodings = face_recognition.face_encodings(image, face_locations)

            if not face_encodings:
                print("   ❌ Could not encode faces!")
                continue

            # Check face size in image
            for i, face_location in enumerate(face_locations):
                top, right, bottom, left = face_location
                face_width = right - left
                face_height = bottom - top
                face_area_ratio = (face_width * face_height) / (width * height)

                print(f"   Face {i+1}: {face_width}x{face_height} pixels ({face_area_ratio:.1%} of image)")

                if face_area_ratio < 0.05:  # Face is less than 5% of image
                    print("   ⚠️  Face is quite small in the image")
                elif face_area_ratio > 0.4:  # Face is more than 40% of image
                    print("   ✅ Good face size")
                else:
                    print("   ✅ Acceptable face size")

            # Store encoding for diversity check
            all_encodings.extend(face_encodings)
            good_photos.append(filename)
            print("   ✅ Photo is usable!")

        except Exception as e:
            print(f"   ❌ Error processing: {e}")

        print()

    # Summary and recommendations
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)

    if len(good_photos) == 0:
        print("❌ No usable reference photos found!")
        print("\nRecommendations:")
        print("- Add photos with clear, visible faces")
        print("- Ensure good lighting and focus")
        print("- Use higher resolution images")
        return False

    print(f"✅ {len(good_photos)} usable reference photos:")
    for photo in good_photos:
        print(f"   • {photo}")

    # Quality assessment
    if len(good_photos) >= 5:
        quality = "Excellent"
        color = "✅"
    elif len(good_photos) >= 3:
        quality = "Good"
        color = "✅"
    elif len(good_photos) >= 2:
        quality = "Fair"
        color = "⚠️ "
    else:
        quality = "Poor"
        color = "❌"

    print(f"\n{color} Photo set quality: {quality}")

    # Check encoding diversity
    if len(all_encodings) >= 2:
        print("\n🔍 Checking photo diversity...")
        distances = []
        for i in range(len(all_encodings)):
            for j in range(i+1, len(all_encodings)):
                distance = face_recognition.face_distance([all_encodings[i]], all_encodings[j])[0]
                distances.append(distance)

        if distances:
            avg_distance = np.mean(distances)
            print(f"   Average face distance: {avg_distance:.3f}")

            if avg_distance < 0.3:
                print("   ⚠️  Photos are very similar - consider adding more diverse angles/lighting")
            elif avg_distance > 0.7:
                print("   ⚠️  Photos are quite different - verify they're all the same person")
            else:
                print("   ✅ Good diversity in reference photos")

    # Recommendations
    print("\n📋 RECOMMENDATIONS:")

    if len(good_photos) < 3:
        print("• Add more reference photos (aim for 3-5 total)")

    print("• Ensure photos have:")
    print("  - Clear face visibility")
    print("  - Good lighting (natural light preferred)")
    print("  - Different angles/expressions")
    print("  - Face takes up 10-40% of image")

    if len(good_photos) >= 2:
        print(f"\n🎯 Your reference photos should work!")
        print("You can proceed with running the main photo matching script.")
    else:
        print(f"\n⚠️  Consider adding more reference photos for better results.")

    return len(good_photos) >= 2


if __name__ == "__main__":
    success = test_reference_photos()
    if success:
        print("\n✅ Ready to run photo matching!")
    else:
        print("\n❌ Please improve reference photos before proceeding.")