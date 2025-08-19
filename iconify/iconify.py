#!/usr/bin/env python3
import glob
import os
from pathlib import Path
from PIL import Image


def process_icons():
    """Process PNG files and convert them to binary icon strings."""
    data = {}
    files = glob.glob('./*.png')
    
    for file in files:
        # Get filename without extension (equivalent to parse(file).name in JS)
        id_name = Path(file).stem
        
        # Open image
        img = Image.open(file).convert('RGBA')
        
        width, height = img.size
        
        # Store data (though not used in output, keeping for consistency)
        datum = data[file] = {
            'pal': [],
            'pixels': [None] * (width * height)
        }
        
        icon = f"{id_name}="
        
        # Process pixels row by row
        for y in range(height):
            for x in range(width):
                r, g, b, a = img.getpixel((x, y))
                
                # Convert to binary based on red channel brightness
                # (r < 128 ? 0 : 1) in JavaScript
                icon += '1' if r >= 128 else '0'
        
        print(icon)


if __name__ == "__main__":
    process_icons()
