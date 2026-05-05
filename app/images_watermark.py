#!/usr/bin/env python3
"""
Script to apply logo watermark to all images in the source directory.
The logo will be positioned using configurable offsets from bottom edge, centered horizontally.
"""

import os
from PIL import Image

# Configuration
LOGO_PATH = "../config/logo.png"
SOURCE_DIR = "../images/source"
OUTPUT_DIR = "../images/public"

# Positioning configuration
# Logo positioned at 16px from bottom, centered horizontally
LOGO_MAX_WIDTH = 360  # Maximum logo width in pixels (proportional resizing)
LOGO_BOTTOM_OFFSET = 16  # Distance from bottom edge in pixels

def apply_watermark(image_path, logo_path, output_path, logo_max_width=360, bottom_offset=16):
    """Apply logo watermark to an image at bottom center with configurable offset."""
    try:
        # Open the base image
        with Image.open(image_path) as base_image:
            # Convert to RGBA if not already
            if base_image.mode != 'RGBA':
                base_image = base_image.convert('RGBA')
            
            # Open the logo
            with Image.open(logo_path) as logo:
                # Convert logo to RGBA if not already
                if logo.mode != 'RGBA':
                    logo = logo.convert('RGBA')
                
                # Resize logo proportionally to maintain aspect ratio
                original_width, original_height = logo.size
                aspect_ratio = original_width / original_height
                new_width = logo_max_width
                new_height = int(new_width / aspect_ratio)
                logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Calculate position (centered horizontally, 128px from bottom)
                base_width, base_height = base_image.size
                logo_width, logo_height = logo.size
                
                # Center horizontally
                x = (base_width - logo_width) // 2
                
                # Position at 128px from bottom
                y = base_height - bottom_offset - logo_height
                
                # Ensure logo doesn't go outside image bounds
                x = max(0, min(x, base_width - logo_width))
                y = max(0, min(y, base_height - logo_height))
                
                # Create a copy of the base image
                watermarked = base_image.copy()
                
                # Paste the logo onto the base image
                watermarked.paste(logo, (x, y), logo)
                
                # Save the watermarked image
                if output_path.lower().endswith(('.jpg', '.jpeg')):
                    # Convert back to RGB for JPEG files (remove transparency)
                    rgb_image = Image.new('RGB', watermarked.size, (255, 255, 255))
                    rgb_image.paste(watermarked, mask=watermarked.split()[-1])
                    rgb_image.save(output_path, quality=95)
                else:
                    watermarked.save(output_path, quality=95)
                print(f"✓ Watermarked: {os.path.basename(image_path)} -> {os.path.basename(output_path)}")
                return True
                
    except Exception as e:
        print(f"✗ Error processing {image_path}: {str(e)}")
        return False

def main():
    """Main function to process all images."""
    print("Starting watermark application...")
    print(f"Logo: {LOGO_PATH}")
    print(f"Source directory: {SOURCE_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Logo position: {LOGO_BOTTOM_OFFSET}px from bottom, centered")
    print("-" * 50)
    
    # Check if logo exists
    if not os.path.exists(LOGO_PATH):
        print(f"Error: Logo file '{LOGO_PATH}' not found!")
        return
    
    # Check if source directory exists
    if not os.path.exists(SOURCE_DIR):
        print(f"Error: Source directory '{SOURCE_DIR}' not found!")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Supported image extensions
    supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    
    # Check if source directory has images
    image_files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(supported_extensions)]
    if not image_files:
        print(f"No supported images found in '{SOURCE_DIR}'")
        return
    
    print(f"Found {len(image_files)} images to process")
    
    # Process all images in the images directory
    processed_count = 0
    error_count = 0
    
    for filename in os.listdir(SOURCE_DIR):
        if filename.lower().endswith(supported_extensions):
            input_path = os.path.join(SOURCE_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename)
            
            if apply_watermark(input_path, LOGO_PATH, output_path, LOGO_MAX_WIDTH, LOGO_BOTTOM_OFFSET):
                processed_count += 1
            else:
                error_count += 1
    
    print("-" * 50)
    print(f"Processing complete!")
    print(f"Successfully processed: {processed_count} images")
    print(f"Errors: {error_count} images")
    print(f"Watermarked images saved to: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
