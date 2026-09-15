"""
test_stegacrypt.py

Comprehensive pytest test suite for StegaCrypt.

Covers:
    - Password → key derivation
    - Salt generation (randomness)
    - Same password + same salt → same key
    - Encrypt/decrypt with password
    - Full encrypt + embed + extract + decrypt cycle
    - Correct password recovers message
    - Wrong password fails
    - Empty password rejected
    - Empty message rejected
    - Payload too large rejected
    - END_MARKER handling
    - SHA-256 integrity verification
    - Modified/corrupted payload detection
    - Special characters
    - Long messages within capacity
    - Existing steganography functions still work
    - Existing crypto functions still work
    - Existing LSB functions still work

Author: Madhuri
Project: StegaCrypt
"""

import pytest
import json
import base64
import hashlib
from PIL import Image

# ==================================================
# Helpers
# ==================================================

def make_image(width: int = 200, height: int = 200) -> Image.Image:
    """Create a solid-color RGB test image."""
    img = Image.new("RGB", (width, height), color=(100, 150, 200))
    return img


# ==================================================
# Section 1 — password_utils
# ==================================================

class TestPasswordUtils:

    def test_salt_is_16_bytes(self):
        from password_utils import generate_salt
        salt = generate_salt()
        assert len(salt) == 16

    def test_random_salts_are_different(self):
        from password_utils import generate_salt
        salt1 = generate_salt()
        salt2 = generate_salt()
        assert salt1 != salt2

    def test_same_password_same_salt_same_key(self):
        from password_utils import generate_salt, derive_key
        password = "TestPassword123"
        salt = generate_salt()
        key1 = derive_key(password, salt)
        key2 = derive_key(password, salt)
        assert key1 == key2

    def test_different_salt_different_key(self):
        from password_utils import generate_salt, derive_key
        password = "TestPassword123"
        salt1 = generate_salt()
        salt2 = generate_salt()
        key1 = derive_key(password, salt1)
        key2 = derive_key(password, salt2)
        assert key1 != key2

    def test_different_password_different_key(self):
        from password_utils import generate_salt, derive_key
        salt = generate_salt()
        key1 = derive_key("PasswordA", salt)
        key2 = derive_key("PasswordB", salt)
        assert key1 != key2

    def test_derived_key_is_bytes(self):
        from password_utils import generate_salt, derive_key
        salt = generate_salt()
        key = derive_key("SomePassword", salt)
        assert isinstance(key, bytes)

    def test_derived_key_is_44_bytes(self):
        """Fernet requires a 32-byte key encoded as base64url → 44 chars."""
        from password_utils import generate_salt, derive_key
        salt = generate_salt()
        key = derive_key("SomePassword", salt)
        assert len(key) == 44


# ==================================================
# Section 2 — crypto_utils
# ==================================================

class TestCryptoUtils:

    def test_generate_key_returns_bytes(self):
        from crypto_utils import generate_key
        key = generate_key()
        assert isinstance(key, bytes)

    def test_encrypt_decrypt_roundtrip(self):
        from crypto_utils import generate_key, encrypt_message, decrypt_message
        key = generate_key()
        message = "Hello StegaCrypt"
        encrypted = encrypt_message(message, key)
        decrypted = decrypt_message(encrypted, key)
        assert decrypted == message

    def test_encrypt_with_password_derived_key(self):
        from password_utils import generate_salt, derive_key
        from crypto_utils import encrypt_message, decrypt_message
        password = "MyPassword123"
        salt = generate_salt()
        key = derive_key(password, salt)
        message = "Secret data"
        encrypted = encrypt_message(message, key)
        decrypted = decrypt_message(encrypted, key)
        assert decrypted == message

    def test_wrong_key_raises(self):
        from crypto_utils import generate_key, encrypt_message, decrypt_message
        key = generate_key()
        wrong_key = generate_key()
        encrypted = encrypt_message("Hello", key)
        with pytest.raises(Exception):
            decrypt_message(encrypted, wrong_key)

    def test_wrong_password_raises(self):
        from password_utils import generate_salt, derive_key
        from crypto_utils import encrypt_message, decrypt_message
        salt = generate_salt()
        good_key = derive_key("CorrectPassword", salt)
        bad_key = derive_key("WrongPassword", salt)
        encrypted = encrypt_message("Secret", good_key)
        with pytest.raises(Exception):
            decrypt_message(encrypted, bad_key)


