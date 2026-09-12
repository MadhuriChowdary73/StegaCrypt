"""
crypto_utils.py

Contains AES encryption and
decryption utilities.

Author: Madhuri,Kundan
Project: StegaCrypt
"""

from cryptography.fernet import Fernet

def generate_key() -> bytes:
    """
    Generate a new encryption key.

    Returns:
        bytes: Random encryption key.
    """

    return Fernet.generate_key()
def encrypt_message(
    message: str,
    key: bytes
) -> bytes:
    """
    Encrypt a message using the given key.

    Args:
        message (str): Plain text message.
        key (bytes): Encryption key.

    Returns:
        bytes: Encrypted message.
    """

    cipher = Fernet(key)

    encrypted_message = cipher.encrypt(message.encode())

    return encrypted_message

def decrypt_message(
    encrypted_message: bytes,
    key: bytes
) -> str:
    """
    Decrypt an encrypted message.

    Args:
        encrypted_message (bytes): Cipher text.
        key (bytes): Encryption key.

    Returns:
        str: Original plain text.
    """

    cipher = Fernet(key)

    decrypted_message = cipher.decrypt(encrypted_message)

    return decrypted_message.decode()