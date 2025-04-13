#!/usr/bin/env python3
"""
Create placeholder screenshot images for the Finance Analyzer
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm

def create_placeholder_image(title, filename, width=1280, height=720):
    """Create a placeholder image with the given title and save to the given filename"""
    # Create a blank image with a gradient background
    x = np.linspace(0, 1, width)[:, np.newaxis]
    y = np.linspace(0, 1, height)[np.newaxis, :]
    
    # Create gradient background
    r = np.abs(np.sin(x * 5)) * 30 + 20
    g = np.abs(np.cos(y * 5)) * 30 + 80 
    b = np.abs(np.sin(x * 2 + y * 2)) * 50 + 150
    
    # Combine channels
    rgb = np.dstack((r, g, b)).astype(np.uint8)
    
    # Create PIL image
    img = Image.fromarray(rgb)
    draw = ImageDraw.Draw(img)
    
    # Try to find a nice font
    try:
        # Try to use a nice font if available
        fonts = fm.findSystemFonts()
        font_choices = [f for f in fonts if 'Arial' in f or 'Helvetica' in f or 'DejaVu' in f]
        if font_choices:
            font_path = font_choices[0]
        else:
            # Default to a basic font
            font_path = fm.findfont(fm.FontProperties())
        
        font_large = ImageFont.truetype(font_path, 60)
        font_small = ImageFont.truetype(font_path, 40)
    except:
        # If font handling fails, use default font
        font_large = ImageFont.load_default()
        font_small = font_large
    
    # Add the title
    text_width, text_height = draw.textsize(title, font=font_large)
    draw.text(
        ((width - text_width) // 2, (height - text_height) // 2 - 50),
        title,
        font=font_large,
        fill=(255, 255, 255)
    )
    
    # Add a subtitle
    subtitle = "Finance Analyzer screenshot placeholder"
    sub_width, sub_height = draw.textsize(subtitle, font=font_small)
    draw.text(
        ((width - sub_width) // 2, (height - sub_height) // 2 + 50),
        subtitle,
        font=font_small,
        fill=(255, 255, 255, 180)
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
