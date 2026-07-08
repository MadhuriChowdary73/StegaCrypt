from image_utils import (
    load_image,
    get_pixel,
    set_pixel,
    save_image
)


image,original_format=load_image("images/cover/flower.png")


print("Original Pixel :",get_pixel(image,0,0))
set_pixel(image,0,0,(1,0,0))
print("Modified Pixel :",get_pixel(image,0,0))
save_image(image,"images/cover/output/test.png")

new_image, fmt = load_image("images/cover/output/test.png")

print("Saved Mode   :", new_image.mode)
print("Saved Format :", fmt)

