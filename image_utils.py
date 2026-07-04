"""
image_utils.py

Description:
Contains utility functions for loading,
reading and saving images.

Author: Madhu
Project: StegaCrypt
"""
from PIL import Image


def load_image(path: str) -> tuple[Image.Image , str] :
    """
    Load an image and convert it to RGB mode.

    Args:
        path (str): Path to the image.

    Returns:
        Image: Pillow Image object.
    """
    image = Image.open(path)
    original_format =image.format
    image = image.convert("RGB")
    return image,original_format



