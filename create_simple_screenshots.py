#!/usr/bin/env python3
"""
Create simple placeholder screenshot images for the Finance Analyzer
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_placeholder_image(title, filename, width=1280, height=720):
    """Create a placeholder image with the given title and save to the given filename"""
    # Create a blank image with a gradient background
    img = Image.new('RGB', (width, height), color=(60, 90, 180))
    draw = ImageDraw.Draw(img)
    
    # Create a simple gradient overlay
    for y in range(height):
        for x in range(width):
            r = int(60 + (x / width) * 30)
            g = int(90 + (y / height) * 40)
            b = int(180 - (x / width) * (y / height) * 50)
            img.putpixel((x, y), (r, g, b))
    
    # Add the title
    try:
        # Try to use a default font
        font_large = ImageFont.load_default()
    except:
        # If that fails, create a very basic font
        font_large = ImageFont.load_default()
    
    # Add the title and subtitle text
    draw.text(
        (width // 2 - 200, height // 2 - 50),
        title,
        font=font_large,
        fill=(255, 255, 255)
    )
    
    draw.text(
        (width // 2 - 200, height // 2 + 50),
        "Finance Analyzer screenshot placeholder",
        font=font_large,
        fill=(230, 230, 230)
    )
    
    # Save the image
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)
    print(f"Created placeholder image: {filename}")

def main():
    """Create all required placeholder images"""
    screenshots = [
        ("Dashboard Overview", "dashboard.png"),
        ("Transaction Analysis", "transactions.png"),
        ("Personalized Recommendations", "recommendations.png"),
        ("AI Financial Assistant", "ai_chat.png")
    ]
    
    for title, filename in screenshots:
        create_placeholder_image(
            title, 
            os.path.join("screenshots", filename)
        )

if __name__ == "__main__":
    main()
