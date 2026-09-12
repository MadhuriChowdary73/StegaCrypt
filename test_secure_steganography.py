from image_utils import load_image, save_image
from crypto_utils import generate_key
from secure_steganography import (
    encrypt_and_embed,
    extract_and_decrypt
)

image, _ = load_image("images/cover/flower.png")

key = generate_key()

encrypt_and_embed(
    image,
    "Hello Secure World",
    key
)

save_image(
    image,
    "images/cover/output/secure.png"
)

# Load the saved image again
image, _ = load_image("images/cover/output/secure.png")

message = extract_and_decrypt(
    image,
    key
)

print("Recovered Message:", message)