#!/usr/bin/env python3
"""
Generate PWA icons for BhashaMitra

This script creates proper RGB PNG icons for the PWA manifest.
Run from the frontend directory:
    python3 scripts/generate-icons.py

Requirements:
    pip install Pillow
"""

from PIL import Image, ImageDraw
import os

# Colors
ORANGE = "#F97316"
BACKGROUND = "#FFF7ED"

def create_icon(size: int, output_path: str):
    """Create a simple circular icon with the BhashaMitra orange color."""
    img = Image.new('RGB', (size, size), BACKGROUND)
    draw = ImageDraw.Draw(img)
    
    # Draw a circle with orange color
    margin = size // 8
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=ORANGE,
        outline=None
    )
    
    img.save(output_path, 'PNG')
    print(f"Created {output_path}")

def main():
    """Generate all required PWA icons."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    public_dir = os.path.join(script_dir, '..', 'public')
    
    # Generate 192x192 icon
    create_icon(192, os.path.join(public_dir, 'icon-192.png'))
    
    # Generate 512x512 icon
    create_icon(512, os.path.join(public_dir, 'icon-512.png'))
    
    print("\nIcons generated successfully!")
    print("Run 'file public/icon-192.png' to verify they are RGB PNG format.")

if __name__ == '__main__':
    main()
