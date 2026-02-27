import streamlit as st
import requests
import uuid
import os

# ==============================
# Backend URL (auto switch)
# ==============================

API_URL = os.getenv("API_URL", "http://localhost:8000/api/ask")

st.set_page_config(page_title="DermaSense AI", layout="centered")

st.title("🧴 DermaSense AI")
st.markdown("AI-Powered Dermatology Assistant")

# ==============================
# Session Initialization
# ==============================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==============================
# Display Chat History
# ==============================

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ==============================
# Input Section
# ==============================

uploaded_image = st.file_uploader(
    "Upload skin image (optional)",
    type=["jpg", "jpeg", "png"]
)

user_input = st.chat_input("Ask your skincare question...")

if user_input:

    # Store & display user message
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    data = {
        "question": user_input,
        "session_id": st.session_state.session_id
    }

    files = None
    if uploaded_image:
        files = {
            "image": (
                uploaded_image.name,
                uploaded_image.getvalue(),
                uploaded_image.type,
            )
        }

    # ==============================
    # Streaming Assistant Response
    # ==============================

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = requests.post(
                API_URL,
                data=data,
                files=files,
                stream=True,
                timeout=120
            )

            if response.status_code != 200:
                message_placeholder.error("⚠️ Backend error.")
            else:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        text = chunk.decode("utf-8")
                        full_response += text
                        message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

        except requests.exceptions.RequestException:
            message_placeholder.error("⚠️ Could not connect to backend.")

    # Save assistant response
    st.session_state.chat_history.append(("assistant", full_response))