#!/usr/bin/env python3
"""
Setup script for the Dropbox Photo Person Finder
"""

import subprocess
import sys
import os


def install_dependencies():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    directories = [
        "reference_photos",
        "downloaded_photos",
        "matched_photos"
    ]

    print("Creating directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}/")


def check_system_requirements():
    """Check if system requirements are met"""
    print("Checking system requirements...")

    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

    # Check if cmake is available (required for face_recognition)
    try:
        subprocess.check_output(["cmake", "--version"], stderr=subprocess.DEVNULL)
        print("✅ CMake found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  CMake not found. Install it with: brew install cmake (macOS)")

    return True


def main():
    print("🔧 Setting up Dropbox Photo Person Finder")
    print("=" * 50)

    # Check requirements
    if not check_system_requirements():
        return False

    # Create directories
    create_directories()

    # Install dependencies
    if not install_dependencies():
        return False

    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Add reference photos to 'reference_photos/' directory")
    print("2. Run: python find_person_photos.py")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)