from image_utils import load_image,save_image
from steganography import embed_message

image,_=load_image("images/cover/flower.png")

embed_message(image,"Hello")

save_image(
    image,
    "images/cover/output/hello.png"
)

print("Message Embedded Sucessfully!!")