#!/usr/bin/env python3
"""
Quick start script for Dropbox Photo Person Finder.
Guides users through the complete process step by step.
"""

import os
import subprocess
import sys


def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"You have Python {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True


def check_directories():
    """Check and create necessary directories"""
    directories = ["reference_photos", "downloaded_photos", "matched_photos"]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}/")
        else:
            print(f"✅ Directory exists: {directory}/")

    return True


def setup_virtual_environment():
    """Set up virtual environment if needed"""
    venv_path = "venv"

    # Check if we're already in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Already in virtual environment")
        return True

    # Check if virtual environment exists
    if not os.path.exists(venv_path):
        print("🔧 Creating virtual environment...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", venv_path])
            print(f"✅ Virtual environment created: {venv_path}/")
        except subprocess.CalledProcessError:
            print("❌ Failed to create virtual environment")
            return False
    else:
        print(f"✅ Virtual environment exists: {venv_path}/")

    print("\n📋 To activate the virtual environment, run:")
    print("   source venv/bin/activate  # macOS/Linux")
    print("   venv\\Scripts\\activate     # Windows")
    print()
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'face_recognition',
        'opencv-python',
        'Pillow',
        'numpy',
        'requests',
        'selenium',
        'tqdm'
    ]

    missing = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_').replace('opencv_python', 'cv2'))
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")

    if missing:
        print(f"\n📦 Missing packages: {', '.join(missing)}")

        # Check if in virtual environment
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

        if not in_venv:
            print("\n⚠️  You're not in a virtual environment!")
            print("For Python 3.8+ systems, you need to:")
            print("1. source venv/bin/activate")
            print("2. pip install face_recognition opencv-python Pillow numpy requests selenium tqdm")
            print("3. Run this script again")
            return False

        print("Attempting to install packages...")
        try:
            # Install without version pinning for better compatibility
            subprocess.check_call([sys.executable, "-m", "pip", "install"] +
                                [pkg.split('==')[0] for pkg in missing])
            print("✅ All packages installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            print("\n🔧 Manual installation:")
            print("pip install face_recognition opencv-python Pillow numpy requests selenium tqdm")
            return False

    return True


def check_reference_photos():
    """Check if reference photos are available"""
    ref_dir = "reference_photos"

    if not os.path.exists(ref_dir):
        return False

    image_files = [f for f in os.listdir(ref_dir)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    if not image_files:
        return False

    print(f"✅ Found {len(image_files)} reference photos")
    return True


def main():
    print("🚀 Dropbox Photo Person Finder - Quick Start")
    print("=" * 50)
    print()

    # Step 1: Check Python
    print("Step 1: Checking Python version...")
    if not check_python_version():
        return False
    print()

    # Step 2: Set up virtual environment
    print("Step 2: Setting up virtual environment...")
    if not setup_virtual_environment():
        return False
    print()

    # Step 3: Create directories
    print("Step 3: Setting up directories...")
    check_directories()
    print()

    # Step 4: Check dependencies
    print("Step 4: Checking Python packages...")
    if not check_dependencies():
        return False
    print()

    # Step 5: Check reference photos
    print("Step 5: Checking reference photos...")
    if not check_reference_photos():
        print("❌ No reference photos found!")
        print()
        print("📋 NEXT STEPS:")
        print("1. Activate virtual environment: source venv/bin/activate")
        print("2. Add 3-5 photos of the target person to the 'reference_photos/' directory")
        print("3. Read the guide: REFERENCE_PHOTOS_GUIDE.md")
        print("4. Test your photos: python test_references.py")
        print("5. Run the main script: python find_person_photos.py")
        return False
    print()

    # Step 6: Test reference photos
    print("Step 6: Testing reference photos...")
    try:
        subprocess.run([sys.executable, "test_references.py"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Could not test reference photos automatically.")
        print("Please run manually: python test_references.py")
    print()

    # All good - ready to go!
    print("🎉 SETUP COMPLETE!")
    print("=" * 50)
    print()
    print("Your system is ready to find photos containing the target person.")
    print()
    print("📋 WHAT'S NEXT:")
    print()
    print("IMPORTANT: Activate the virtual environment first:")
    print("   source venv/bin/activate")
    print()
    print("Option 1 - Standard processing:")
    print("   python find_person_photos.py")
    print()
    print("Option 2 - Extra-safe processing (slower, but avoids IP bans):")
    print("   python safe_download.py")
    print()
    print("Option 3 - Manual download (if automatic doesn't work):")
    print("   1. Manually download photos from Dropbox to 'downloaded_photos/'")
    print("   2. Run: python manual_process.py")
    print()
    print("📖 For detailed help, read: README.md")
    print("🖼️  For photo tips, read: REFERENCE_PHOTOS_GUIDE.md")

    return True


if __name__ == "__main__":
    success = main()

    if not success:
        print("\n❌ Setup incomplete. Please address the issues above.")
        sys.exit(1)
    else:
        print("\n✅ Ready to go! Choose one of the processing options above.")
        sys.exit(0)