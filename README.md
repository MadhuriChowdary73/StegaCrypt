# 🔐 StegaCrypt

## Secure Image Steganography Using Cryptography and LSB

StegaCrypt is a Python-based cybersecurity project that combines **cryptography** and **image steganography** to securely hide confidential messages inside digital images.

The secret message is first encrypted using a password-derived key and then hidden inside an image using **Least Significant Bit (LSB) steganography**. During extraction, the hidden payload is recovered, decrypted using the correct password, and verified for integrity.

---

## 🚀 Key Features

- 🔒 Password-based message encryption
- 🔑 PBKDF2-HMAC-SHA256 key derivation
- 🧂 Random salt generation
- 🔐 Fernet authenticated encryption
- 🖼️ LSB image steganography
- 📦 Structured secure payload
- 🛡️ SHA-256 integrity verification
- 📏 Image capacity validation
- 🔓 Secure message extraction
- ❌ Wrong-password detection
- ⚠️ Corruption/tampering detection
- 🖥️ Streamlit web interface
- 🧪 Automated testing with Pytest
- 📊 Image quality and performance evaluation

---

## 🧠 How StegaCrypt Works

StegaCrypt combines two security techniques:

### Cryptography

Cryptography protects the actual content of the secret message.

### Steganography

Steganography hides the existence of the message inside an image.

Together:

    Secret Message
          ↓
       Password
          ↓
    PBKDF2-HMAC-SHA256
          ↓
    Encryption Key
          ↓
    Fernet Encryption
          ↓
    Encrypted Message
          ↓
    Secure Payload
          ↓
    Binary Conversion
          ↓
    LSB Embedding
          ↓
      Stego Image

The receiver performs the reverse process:

    Stego Image
          ↓
    LSB Extraction
          ↓
    Secure Payload
          ↓
       Read Salt
          ↓
    Password + Salt
          ↓
    PBKDF2-HMAC-SHA256
          ↓
    Encryption Key
          ↓
    Fernet Decryption
          ↓
    SHA-256 Verification
          ↓
    Original Message

---

## 🔐 Password-Based Key Derivation

The user's password is not directly used as the encryption key.

StegaCrypt uses **PBKDF2-HMAC-SHA256** to derive a cryptographic key from the password and a randomly generated salt.

    Password + Random Salt
             ↓
      PBKDF2-HMAC-SHA256
             ↓
       Derived Key
             ↓
       Fernet Encryption

A random salt ensures that the same password does not always produce the same derived key.

The salt is stored inside the encrypted payload and does not need to be secret.

The user's password itself is never stored.

---

## 🔒 Encryption

StegaCrypt uses **Fernet authenticated encryption** from the Python `cryptography` library.

    Secret Message
          +
    Derived Encryption Key
          ↓
    Fernet Encryption
          ↓
    Ciphertext

Fernet provides confidentiality and authentication for the encrypted data.

---

## 🖼️ LSB Steganography

StegaCrypt uses **Least Significant Bit (LSB)** steganography to hide the encrypted payload inside an image.

A pixel contains three color channels:

    (R, G, B)

The current implementation stores one hidden bit in the least significant bit of the **red channel**.

For example:

    120 = 01111000
    121 = 01111001

Only the least significant bit changes.

Because the modification is very small, the visual difference between the original image and stego image is generally minimal.

---

## 📏 Image Capacity

The current implementation stores one bit per pixel.

    Capacity = Width × Height bits

For example, a 500 × 500 image provides:

    500 × 500
    = 250,000 bits
    = 31,250 bytes

The actual usable capacity is lower because the payload also contains metadata and an end marker.

---

## 📦 Secure Payload

Instead of hiding only the encrypted message, StegaCrypt creates a structured payload.

Example:

    {
        "version": 1,
        "salt": "...",
        "ciphertext": "...",
        "hash": "..."
    }

### Payload Components

| Component | Purpose |
|---|---|
| `version` | Identifies the payload format |
| `salt` | Used for password-based key derivation |
| `ciphertext` | Encrypted secret message |
| `hash` | SHA-256 integrity information |

The complete payload is converted into binary and embedded into the image.

---

## 🛡️ Integrity Verification

StegaCrypt uses SHA-256 to provide an explicit integrity check.

During encryption:

    Original Message
          ↓
       SHA-256
          ↓
      Stored Hash

During extraction:

    Recovered Message
          ↓
       SHA-256
          ↓
    Calculated Hash

The hashes are compared.

If they match, the integrity check passes.

If they do not match, the application reports an integrity verification failure.

Fernet also provides cryptographic authentication for the encrypted ciphertext.

---

## 📏 Capacity Validation

Before embedding, StegaCrypt checks whether the complete payload can fit inside the selected image.

The calculation considers:

- Encrypted message
- Salt
- SHA-256 hash
- Payload metadata
- End marker

If the payload is too large, the application stops the operation and displays an appropriate error.

---

## 🖥️ Application

StegaCrypt provides two main operations through its Streamlit interface.

### Encrypt & Hide

The user provides:

1. Cover image
2. Secret message
3. Password

The application:

1. Generates a random salt.
2. Derives an encryption key using PBKDF2.
3. Encrypts the message using Fernet.
4. Calculates the SHA-256 hash.
5. Creates the secure payload.
6. Converts the payload into binary.
7. Embeds the binary data into the image using LSB.
8. Provides the generated stego image for download.

### Extract & Decrypt

The user provides:

1. Stego image
2. Password

The application:

1. Extracts the hidden binary data.
2. Reconstructs the secure payload.
3. Retrieves the salt.
4. Derives the encryption key from the supplied password.
5. Decrypts the ciphertext.
6. Verifies the SHA-256 integrity hash.
7. Displays the original message.

