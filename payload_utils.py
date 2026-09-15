"""
payload_utils.py

Structured payload serialization and SHA-256 integrity
verification for StegaCrypt.

Author: Madhuri
Project: StegaCrypt
"""

import json
import hashlib
import base64


# Payload format version
PAYLOAD_VERSION = 1


def compute_hash(message: str) -> str:
    """
    Compute the SHA-256 hash of a plaintext message.

    Args:
        message (str): The original plaintext.

    Returns:
        str: Hex-encoded SHA-256 digest.
    """
    return hashlib.sha256(message.encode("utf-8")).hexdigest()


def build_payload(
    salt: bytes,
    ciphertext: bytes,
    plaintext_hash: str
) -> str:
    """
    Build a compact JSON payload string.

    Format:
        {
            "version": 1,
            "salt": "<base64url-encoded salt>",
            "ciphertext": "<Fernet token string>",
            "hash": "<SHA-256 hex digest>"
        }

    Args:
        salt (bytes): Random 16-byte salt.
        ciphertext (bytes): Fernet-encrypted ciphertext token.
        plaintext_hash (str): SHA-256 hex digest of original plaintext.

    Returns:
        str: Compact JSON string suitable for embedding in an image.
    """
    payload = {
        "version": PAYLOAD_VERSION,
        "salt": base64.urlsafe_b64encode(salt).decode("utf-8"),
        "ciphertext": ciphertext.decode("utf-8"),
        "hash": plaintext_hash,
    }
    return json.dumps(payload, separators=(",", ":"))


def parse_payload(payload_str: str) -> dict:
    """
    Parse and validate a JSON payload string.

    Args:
        payload_str (str): JSON string extracted from a stego image.

    Returns:
        dict: Parsed payload with keys:
            - "version" (int)
            - "salt" (bytes)  — already base64-decoded
            - "ciphertext" (bytes) — encoded for Fernet
            - "hash" (str)

    Raises:
        ValueError: If the payload is invalid JSON, missing required
                    fields, or has an unsupported version.
    """
    try:
        data = json.loads(payload_str)
    except (json.JSONDecodeError, TypeError):
        raise ValueError(
            "Invalid payload format: not a valid JSON structure."
        )

    required_fields = {"version", "salt", "ciphertext", "hash"}
    missing = required_fields - set(data.keys())
    if missing:
        raise ValueError(
            f"Invalid payload: missing required fields: {missing}"
        )

    if data["version"] != PAYLOAD_VERSION:
        raise ValueError(
            f"Unsupported payload version: {data['version']}"
        )

    try:
        salt_bytes = base64.urlsafe_b64decode(data["salt"])
    except Exception:
        raise ValueError("Invalid payload: salt is not valid base64.")

    ciphertext_bytes = data["ciphertext"].encode("utf-8")

    return {
        "version": data["version"],
        "salt": salt_bytes,
        "ciphertext": ciphertext_bytes,
        "hash": data["hash"],
    }
