from PIL import Image, ImageEnhance, ImageOps
import os
import random

SOURCE_FOLDER = 'album_covers'

# Platform Sizes (Width, Height)
PLATFORMS = {
    "fb_linkedin_banner": (3000, 1000),
    "instagram_square": (1080, 1080),
}

def apply_vintage_filter(img):
    """Applies a 90s warm film/sepia-like filter."""
    # 1. Lower saturation for that faded look
    converter = ImageEnhance.Color(img)
    img = converter.enhance(0.5)
    
    # 2. Add Warm Tint (Sepia-style)
    # Blending a grayscale version with a warm color palette
    sepia = ImageOps.colorize(ImageOps.grayscale(img), "#2e1a05", "#f5e6c8")
    img = Image.blend(img, sepia, 0.3)
    
    # 3. Boost Contrast slightly to make the logos pop
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(1.1)
    
    return img

def create_high_density_assets():
    files = [f for f in os.listdir(SOURCE_FOLDER) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    for name, size in PLATFORMS.items():
        width, height = size
        canvas = Image.new('RGB', (width, height), color=(15, 15, 15)) 
        
        if name == "instagram_square":
            cols, rows = 6, 6  # 36 albums for IG
            collage_width = width
            collage_height = height
        else:
            # High density banner: 12 columns by 4 rows
            cols, rows = 12, 4  # 48 albums total
            collage_width = int(width * 0.70) # Slightly more room for the collage
            collage_height = height

        num_tiles = cols * rows
        
        # Adjust tile size to fit the height perfectly if possible
        tile_w = collage_width // cols
        tile_h = height // rows
        tile_size = min(tile_w, tile_h)

        # Shuffle and select
        selection = random.sample(files, min(len(files), num_tiles))

        for i, filename in enumerate(selection):
            img = Image.open(os.path.join(SOURCE_FOLDER, filename)).convert('RGB')
            img = img.resize((tile_size, tile_size), Image.LANCZOS)
            
            # Apply Vintage Filter
            img = apply_vintage_filter(img)
            
            x = (i % cols) * tile_size
            y = (i // cols) * tile_size
            
            # Center the grid vertically if there's extra space
            y_offset = (height - (rows * tile_size)) // 2
            canvas.paste(img, (x, y + y_offset))

        output_path = f"duo_dense_{name}.jpg"
        canvas.save(output_path, quality=95)
        print(f"Created: {output_path} with {len(selection)} covers.")

if __name__ == "__main__":
    if not os.path.exists(SOURCE_FOLDER):
        print(f"Source folder '{SOURCE_FOLDER}' not found!")
    else:
        create_high_density_assets()