# ==================================================
# Section 3 — lsb_utils
# ==================================================

class TestLSBUtils:

    def test_embed_bit_0(self):
        from lsb_utils import embed_bit
        result = embed_bit(255, 0)
        assert result & 1 == 0

    def test_embed_bit_1(self):
        from lsb_utils import embed_bit
        result = embed_bit(254, 1)
        assert result & 1 == 1

    def test_extract_bit_even(self):
        from lsb_utils import extract_bit
        assert extract_bit(120) == 0
        assert extract_bit(254) == 0

    def test_extract_bit_odd(self):
        from lsb_utils import extract_bit
        assert extract_bit(121) == 1
        assert extract_bit(255) == 1

    def test_embed_then_extract(self):
        from lsb_utils import embed_bit, extract_bit
        for original_value in [0, 100, 200, 255]:
            for bit in [0, 1]:
                modified = embed_bit(original_value, bit)
                extracted = extract_bit(modified)
                assert extracted == bit


# ==================================================
# Section 4 — binary_utils
# ==================================================

class TestBinaryUtils:

    def test_text_to_binary_length(self):
        from binary_utils import text_to_binary
        result = text_to_binary("A")
        assert len(result) == 8

    def test_text_to_binary_roundtrip(self):
        from binary_utils import text_to_binary, binary_to_text
        text = "Hello"
        assert binary_to_text(text_to_binary(text)) == text

    def test_special_characters(self):
        from binary_utils import text_to_binary, binary_to_text
        text = "Hello! @#$%^&*()"
        assert binary_to_text(text_to_binary(text)) == text


# ==================================================
# Section 5 — steganography
# ==================================================

class TestSteganography:

    def test_embed_and_extract_message(self):
        from steganography import embed_message, extract_message
        img = make_image(300, 300)
        embed_message(img, "Hello World")
        recovered = extract_message(img)
        assert recovered == "Hello World"

    def test_embed_single_bit(self):
        from steganography import embed_single_bit, extract_single_bit
        img = make_image(10, 10)
        embed_single_bit(img, 0, 0, 1)
        assert extract_single_bit(img, 0, 0) == 1
        embed_single_bit(img, 0, 0, 0)
        assert extract_single_bit(img, 0, 0) == 0

    def test_end_marker_not_in_result(self):
        """Extracted message must not contain the END_MARKER."""
        from steganography import embed_message, extract_message, END_MARKER
        img = make_image(300, 300)
        embed_message(img, "Test")
        result = extract_message(img)
        assert END_MARKER not in result

    def test_message_too_large_raises(self):
        from steganography import validate_message_size
        tiny_img = make_image(5, 5)  # 25 bits = ~3 characters
        with pytest.raises(ValueError, match="too large"):
            validate_message_size(tiny_img, "This is way too long for a 5x5 image")

    def test_validate_payload_size_ok(self):
        from steganography import validate_payload_size
        img = make_image(300, 300)
        validate_payload_size(img, "short")  # Should not raise

    def test_validate_payload_size_too_large(self):
        from steganography import validate_payload_size
        tiny_img = make_image(5, 5)
        with pytest.raises(ValueError, match="too large|Payload"):
            validate_payload_size(tiny_img, "A" * 100)

    def test_get_image_capacity(self):
        from steganography import get_image_capacity
        img = make_image(100, 200)
        assert get_image_capacity(img) == 100 * 200


# ==================================================
# Section 6 — payload_utils
# ==================================================

