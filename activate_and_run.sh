#!/bin/bash
# Simple activation script for the Dropbox Photo Person Finder

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "✅ Virtual environment activated!"
echo ""
echo "📋 Available commands:"
echo "  python quickstart.py          - Setup and check everything"
echo "  python test_references.py     - Test your reference photos"
echo "  python find_person_photos.py  - Find photos (standard)"
echo "  python safe_download.py       - Find photos (extra-safe)"
echo "  python manual_process.py      - Process manually downloaded photos"
echo ""
echo "🎯 Quick start: Add photos to 'reference_photos/' then run:"
echo "   python find_person_photos.py"
echo ""
echo "Type 'deactivate' to exit the virtual environment"

# Keep the shell open in the virtual environment
exec $SHELL