from image_utils import load_image
from steganography import extract_message

image, _ = load_image("images/cover/output/hello.png")

message = extract_message(image)

print("Extracted Message:", message)