class TestPayloadUtils:

    def test_compute_hash_is_sha256(self):
        from payload_utils import compute_hash
        message = "Hello"
        expected = hashlib.sha256("Hello".encode("utf-8")).hexdigest()
        assert compute_hash(message) == expected

    def test_compute_hash_same_input_same_output(self):
        from payload_utils import compute_hash
        assert compute_hash("abc") == compute_hash("abc")

    def test_compute_hash_different_input(self):
        from payload_utils import compute_hash
        assert compute_hash("abc") != compute_hash("xyz")

    def test_build_payload_valid_json(self):
        from payload_utils import build_payload
        salt = b"0123456789012345"
        ciphertext = b"fake_ciphertext_data"
        h = "abc123"
        result = build_payload(salt, ciphertext, h)
        data = json.loads(result)
        assert data["version"] == 1
        assert "salt" in data
        assert "ciphertext" in data
        assert "hash" in data

    def test_build_and_parse_roundtrip(self):
        from payload_utils import build_payload, parse_payload
        from password_utils import generate_salt
        salt = generate_salt()
        ciphertext = b"gAAAAABtest_ciphertext"
        h = hashlib.sha256(b"test").hexdigest()
        payload_str = build_payload(salt, ciphertext, h)
        parsed = parse_payload(payload_str)
        assert parsed["salt"] == salt
        assert parsed["ciphertext"] == ciphertext
        assert parsed["hash"] == h
        assert parsed["version"] == 1

    def test_parse_payload_invalid_json(self):
        from payload_utils import parse_payload
        with pytest.raises(ValueError, match="Invalid payload format"):
            parse_payload("not json at all {{{")

    def test_parse_payload_missing_fields(self):
        from payload_utils import parse_payload
        bad = json.dumps({"version": 1, "salt": "abc"})
        with pytest.raises(ValueError, match="missing required fields"):
            parse_payload(bad)

    def test_parse_payload_wrong_version(self):
        from payload_utils import parse_payload
        import base64
        bad = json.dumps({
            "version": 99,
            "salt": base64.urlsafe_b64encode(b"1234567890123456").decode(),
            "ciphertext": "xxx",
            "hash": "yyy"
        })
        with pytest.raises(ValueError, match="Unsupported payload version"):
            parse_payload(bad)

    def test_parse_payload_bad_salt_base64(self):
        from payload_utils import parse_payload
        bad = json.dumps({
            "version": 1,
            "salt": "!!!not_base64!!!",
            "ciphertext": "xxx",
            "hash": "yyy"
        })
        with pytest.raises(ValueError, match="not valid base64"):
            parse_payload(bad)


# ==================================================
# Section 7 — secure_steganography (password-based)
# ==================================================

