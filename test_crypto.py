from crypto_utils import (
    generate_key,
    encrypt_message,
    decrypt_message
)

key = generate_key()
wrong_key = generate_key()

message = "Hello StegaCrypt"

encrypted = encrypt_message(message, key)

print("Encrypted:", encrypted)

print(decrypt_message(encrypted, wrong_key))