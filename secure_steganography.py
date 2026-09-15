"""
secure_steganography.py

Combines AES encryption with
LSB steganography.

Author: Madhuri,kundan
Project: StegaCrypt
"""

from PIL import Image

from steganography import (
    embed_message,
    extract_message,
    validate_payload_size
)

from crypto_utils import (
    encrypt_message,
    decrypt_message
)

from password_utils import (
    generate_salt,
    derive_key
)

from payload_utils import (
    build_payload,
    parse_payload,
    compute_hash
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


# ==================================================
# Password-based functions (Tasks 1, 2, 3, 4)
# ==================================================

def encrypt_and_embed_with_password(
    image: Image.Image,
    message: str,
    password: str
) -> None:
    """
    Encrypt a message using a password and embed it into an image.

    Workflow:
        1. Validate inputs.
        2. Compute SHA-256 hash of the plaintext.
        3. Generate a random 16-byte salt.
        4. Derive a Fernet-compatible key via PBKDF2-HMAC-SHA256.
        5. Encrypt the message with the derived key.
        6. Build a structured JSON payload (version, salt, ciphertext, hash).
        7. Validate the payload fits in the image.
        8. Embed the payload into the image using LSB steganography.

    Args:
        image (Image.Image): Cover image (modified in-place).
        message (str): Secret plaintext message.
        password (str): User-provided password.

    Raises:
        ValueError: If message or password is empty, or payload too large.
    """

    if not message:
        raise ValueError("Message must not be empty.")

    if not password:
        raise ValueError("Password must not be empty.")

    # Step 1: Compute SHA-256 of the original plaintext
    plaintext_hash = compute_hash(message)

    # Step 2: Generate random salt (never reused)
    salt = generate_salt()

    # Step 3: Derive Fernet-compatible key from password + salt
    key = derive_key(password, salt)

    # Step 4: Encrypt the message
    ciphertext = encrypt_message(message, key)

    # Step 5: Build structured JSON payload
    payload_str = build_payload(salt, ciphertext, plaintext_hash)

    # Step 6: Validate payload fits in image (includes END_MARKER)
    validate_payload_size(image, payload_str)

    # Step 7: Embed payload string into image via LSB steganography
    embed_message(image, payload_str)


def extract_and_decrypt_with_password(
    image: Image.Image,
    password: str
) -> str:
    """
    Extract and decrypt a password-protected message from a stego image.

    Workflow:
        1. Extract the embedded payload string from the image.
        2. Parse the structured JSON payload.
        3. Decode the stored salt.
        4. Derive the Fernet key from the user's password + stored salt.
        5. Decrypt the ciphertext (wrong password → Fernet error).
        6. Compute SHA-256 of the recovered plaintext.
        7. Compare with stored hash → integrity verification.
        8. Return the original message.

    Args:
        image (Image.Image): Stego image containing hidden payload.
        password (str): User-provided password.

    Returns:
        str: Original plaintext message.

    Raises:
        ValueError: If the payload is missing, malformed, the password
                    is wrong, or integrity verification fails.
    """

    if not password:
        raise ValueError("Password must not be empty.")

    # Step 1: Extract embedded payload string
    try:
        payload_str = extract_message(image)
    except ValueError:
        raise ValueError(
            "No valid StegaCrypt payload found in this image."
        )

    # Step 2: Parse and validate the JSON payload
    payload = parse_payload(payload_str)

    salt = payload["salt"]
    ciphertext = payload["ciphertext"]
    stored_hash = payload["hash"]

    # Step 3: Derive key from password + extracted salt
    key = derive_key(password, salt)

    # Step 4: Decrypt the ciphertext
    try:
        plaintext = decrypt_message(ciphertext, key)
    except Exception:
        raise ValueError("Incorrect password or corrupted data.")

    # Step 5: Integrity check — SHA-256 of recovered plaintext
    recovered_hash = compute_hash(plaintext)

    if recovered_hash != stored_hash:
        raise ValueError(
            "Integrity verification failed. "
            "The message may have been tampered with or corrupted."
        )

    return plaintext