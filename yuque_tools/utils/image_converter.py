import os
import logging
from PIL import Image
import cairosvg

def convert_image_to_png(image_path):
    """Convert any image format to PNG format
    
    Args:
        image_path: Path to the source image
        
    Returns:
        str: Path to the converted PNG image
    """
    try:
        # Get the file extension
        _, extension = os.path.splitext(image_path)
        
        # Handle SVG files separately
        if extension.lower() == '.svg':
            png_image_path = os.path.splitext(image_path)[0] + '.png'
            cairosvg.svg2png(url=image_path, write_to=png_image_path)
            os.remove(image_path)
            logging.debug(f"Converted SVG {image_path} to {png_image_path}")
            return png_image_path
            
        # Check if the image is already in PNG format
        if extension.lower() == '.png':
            return image_path
        
        # Open the image using PIL
        image = Image.open(image_path)
        
        # Convert the image to PNG format
        png_image_path = os.path.splitext(image_path)[0] + '.png'
        
        # Save as PNG (if image is in RGBA mode, convert to RGB first)
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            background.save(png_image_path, 'PNG')
        else:
            image.convert('RGB').save(png_image_path, 'PNG')
        
        # Close the image
        image.close()
        
        # Remove the original image file
        os.remove(image_path)
        
        logging.debug(f"Converted {image_path} to {png_image_path}")
        return png_image_path
        
    except Exception as e:
        logging.error(f"Failed to convert image {image_path}: {str(e)}")
        return image_path 