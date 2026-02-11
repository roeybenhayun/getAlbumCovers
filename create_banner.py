from PIL import Image
import os
import random

# Configuration
SOURCE_FOLDER = 'album_covers'
OUTPUT_NAME = 'duo_banner_clean.jpg'
BANNER_WIDTH = 3000  
BANNER_HEIGHT = 1000 
COLLAGE_RATIO = 2/3  # Collage takes up the left 2000px

def create_clean_banner():
    # 1. Setup Dimensions
    collage_width = int(BANNER_WIDTH * COLLAGE_RATIO)
    cols = 8
    rows = 3  # 8x3 = 24 tiles
    tile_size = collage_width // cols # This will be 250px per tile

    # 2. Get and Shuffle Images
    files = [f for f in os.listdir(SOURCE_FOLDER) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if len(files) < 24:
        print(f"Warning: Only found {len(files)} images. You need at least 24 for a full grid.")
        selection = files
    else:
        selection = random.sample(files, 24) # Randomly pick 24 unique covers

    # 3. Create Canvas (Black background for a sleek look)
    canvas = Image.new('RGB', (BANNER_WIDTH, BANNER_HEIGHT), color=(0, 0, 0))

    # 4. Paste Tiles into the Grid
    for i, filename in enumerate(selection):
        try:
            img = Image.open(os.path.join(SOURCE_FOLDER, filename))
            img = img.resize((tile_size, tile_size), Image.LANCZOS)
            
            x = (i % cols) * tile_size
            y = (i // cols) * tile_size
            
            canvas.paste(img, (x, y))
        except Exception as e:
            print(f"Could not process {filename}: {e}")

    # 5. Save the result
    canvas.save(OUTPUT_NAME, quality=95)
    print(f"Clean banner created! {OUTPUT_NAME}")
    print(f"Grid: {cols}x{rows} | Tile Size: {tile_size}x{tile_size}px")

if __name__ == "__main__":
    create_clean_banner()