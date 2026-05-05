# Philosophy Repository

A repository for philosophical studies and materials with watermark application.

## Structure

- `app/`: Python application for image watermarking
- `config/`: Configuration files (logo, settings)
- `images/`: Image directories
  - `source/`: Original philosopher images (input)
  - `public/`: Watermarked images (output)
- `philosophy-of-mind/`: Resources and materials related to philosophy of mind
- `docs/`: Documentation

## Quick Start

1. Install dependencies:
   ```bash
   cd app && pip install -r requirements.txt
   ```

2. Run watermark application:
   ```bash
   cd app && python3 watermark_images.py
   ```

## Features

- Automatic watermark application to philosopher images
- Proportional logo resizing maintaining aspect ratio
- Configurable positioning (currently 128px from bottom, centered)
- Support for multiple image formats
- Organized source/public directory structure
