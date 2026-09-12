"""
app.py

Main Streamlit application for StegaCrypt.

Author: Madhuri
"""

import streamlit as st

st.set_page_config(
    page_title="StegaCrypt",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 StegaCrypt")
st.write("Hide encrypted messages inside images using LSB Steganography.")

mode = st.sidebar.selectbox(
    "Choose Mode",
    [
        "Encrypt & Hide",
        "Extract & Decrypt"
    ]
)

st.divider()

if mode == "Encrypt & Hide":

    st.header("Encrypt Message")

    uploaded_image = st.file_uploader(
        "Upload PNG Image",
        type=["png"]
    )

    message = st.text_area(
        "Secret Message"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Encrypt & Hide"):

        if uploaded_image is None:
            st.error("Please upload an image.")

        elif not message:
            st.error("Please enter a secret message.")

        elif not password:
            st.error("Please enter a password.")

        else:
            st.success("Backend integration coming next.")

else:

    st.header("Extract Message")

    uploaded_image = st.file_uploader(
        "Upload Stego Image",
        type=["png"]
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Extract & Decrypt"):

        if uploaded_image is None:
            st.error("Please upload a stego image.")

        elif not password:
            st.error("Please enter the password.")

        else:
            st.success("Backend integration coming next.")