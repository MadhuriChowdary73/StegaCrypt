from image_utils import load_image
image,original_format=load_image("images/cover/flower.png")
print("Image Loaded Sucessfully")
print("size :",image.size)
print("Mode: ",image.mode)
print("Format :",original_format)
