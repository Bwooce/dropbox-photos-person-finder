# Project Overview: Dropbox Photo Person Finder

A complete solution to find all photos containing a specific person from a Dropbox shared folder using facial recognition.

## 📁 Project Files

### 🚀 Getting Started
- **`quickstart.py`** - Run this first! Guides you through setup
- **`README.md`** - Complete documentation and instructions

### 🔧 Setup & Installation
- **`setup.py`** - Automated dependency installation
- **`requirements.txt`** - Python package dependencies
- **`config.json`** - Configuration settings for downloads and recognition

### 📷 Photo Processing Scripts

#### Main Scripts
- **`find_person_photos.py`** - Main script with automatic Dropbox download
- **`safe_download.py`** - Extra-safe version with aggressive rate limiting
- **`manual_process.py`** - For when you manually download photos first

#### Testing & Validation
- **`test_references.py`** - Test reference photo quality before processing

### 📚 Documentation
- **`REFERENCE_PHOTOS_GUIDE.md`** - Comprehensive guide for choosing reference photos
- **`PROJECT_OVERVIEW.md`** - This file - project structure overview

### 📂 Directories (Created Automatically)
- **`reference_photos/`** - Put 3-5 photos of target person here
- **`downloaded_photos/`** - Temporary storage for Dropbox photos
- **`matched_photos/`** - Results - photos containing the target person
- **`download_cache/`** - Cache to avoid re-downloading files

## 🔄 Workflow Options

### Option 1: Fully Automated (Recommended)
```bash
python quickstart.py        # Setup and check everything
python find_person_photos.py # Process with built-in rate limiting
```

### Option 2: Extra-Safe Automated
```bash
python quickstart.py        # Setup and check everything
python safe_download.py     # Very conservative downloading
```

### Option 3: Manual Download
```bash
python quickstart.py        # Setup and check everything
# Manually download photos from Dropbox to downloaded_photos/
python manual_process.py    # Process manually downloaded photos
```

## 🎯 Quick Start (30 seconds)

1. **Run setup:**
   ```bash
   python quickstart.py
   ```

2. **Add reference photos:**
   - Put 3-5 clear photos of the target person in `reference_photos/`
   - Read `REFERENCE_PHOTOS_GUIDE.md` for best practices

3. **Test reference photos:**
   ```bash
   python test_references.py
   ```

4. **Find matching photos:**
   ```bash
   python find_person_photos.py
   ```

5. **Check results:**
   - Look in `matched_photos/` directory

## 🛡️ IP Protection Features

All scripts include protection against IP bans:
- **Rate limiting** (2-5 second delays between downloads)
- **Caching** (won't re-download existing files)
- **Retry logic** with exponential backoff
- **Realistic browser headers** to avoid detection
- **Batch processing** with breaks between batches

## 📊 Expected Results

### With Good Reference Photos (3-5 clear photos):
- **Accuracy:** 85-95% for finding matching faces
- **Speed:** 1-3 seconds per photo for facial recognition
- **Download speed:** Limited by rate limiting (2-5 seconds per photo)

### With Fair Reference Photos (2-3 average photos):
- **Accuracy:** 60-75%
- Some matches may be missed

## 🔧 Customization

### Adjust Face Recognition Sensitivity
Edit tolerance in any script (lower = stricter):
```python
matches = face_recognition.compare_faces(
    reference_encodings,
    face_encoding,
    tolerance=0.6  # 0.4=strict, 0.6=balanced, 0.8=permissive
)
```

### Adjust Download Rate Limiting
Edit `config.json`:
```json
{
  "download_settings": {
    "delay_between_downloads": 5,  // seconds between downloads
    "rate_limit_retry_delay": 60   // seconds to wait if rate limited
  }
}
```

## 🚨 Important Notes

### Privacy & Ethics
- Only use on photos you have permission to access
- Respect privacy and consent of individuals
- Consider applicable laws and regulations

### Technical Limitations
- Requires clear face visibility in both reference and target photos
- Performance depends on reference photo quality
- May have false positives/negatives with similar-looking people
- Dropbox may change their interface, affecting automatic download

### Troubleshooting
If automatic download fails:
1. Try the `safe_download.py` approach
2. Use manual download method
3. Check Dropbox link is public and accessible
4. Verify internet connection

## 📞 Support

- Check `README.md` for detailed troubleshooting
- Reference photos not working? Read `REFERENCE_PHOTOS_GUIDE.md`
- Run `python test_references.py` to validate your setup

## 🎉 Success!

When everything works, you'll have:
- All photos containing the target person in `matched_photos/`
- Original photos preserved in `downloaded_photos/`
- Cache of downloads to avoid future re-downloading
- Clear logs showing what was found and processed