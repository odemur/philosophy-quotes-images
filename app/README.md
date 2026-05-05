# Philosophy Watermark Application

## Description
Python script to apply logo watermarks to philosopher images.

## Directory Structure
```
philosophy/
├── app/                    # Application code
│   ├── watermark_images.py # Main watermark script
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # This file
├── config/                 # Configuration files
│   └── logo.png           # Logo watermark image
├── images/                 # Image directories
│   ├── source/            # Original images (input)
│   └── public/            # Watermarked images (output)
└── docs/                  # Documentation
```

## Usage
1. Navigate to the app directory:
   ```bash
   cd app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the watermark script:
   ```bash
   python3 watermark_images.py
   ```

## Configuration
Edit the variables in `watermark_images.py`:
- `LOGO_MAX_WIDTH`: Maximum logo width (default: 360px)
- `LOGO_BOTTOM_OFFSET`: Distance from bottom edge (default: 128px)
- `LOGO_PATH`: Path to logo file
- `SOURCE_DIR`: Input directory for original images
- `OUTPUT_DIR`: Output directory for watermarked images

## Features
- Proportional logo resizing maintaining aspect ratio
- Centered horizontal positioning
- Configurable distance from bottom edge
- Support for multiple image formats (PNG, JPG, etc.)
- Automatic output directory creation
