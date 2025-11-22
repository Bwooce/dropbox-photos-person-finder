# Dropbox Photo Person Finder

A Python tool that uses facial recognition to find all photos containing a specific person from a Dropbox shared folder. Uses advanced facial recognition with high accuracy and includes multiple approaches for photo acquisition.

## Features

- 🎯 **High-accuracy facial recognition** using state-of-the-art deep learning
- 📸 **Multiple reference photos** for improved matching accuracy
- 🛡️ **Privacy-focused** - processes photos locally, never uploads data
- 🔄 **Multiple acquisition methods** - automated and manual approaches
- 📊 **Quality validation** - tests reference photos before processing
- 💾 **Smart caching** - avoids re-downloading or re-processing files

## Requirements

- Python 3.7 or higher
- CMake (for building face_recognition)
- Chrome browser (for web scraping)

### Installation

1. **Install system dependencies:**
   ```bash
   # macOS
   brew install cmake

   # Ubuntu/Debian
   sudo apt-get install cmake

   # Windows
   # Install Visual Studio Build Tools and CMake from official websites
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

   Or manually:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Prepare Reference Photos

Create a `reference_photos` directory and add 3-5 clear photos of the person you want to find:

```bash
reference_photos/
├── person_photo1.jpg
├── person_photo2.jpg
├── person_photo3.jpg
├── person_photo4.jpg
└── person_photo5.jpg
```

**📖 Read the complete guide:** [REFERENCE_PHOTOS_GUIDE.md](REFERENCE_PHOTOS_GUIDE.md)

**Quick tips for best results:**
- **3-5 photos recommended** (minimum 2, maximum 8)
- **High resolution:** Face should be at least 300x300 pixels
- **Good lighting:** Natural daylight preferred
- **Clear face view:** Front-facing or slight angles
- **Different angles/expressions:** Variety improves accuracy
- **No obstructions:** Avoid sunglasses, masks, or hair covering face

**Test your photos:**
```bash
python test_references.py
```
This will verify your reference photos are good quality before processing.

### 2. Choose Your Approach

#### 🎯 **Recommended: Manual Download** (Most Reliable)
```bash
# 1. Download photos from Dropbox manually (see guide below)
# 2. Process downloaded photos
python manual_process.py
```

#### 🤖 **Alternative: Automated Download** (May have reliability issues)
```bash
# Standard automated approach
python find_person_photos.py

# Extra-safe automated approach (slower, maximum IP protection)
python safe_download.py
```

### 3. Manual Download Process (Recommended)

**Step A: Download from Dropbox**
1. Open your Dropbox link in a web browser
2. Click "Download all" or select photos and click "Download"
3. Extract downloaded files to the `downloaded_photos/` directory

**Step B: Process Photos**
```bash
python manual_process.py
```

**Why Manual Download?**
- ✅ 100% reliable (no web scraping failures)
- ✅ Faster than automated approaches
- ✅ No risk of IP limitations
- ✅ Works with any Dropbox folder structure

### 4. Results

Check the `matched_photos/` directory for all photos containing the target person.

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Setup
python quickstart.py

# 2. Add 3-5 reference photos to reference_photos/ directory

# 3. Download photos from Dropbox to downloaded_photos/ directory

# 4. Find matches
source venv/bin/activate
python manual_process.py

# 5. Check results in matched_photos/ directory
```

## Directory Structure

```
dropbox_photos_person/
├── find_person_photos.py      # Main script
├── setup.py                   # Setup script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── reference_photos/          # Add reference photos here
├── downloaded_photos/         # Downloaded photos (temporary)
└── matched_photos/           # Results go here
```

## Configuration

### Adjusting Face Recognition Sensitivity

Edit `find_person_photos.py` and modify the tolerance value (line ~200):

```python
matches = face_recognition.compare_faces(
    self.reference_encodings,
    face_encoding,
    tolerance=0.6  # Lower = stricter matching
)
```

- **0.4**: Very strict (fewer false positives, may miss some matches)
- **0.6**: Balanced (recommended)
- **0.8**: Permissive (more matches, possible false positives)

### Alternative: Manual Photo Download

If automatic Dropbox download doesn't work:

1. Manually download photos to `downloaded_photos/` directory
2. Run the script - it will skip the download step and process existing files

## Troubleshooting

### Common Issues

**"No faces found in reference photos"**
- Ensure reference photos clearly show the person's face
- Try different reference photos with better lighting
- Make sure photos are in supported formats (.jpg, .png, .gif)

**"CMake not found"**
```bash
# macOS
brew install cmake

# Ubuntu/Debian
sudo apt-get install cmake build-essential

# Windows
# Install Visual Studio Build Tools
```

**"Chrome driver issues"**
- The script will automatically download ChromeDriver
- Ensure Chrome browser is installed
- Check your internet connection

**"Dropbox automated download failed"**
- ✅ **Solution: Use manual download method** (recommended)
- Automated web scraping can be unreliable with modern Dropbox interfaces
- Manual download is faster and 100% reliable

### Performance Tips

- Reduce image resolution for faster processing (images are resized automatically)
- Process fewer photos at a time by organizing them in batches
- Use an SSD for faster file I/O

## Privacy and Ethics

- Only use this tool on photos you have permission to access
- Respect privacy and consent of individuals in photos
- Consider applicable laws and regulations in your jurisdiction
- This tool is for legitimate personal/professional use only

## Technical Details

### Libraries Used

- **face_recognition**: Facial recognition using dlib
- **opencv-python**: Image processing
- **selenium**: Web automation for Dropbox access
- **requests**: HTTP requests for downloading
- **Pillow**: Image file handling

### Algorithm

1. **Reference Encoding**: Extract facial features from reference photos using deep learning
2. **Face Detection**: Find all faces in downloaded photos
3. **Face Comparison**: Calculate similarity between reference and found faces
4. **Filtering**: Select photos with similarity above threshold

## License

This project is for educational and personal use. Ensure compliance with applicable laws and terms of service.