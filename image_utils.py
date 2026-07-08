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


def get_pixel(image:Image.Image,x:int,y:int) -> tuple[int,int,int]:
    return image.getpixel((x,y))

def set_pixel(
        image:Image.Image,
        x:int,
        y:int,
        rgb:tuple[int,int,int]

)-> None:
#this function doesnot returns anything insead it chages the image pixel     
#strings are immutable but images are mutable they can be modified directly,now NO need to return new image 
    image.putpixel((x,y),rgb)


def save_image(image:Image.Image,path:str)->None:
    image.save(path)


