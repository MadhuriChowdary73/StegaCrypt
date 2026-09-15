"""
app.py

Main Streamlit application for StegaCrypt.

Author: Madhuri
"""

import streamlit as st
from PIL import Image
from io import BytesIO

from crypto_utils import generate_key
from secure_steganography import (
    encrypt_and_embed,
    extract_and_decrypt
)


st.set_page_config(
    page_title="StegaCrypt",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# Custom CSS
# ==================================================

st.markdown(
    """
    <style>
    .main {
        padding-top: 1.5rem;
    }

    /* Hero / title area */
    .stega-hero {
        text-align: center;
        padding: 1.5rem 1rem 1rem 1rem;
    }
    .stega-hero h1 {
        font-size: 2.6rem;
        margin-bottom: 0.2rem;
    }
    .stega-hero p {
        color: #9aa0a6;
        font-size: 1.05rem;
        margin-top: 0;
    }

    /* Cards */
    .stega-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.4rem 1.4rem 1rem 1.4rem;
        margin-bottom: 1rem;
    }

    /* Key display box */
    .key-box {
        font-family: 'Courier New', monospace;
        background: #111418;
        color: #7CFC9C;
        padding: 0.9rem 1rem;
        border-radius: 10px;
        border: 1px solid rgba(124, 252, 156, 0.25);
        word-break: break-all;
        font-size: 0.95rem;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        font-weight: 600;
    }

    div.stDownloadButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
    }

    /* Sidebar title */
    section[data-testid="stSidebar"] h2 {
        font-size: 1.1rem;
    }

    hr {
        margin: 1.2rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# Header
# ==================================================

st.markdown(
    """
    <div class="stega-hero">
        <h1>🔐 StegaCrypt</h1>
        <p>Hide encrypted messages inside images using AES Encryption and LSB Steganography.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# Sidebar
# ==================================================

st.sidebar.markdown("## ⚙️ Mode")

mode = st.sidebar.selectbox(
    "Choose an operation",
    (
        "Encrypt & Hide",
        "Extract & Decrypt"
    ),
    label_visibility="collapsed"
)

st.sidebar.divider()

if mode == "Encrypt & Hide":
    st.sidebar.markdown(
        """
        **How it works**
        1. Upload a PNG image
        2. Type your secret message
        3. Click **Encrypt & Hide**
        4. Download the stego image
        5. **Save the generated key** — you'll need it to decrypt later
        """
    )
else:
    st.sidebar.markdown(
        """
        **How it works**
        1. Upload the stego PNG image
        2. Paste in the encryption key
        3. Click **Extract & Decrypt**
        4. View the recovered message
        """
    )

st.divider()

# ==================================================
# Encrypt & Hide
# ==================================================

if mode == "Encrypt & Hide":

    st.header("🔒 Encrypt Message")

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="stega-card">', unsafe_allow_html=True)

        uploaded_image = st.file_uploader(
            "Upload PNG Image",
            type=["png"]
        )

        if uploaded_image is not None:
            st.image(uploaded_image, caption="Preview", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="stega-card">', unsafe_allow_html=True)

        message = st.text_area(
            "Secret Message",
            height=140,
            placeholder="Type the message you want to hide..."
        )

        password = st.text_input(
            "Password (Currently not used)",
            type="password"
        )

        encrypt_clicked = st.button("🔐 Encrypt & Hide", type="primary")

        st.markdown('</div>', unsafe_allow_html=True)

    if encrypt_clicked:

        if uploaded_image is None:
            st.error("Please upload an image.")

        elif not message:
            st.error("Please enter a secret message.")

        elif not password:
            st.error("Please enter a password.")

        else:

            with st.spinner("Encrypting and embedding your message..."):

                image = Image.open(uploaded_image).convert("RGB")

                key = generate_key()

                encrypt_and_embed(
                    image,
                    message,
                    key
                )

                buffer = BytesIO()

                image.save(
                    buffer,
                    format="PNG"
                )

                buffer.seek(0)

            st.success("✅ Message hidden successfully!")

            result_col1, result_col2 = st.columns([1, 1], gap="large")

            with result_col1:
                st.image(buffer, caption="Stego Image", use_container_width=True)
                buffer.seek(0)

                st.download_button(
                    label="📥 Download Stego Image",
                    data=buffer,
                    file_name="stego.png",
                    mime="image/png"
                )

            with result_col2:
                st.warning(
                    "⚠️ Copy and save this encryption key. "
                    "It is required during extraction."
                )
                st.markdown(
                    f'<div class="key-box">{key.decode()}</div>',
                    unsafe_allow_html=True
                )


# ==================================================
# Extract & Decrypt
# ==================================================

else:

    st.header("🔓 Extract Message")

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="stega-card">', unsafe_allow_html=True)

        uploaded_image = st.file_uploader(
            "Upload Stego Image",
            type=["png"]
        )

        if uploaded_image is not None:
            st.image(uploaded_image, caption="Stego Image", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="stega-card">', unsafe_allow_html=True)

        key = st.text_area(
            "Encryption Key",
            height=140,
            placeholder="Paste the encryption key here..."
        )

        extract_clicked = st.button("🔓 Extract & Decrypt", type="primary")

        st.markdown('</div>', unsafe_allow_html=True)

    if extract_clicked:

        if uploaded_image is None:
            st.error("Please upload a stego image.")

        elif not key:
            st.error("Please enter the encryption key.")

        else:

            with st.spinner("Extracting and decrypting your message..."):

                image = Image.open(uploaded_image).convert("RGB")

                try:

                    message = extract_and_decrypt(
                        image,
                        key.encode()
                    )

                    success = True

                except Exception as e:
                    success = False
                    error_message = str(e)

            if success:
                st.success("✅ Message recovered successfully!")

                st.text_area(
                    "Recovered Message",
                    value=message,
                    height=150
                )
            else:
                st.error(f"Error: {error_message}")