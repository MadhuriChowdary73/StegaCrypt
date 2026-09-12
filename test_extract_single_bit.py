from image_utils import load_image
from steganography import extract_single_bit

image, _ = load_image("images/cover/output/hello.png")

bit = extract_single_bit(image, 0, 0)

print("Extracted Bit:", bit)