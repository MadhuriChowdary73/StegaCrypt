from image_utils import (
    load_image,
    save_image,
    get_pixel
)

from steganography import embed_single_bit

image, fmt = load_image("images/cover/flower.png")

print("Before :", get_pixel(image,0,0))

embed_single_bit(image,0,0,0)

print("After  :", get_pixel(image,0,0))

save_image(
    image,
    "images/cover/output/embedded.png"
)