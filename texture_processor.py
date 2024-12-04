from PIL import Image
from wand import image as wand_image
import os
import json

def create_collage(images, output_size, grid_size, image_size):
    # Create a new blank image for the collage
    collage = Image.new('RGBA', output_size)
    
    # Calculate the number of images per row and column
    images_per_row = grid_size[0]
    images_per_col = grid_size[1]
    
    # Place each image in the collage
    for index, img in enumerate(images):
        # Calculate the position for this image
        row = index // images_per_row
        col = index % images_per_row
        x = col * image_size[0]
        y = row * image_size[1]
        
        # Paste the image into the collage
        collage.paste(img, (x, y))
    
    return collage

# Example usage
if __name__ == "__main__":
    
    image_files = [
        'inputs/sand.png'
    ]
    # Load the JSON file
    with open('job.json', 'r') as f:
        config = json.load(f)

    # Extract input and output paths
    image_files = config['files']

    input_size = 16
    collage_size = 2**7  # 4 is the min that you should use
    print("Original image size: ", collage_size)
    # Basic checks to make sure the inputs will work out
    assert collage_size >= input_size
    assert 2048 % collage_size == 0

    output_size = (2048, 2048)  # Final collage size
    grid_size = (2048 // collage_size, 2048 // collage_size)  # Grid size
    image_size = (collage_size, collage_size)  # Each image resized to collage_size x collage_size

    image_files = [{"input":"shallow.png","output":"g_sha.dds"}]
    
    # Load and resize images
    for paths in image_files:
        img = Image.open(f"inputs/{paths['input']}")
        img = img.resize(image_size, 0)
        
        # Create a collage with the single image repeated
        images = [img] * (grid_size[0] * grid_size[1])
        
        collage = create_collage(images, output_size, grid_size, image_size)
        collage_name = f"temp/collage_{os.path.basename(paths['input']).split('.')[0]}.png"
        collage.save(collage_name)
        
        with wand_image.Image(filename=collage_name) as img:
            img.compression = 'dxt5'
            output_filename = os.path.basename(paths['output']).split('.')[0] + '.dds'
            img.save(filename=f"C:/Users/Eric/Games/Age of Empires 2 DE/76561198325348433/mods/local/minecraft/resources/_common/terrain/textures/2x/{output_filename}")