---

## 🗂️ Project Structure

    StegaCrypt/
    │
    ├── app.py
    │
    ├── binary_utils.py
    ├── image_utils.py
    ├── lsb_utils.py
    ├── steganography.py
    │
    ├── crypto_utils.py
    ├── password_utils.py
    ├── secure_steganography.py
    │
    ├── test/
    │   ├── test_binary.py
    │   ├── test_lsb.py
    │   ├── test_steganography.py
    │   ├── test_crypto.py
    │   └── test_secure_steganography.py
    │
    ├── images/
    │   └── cover/
    │
    ├── requirements.txt
    ├── .gitignore
    └── README.md

---

## 📄 Module Description

| File | Description |
|---|---|
| `app.py` | Streamlit application and user interface |
| `binary_utils.py` | Converts text to binary and binary to text |
| `image_utils.py` | Handles image loading and pixel operations |
| `lsb_utils.py` | Embeds and extracts individual LSB bits |
| `steganography.py` | Handles complete message embedding and extraction |
| `crypto_utils.py` | Handles encryption and decryption |
| `password_utils.py` | Generates salts and derives encryption keys |
| `secure_steganography.py` | Integrates cryptography and steganography |
| `test/` | Automated project tests |
| `images/cover/` | Cover images used during testing |

---

## ⚙️ Technologies Used

- Python
- Streamlit
- Pillow
- Cryptography
- Fernet
- PBKDF2-HMAC-SHA256
- SHA-256
- LSB Steganography
- Pytest

---

## 🚀 Installation

### Prerequisites

Install **Python 3.x**.

### Clone the Repository

    git clone <YOUR_REPOSITORY_URL>
    cd StegaCrypt

### Create Virtual Environment

#### Windows

    python -m venv venv

Activate:

    venv\Scripts\Activate.ps1

#### Linux / macOS

    python3 -m venv venv
    source venv/bin/activate

### Install Dependencies

    pip install -r requirements.txt

---

## ▶️ Run the Application

Start the Streamlit application:

    streamlit run app.py

The application will open in your default browser.

---

## 🧪 Testing

Run the complete test suite:

    python -m pytest

Run a specific test file:

    python -m pytest test/test_steganography.py

The tests cover individual modules as well as the complete secure steganography workflow.

---

## 🧪 Test Scenarios

| Test Case | Expected Result |
|---|---|
| Valid message + valid password | Message successfully recovered |
| Wrong password | Decryption fails |
| Empty message | Validation error |
| Empty password | Validation error |
| Payload too large | Capacity error |
| Corrupted stego image | Extraction/decryption failure |
| Modified encrypted payload | Authentication/integrity failure |
| Long message | Successful recovery if capacity is sufficient |
| Image without payload | Extraction failure |



## 🔄 Complete System Flow

    ┌──────────────────────────────────────┐
    │             STEGACRYPT               │
    └──────────────────────────────────────┘
                     │
                     ▼
              Secret Message
                     │
                     ▼
                  Password
                     │
                     ▼
               Random Salt
                     │
                     ▼
           PBKDF2-HMAC-SHA256
                     │
                     ▼
              Encryption Key
                     │
                     ▼
            Fernet Encryption
                     │
                     ▼
              SHA-256 Hash
                     │
                     ▼
             Secure Payload
                     │
                     ▼
              Binary Data
                     │
                     ▼
             LSB Embedding
                     │
                     ▼
                Stego Image
                     │
                     │
              ─── RECEIVER ───
                     │
                     ▼
             LSB Extraction
                     │
                     ▼
             Secure Payload
                     │
                     ▼
                Read Salt
                     │
                     ▼
             Password + Salt
                     │
                     ▼
           PBKDF2-HMAC-SHA256
                     │
                     ▼
              Encryption Key
                     │
                     ▼
               Decryption
                     │
                     ▼
          Integrity Verification
                     │
                     ▼
             Original Message

---

## ⚠️ Limitations

- The current implementation uses the red-channel LSB.
- One bit is stored per pixel.
- PNG images are recommended for preserving hidden LSB data.
- SHA-256 alone is not a replacement for a keyed authentication mechanism.

---

## 🔮 Future Enhancements

- Multi-channel LSB embedding
- Adaptive steganography
- Payload compression
- Additional image formats
- Additional encryption schemes
- Secure metadata handling

---

## 🎯 Project Objectives

The main objectives of StegaCrypt are:

1. Demonstrate the combination of cryptography and steganography.
2. Secure confidential messages using authenticated encryption.
3. Hide encrypted information inside digital images.
4. Derive encryption keys securely from user passwords.
5. Use random salts for password-based key derivation.
6. Detect corrupted or invalid recovered data.
7. Validate image capacity before embedding.
8. Provide a simple user-friendly security application.
9. Evaluate steganography using measurable image-quality and performance metrics.

---

## 💡 Why StegaCrypt?

Cryptography protects the **message**.

Steganography hides the **existence of the message**.

StegaCrypt combines both:

    Cryptography
         ↓
    Protects the Message
         +
    Steganography
         ↓
    Hides the Message
         =
       StegaCrypt

The project provides practical implementation experience with:

- Cryptography
- Symmetric encryption
- Password-based key derivation
- PBKDF2
- Salt generation
- Hash functions
- Data integrity
- Binary data representation
- Image processing
- LSB steganography
- Secure application development
- Automated software testing

---

## 👩‍💻 Author

**Madhuri**

B.Tech Computer Science Engineering

**Project:** StegaCrypt  
**Domain:** Cryptography & Information Security

---

## 📜 License

This project is developed for **educational and academic purposes**.
