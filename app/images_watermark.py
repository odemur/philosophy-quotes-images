#!/usr/bin/env python3
"""
Script to apply logo watermark to all images in the source directory.
Handles multiple image formats (posts and stories) with different dimensions.
The logo will be positioned using configurable offsets from bottom edge, centered horizontally.
"""

import os
from PIL import Image

# Configuration
LOGO_PATH = "../config/logo.png"
SOURCE_BASE_DIR = "../images/source"
OUTPUT_BASE_DIR = "../images/public"

# Image format configurations
FORMAT_CONFIGS = {
    'posts': {
        'logo_max_width': 360,  # Logo width for posts (1080x1350)
        'bottom_offset': 0,    # Distance from bottom edge
        'expected_size': (1080, 1350)
    },
    'stories': {
        'logo_max_width': 280,  # Smaller logo for stories (941x1672)
        'bottom_offset': 64,    # Double distance from bottom edge (10px instead of 0px)
        'expected_size': (941, 1672)
    }
}

def apply_watermark(image_path, logo_path, output_path, logo_max_width=360, bottom_offset=0):
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
                
                # Calculate position (centered horizontally)
                base_width, base_height = base_image.size
                logo_width, logo_height = logo.size
                
                # Center horizontally
                x = (base_width - logo_width) // 2
                
                # Position from bottom
                y = base_height - bottom_offset - logo_height
                
                # Ensure logo doesn't go outside image bounds
                x = max(0, min(x, base_width - logo_width))
                y = max(0, min(y, base_height - logo_height))
                
                # Create a copy of the base image
                watermarked = base_image.copy()
                
                # Paste the logo onto the base image
                watermarked.paste(logo, (x, y), logo)
                
                # Save watermarked image
                # Always save as JPG with 100% quality
                output_filename = os.path.splitext(os.path.basename(output_path))[0] + '.jpg'
                output_jpg_path = os.path.join(os.path.dirname(output_path), output_filename)
                
                # Convert to RGB for JPG (remove transparency)
                rgb_image = Image.new('RGB', watermarked.size, (255, 255, 255))
                rgb_image.paste(watermarked, mask=watermarked.split()[-1])
                rgb_image.save(output_jpg_path, quality=100)
                print(f"✓ Watermarked: {os.path.basename(image_path)} -> {output_filename}")
                return True
                
    except Exception as e:
        print(f"✗ Error processing {image_path}: {str(e)}")
        return False

def process_format(format_name):
    """Process all images in a specific format folder."""
    source_dir = os.path.join(SOURCE_BASE_DIR, format_name)
    output_dir = os.path.join(OUTPUT_BASE_DIR, format_name)
    config = FORMAT_CONFIGS[format_name]
    
    print(f"\nProcessing {format_name.upper()} images...")
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")
    print(f"Logo size: {config['logo_max_width']}px max width")
    print(f"Bottom offset: {config['bottom_offset']}px")
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Warning: Source directory '{source_dir}' not found!")
        return 0, 0
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Supported image extensions
    supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    
    # Check if source directory has images
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(supported_extensions)]
    if not image_files:
        print(f"No supported images found in '{source_dir}'")
        return 0, 0
    
    print(f"Found {len(image_files)} images to process")
    
    # Process all images in the format directory
    processed_count = 0
    error_count = 0
    
    for filename in image_files:
        input_path = os.path.join(source_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        if apply_watermark(input_path, LOGO_PATH, output_path, 
                          config['logo_max_width'], config['bottom_offset']):
            processed_count += 1
        else:
            error_count += 1
    
    return processed_count, error_count
def main():
    """Main function to process all images in all format folders."""
    print("Starting watermark application...")
    print(f"Logo: {LOGO_PATH}")
    print(f"Source base directory: {SOURCE_BASE_DIR}")
    print(f"Output base directory: {OUTPUT_BASE_DIR}")
    print("=" * 60)
    
    # Check if logo exists
    if not os.path.exists(LOGO_PATH):
        print(f"Error: Logo file '{LOGO_PATH}' not found!")
        return
    
    # Check if source base directory exists
    if not os.path.exists(SOURCE_BASE_DIR):
        print(f"Error: Source base directory '{SOURCE_BASE_DIR}' not found!")
        return
    
    # Process all formats
    total_processed = 0
    total_errors = 0
    
    for format_name in FORMAT_CONFIGS.keys():
        processed, errors = process_format(format_name)
        total_processed += processed
        total_errors += errors
    
    print("=" * 60)
    print("SUMMARY:")
    print(f"Total successfully processed: {total_processed} images")
    print(f"Total errors: {total_errors} images")
    print(f"Watermarked images saved to: {OUTPUT_BASE_DIR}/")
    print(f"  - posts: {OUTPUT_BASE_DIR}/posts/")
    print(f"  - stories: {OUTPUT_BASE_DIR}/stories/")

if __name__ == "__main__":
    main()
