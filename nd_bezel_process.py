#!/usr/bin/env python3
import json
import os
import sys
import argparse
from pathlib import Path
from PIL import Image

def process_bezel_images(base_path):
    """Process NDS bezel images, make screen areas transparent based on layout.json"""
    
    nds_bg_path = Path(base_path)
    
    # Iterate through all resolution directories
    for res_dir in nds_bg_path.iterdir():
        if not res_dir.is_dir():
            continue
        
        print(f"\nProcessing resolution directory: {res_dir.name}")
        
        layout_json_path = res_dir / "layout.json"
        if not layout_json_path.exists():
            print(f"  Skipping: layout.json not found")
            continue
        
        # Read layout.json
        with open(layout_json_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Fix JSON format issues: remove trailing commas
            import re
            content = re.sub(r',\s*}', '}', content)  # Trailing comma in object
            content = re.sub(r',\s*\]', ']', content)  # Trailing comma in array
            layout_data = json.loads(content)
        
        # Iterate through all numeric subdirectories (themes)
        for theme_dir in res_dir.iterdir():
            if not theme_dir.is_dir() or not theme_dir.name.isdigit():
                continue
            
            print(f"  Processing theme: {theme_dir.name}")
            
            # Create (name, bg) to layout_item mapping
            layout_map = {}
            for layout_item in layout_data.get("layout", []):
                bg_filename = layout_item.get("bg", "")
                name = layout_item.get("name", "")
                if bg_filename and name:
                    key = (name, bg_filename)
                    layout_map[key] = layout_item
            
            # Get all PNG files in theme directory
            for img_file in theme_dir.glob("*.png"):
                img_filename = img_file.name
                
                # Find matching layouts (need to match both name and bg)
                matching_keys = [key for key in layout_map.keys() if key[1] == img_filename]
                
                if not matching_keys:
                    continue  # No matching layout found
                
                # Process corresponding image for each matching key
                for (name, bg_filename), layout_item in layout_map.items():
                    if bg_filename != img_filename:
                        continue
                    
                    # Find the image file
                    img_path = theme_dir / bg_filename
                    if not img_path.exists():
                        print(f"    Skipping: {bg_filename} not found")
                        continue
                    
                    # Open image
                    try:
                        img = Image.open(img_path)
                        
                        # Ensure image has alpha channel
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')
                        
                        # Check for rotate attribute
                        rotate_angle = layout_item.get("rotate", 0)
                        
                        # Get image dimensions
                        width, height = img.size
                        pixels = img.load()
                        
                        # Process screen0 area
                        screen0_x = layout_item.get("screen0_x", 0)
                        screen0_y = layout_item.get("screen0_y", 0)
                        screen0_w = layout_item.get("screen0_w", 0)
                        screen0_h = layout_item.get("screen0_h", 0)
                        
                        # Swap w and h if rotated
                        if rotate_angle in [90, 270]:
                            screen0_w, screen0_h = screen0_h, screen0_w
                        
                        if screen0_w > 0 and screen0_h > 0:
                            for sy in range(screen0_y, screen0_y + screen0_h):
                                for sx in range(screen0_x, screen0_x + screen0_w):
                                    if 0 <= sy < height and 0 <= sx < width:
                                        pixels[sx, sy] = (0, 0, 0, 0)
                        
                        # Process screen1 area
                        screen1_x = layout_item.get("screen1_x", 0)
                        screen1_y = layout_item.get("screen1_y", 0)
                        screen1_w = layout_item.get("screen1_w", 0)
                        screen1_h = layout_item.get("screen1_h", 0)
                        
                        # Swap w and h if rotated
                        if rotate_angle in [90, 270]:
                            screen1_w, screen1_h = screen1_h, screen1_w
                        
                        if screen1_w > 0 and screen1_h > 0:
                            for sy in range(screen1_y, screen1_y + screen1_h):
                                for sx in range(screen1_x, screen1_x + screen1_w):
                                    if 0 <= sy < height and 0 <= sx < width:
                                        pixels[sx, sy] = (0, 0, 0, 0)
                        
                        # Save image
                        img.save(img_path, "PNG")
                        print(f"    Processed: {bg_filename} (name: {name}, rotate: {rotate_angle})")
                        
                        # Remove from map after processing to avoid duplicate processing
                        del layout_map[(name, bg_filename)]
                        break  # Process each layout only once
                        
                    except Exception as e:
                        print(f"    Error: {bg_filename} - {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process NDS bezel images, make screen areas transparent based on layout.json')
    parser.add_argument('path', help='Directory path containing layout.json and images', nargs='?', default='/mnt/e/bezels/nds/bg')
    
    args = parser.parse_args()
    
    process_bezel_images(args.path)
    print("\nProcessing complete!")