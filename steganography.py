"""
steganography.py

Contains functions for hiding
and extracting secret data.

Author: Madhuri
Project: StegaCrypt
"""

from image_utils import(
    get_pixel,
    set_pixel
)

from lsb_utils import embed_bit

from PIL import Image


def embed_single_bit(
        image:Image.Image,
        x:int,
        y:int,
        bit:int

) -> None:

    pixel=get_pixel(image,x,y)
    red,green,blue=pixel

    red=embed_bit(red,bit)

    new_pixel=(red,green,blue)

    set_pixel(image,x,y,new_pixel)
