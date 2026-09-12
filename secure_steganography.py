"""
secure_steganography.py

Combines AES encryption with
LSB steganography.

Author: Madhuri
Project: StegaCrypt
"""

from PIL import Image

from steganography import (
    embed_message,
    extract_message
)

from crypto_utils import (
    encrypt_message,
    decrypt_message
)


def encrypt_and_embed(
    image: Image.Image,
    message: str,
    key: bytes
) -> None:
    """
    Encrypt a message and embed it into an image.

    Args:
        image (Image.Image): Cover image.
        message (str): Secret message.
        key (bytes): Encryption key.
    """

    encrypted_message = encrypt_message(message, key)

    encrypted_string = encrypted_message.decode()

    embed_message(image, encrypted_string)


def extract_and_decrypt(
    image: Image.Image,
    key: bytes
) -> str:
    """
    Extract an encrypted message from an image and decrypt it.

    Args:
        image (Image.Image): Stego image.
        key (bytes): Encryption key.

    Returns:
        str: Original secret message.
    """

    encrypted_string = extract_message(image)

    encrypted_message = encrypted_string.encode()

    message = decrypt_message(encrypted_message, key)

    return message