class TestSecureSteganographyPasswordBased:

    def test_full_encrypt_embed_extract_decrypt_cycle(self):
        from secure_steganography import (
            encrypt_and_embed_with_password,
            extract_and_decrypt_with_password
        )
        img = make_image(300, 300)
        message = "Hello World"
        password = "MyPassword123"
        encrypt_and_embed_with_password(img, message, password)
        recovered = extract_and_decrypt_with_password(img, password)
        assert recovered == message

    def test_correct_password_recovers_message(self):
        from secure_steganography import (
            encrypt_and_embed_with_password,
            extract_and_decrypt_with_password
        )
        img = make_image(300, 300)
        encrypt_and_embed_with_password(img, "Secret123", "GoodPassword!")
        result = extract_and_decrypt_with_password(img, "GoodPassword!")
        assert result == "Secret123"

    def test_wrong_password_fails(self):
        from secure_steganography import (
            encrypt_and_embed_with_password,
            extract_and_decrypt_with_password
        )
        img = make_image(300, 300)
        encrypt_and_embed_with_password(img, "Secret", "CorrectPassword")
        with pytest.raises(ValueError, match="Incorrect password|corrupted"):
            extract_and_decrypt_with_password(img, "WrongPassword")

    def test_empty_password_encrypt_raises(self):
        from secure_steganography import encrypt_and_embed_with_password
        img = make_image(200, 200)
        with pytest.raises(ValueError, match="[Pp]assword"):
            encrypt_and_embed_with_password(img, "Hello", "")

    def test_empty_password_decrypt_raises(self):
        from secure_steganography import extract_and_decrypt_with_password
        img = make_image(200, 200)
        with pytest.raises(ValueError, match="[Pp]assword"):
            extract_and_decrypt_with_password(img, "")

    def test_empty_message_raises(self):
        from secure_steganography import encrypt_and_embed_with_password
        img = make_image(200, 200)
        with pytest.raises(ValueError, match="[Mm]essage"):
            encrypt_and_embed_with_password(img, "", "SomePassword")

    def test_payload_too_large_raises(self):
        from secure_steganography import encrypt_and_embed_with_password
        tiny_img = make_image(10, 10)  # 100 bits = ~12 chars
        long_message = "A" * 500
        with pytest.raises(ValueError, match="[Tt]oo large|[Pp]ayload"):
            encrypt_and_embed_with_password(tiny_img, long_message, "Pass123")

    def test_special_characters_work(self):
        from secure_steganography import (
            encrypt_and_embed_with_password,
            extract_and_decrypt_with_password
        )
        img = make_image(400, 400)
        message = "Hello! @#$%^&*() — Unicode: café, naïve, résumé"
        password = "P@$$w0rd!Special"
        encrypt_and_embed_with_password(img, message, password)
        recovered = extract_and_decrypt_with_password(img, password)
        assert recovered == message

    def test_long_message_within_capacity(self):
        from secure_steganography import (
            encrypt_and_embed_with_password,
            extract_and_decrypt_with_password
        )
        # 500x500 image = 250000 bits ~ 31250 chars capacity
        img = make_image(500, 500)
        message = "X" * 800  # ~800 chars + ~250 overhead fits easily
        password = "LongMsgPassword"
        encrypt_and_embed_with_password(img, message, password)
        recovered = extract_and_decrypt_with_password(img, password)
        assert recovered == message

    def test_sha256_integrity_pass(self):
        """Correct decryption produces matching hash — no error raised."""
        from secure_steganography import (
            encrypt_and_embed_with_password,
            extract_and_decrypt_with_password
        )
        img = make_image(300, 300)
        message = "Integrity check message"
        encrypt_and_embed_with_password(img, message, "Pass")
        # Should not raise — hashes must match
        result = extract_and_decrypt_with_password(img, "Pass")
        assert result == message

    def test_no_payload_image_raises(self):
        """A clean image with no hidden data should raise a clear error."""
        from secure_steganography import extract_and_decrypt_with_password
        clean_img = make_image(300, 300)
        with pytest.raises(ValueError):
            extract_and_decrypt_with_password(clean_img, "AnyPassword")

    def test_corrupted_payload_detected(self):
        """Tampered/corrupted payload should fail cleanly."""
        from secure_steganography import (
            encrypt_and_embed_with_password,
            extract_and_decrypt_with_password
        )
        from steganography import embed_message, extract_message
        img = make_image(300, 300)
        # Embed garbage JSON that looks like a payload but with bad ciphertext
        bad_payload = json.dumps({
            "version": 1,
            "salt": base64.urlsafe_b64encode(b"1234567890123456").decode(),
            "ciphertext": "this_is_not_a_valid_fernet_token",
            "hash": "0" * 64
        }, separators=(",", ":"))
        embed_message(img, bad_payload)
        with pytest.raises(ValueError, match="Incorrect password|corrupted|Integrity"):
            extract_and_decrypt_with_password(img, "SomePassword")


# ==================================================
# Section 8 — Backward compatibility (existing key-based API)
# ==================================================

class TestBackwardCompatibility:

    def test_existing_encrypt_and_embed_still_works(self):
        from crypto_utils import generate_key
        from secure_steganography import encrypt_and_embed, extract_and_decrypt
        img = make_image(300, 300)
        key = generate_key()
        encrypt_and_embed(img, "Legacy message", key)
        result = extract_and_decrypt(img, key)
        assert result == "Legacy message"

    def test_existing_steganography_embed_extract(self):
        from steganography import embed_message, extract_message
        img = make_image(200, 200)
        embed_message(img, "Old API still works")
        result = extract_message(img)
        assert result == "Old API still works"

    def test_existing_crypto_encrypt_decrypt(self):
        from crypto_utils import generate_key, encrypt_message, decrypt_message
        key = generate_key()
        enc = encrypt_message("Test", key)
        assert decrypt_message(enc, key) == "Test"
