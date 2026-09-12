"""
password_utils.py

Utilities for deriving encryption keys
from user passwords.

Author: Madhuri,Kundan
Project: StegaCrypt
"""

import base64
import os

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def generate_salt() -> bytes:
    """
    Generate a random 16-byte salt.
    """
    return os.urandom(16)


def derive_key(
    password: str,
    salt: bytes
) -> bytes:
    """
    Derive a Fernet-compatible key from a password.
    """

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    key = base64.urlsafe_b64encode(
        kdf.derive(password.encode())
    )

    return key