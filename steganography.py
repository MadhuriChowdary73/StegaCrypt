"""
steganography.py

Contains functions for hiding
and extracting secret data.

Author: Madhuri
Project: StegaCrypt
"""
from binary_utils import text_to_binary
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


def get_image_capacity(image:Image.Image) -> int:
    width,height=image.size
    return width*height

def validate_message_size(
        image:Image.Image,
        message:str
)-> None:
    
    binary_message =text_to_binary(message)
    required_bits = len(binary_message)
    available_bits = get_image_capacity(image)

    if required_bits > available_bits:
        raise ValueError(
            "Message is too Large to fit in this particular Image"
        )


def embed_message(
        image:Image.Image,
        message: str
) -> None:
    validate_message_size(image,message)

    binary_message = text_to_binary(message)

    width,height=image.size
    index=0
    for y in range(height):
        for x in range(width):
            
            if index >= len(binary_message):
                return
            
            bit = int(binary_message[index])
            embed_single_bit(image,x,y,bit)
            index+=1

