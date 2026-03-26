import streamlit as st
import os
import json
import requests
# from streamlit_mic_recorder import mic_recorder

UPLOAD_API = "http://127.0.0.1:8000/upload"

CHAT_DIR = "saved_chats"


def render_sidebar():

    st.sidebar.title("💬 VizTalk")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -------- NEW CHAT --------
    if st.sidebar.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.sidebar.divider()

    # # -------- VOICE INPUT --------
    # st.sidebar.subheader("🎤 Voice Query")

    # audio = mic_recorder(
    #     start_prompt="Start Recording",
    #     stop_prompt="Stop Recording",
    #     key="voice_recorder"
    # )

    # if audio:
    #     st.sidebar.success("Voice recorded!")

        # try:
        #     response = requests.post(
        #         "http://127.0.0.1:8000/voice",
        #         files={"file": audio["bytes"]}
        #     )

        #     result = response.json()
        #     transcript = result.get("text", "")

        #     if transcript:
        #         st.session_state.voice_query = transcript
        #         st.sidebar.write("You said:")
        #         st.sidebar.write(transcript)

        # except Exception as e:
        #     st.sidebar.error("Voice processing failed")
        #     st.sidebar.write(e)

    # st.sidebar.divider()

    # -------- CSV UPLOAD --------
    st.sidebar.subheader("📁 Upload Dataset")

    uploaded_file = st.sidebar.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    if uploaded_file:

        try:

            response = requests.post(
                UPLOAD_API,
                files={"file": uploaded_file}
            )

            result = response.json()

            st.sidebar.success("Dataset uploaded!")

            st.sidebar.write("Columns:")
            st.sidebar.write(result.get("columns", []))

        except Exception as e:

            st.sidebar.error("Upload failed")
            st.sidebar.write(e)

    st.sidebar.divider()

    # -------- SAVED CHATS --------
    st.sidebar.subheader("📜 Saved Conversations")

    if not os.path.exists(CHAT_DIR):
        os.makedirs(CHAT_DIR)

    files = os.listdir(CHAT_DIR)
    files.sort(reverse=True)

    for file in files:

        title = file.replace(".json", "").replace("_", " ").title()

        if st.sidebar.button(title, key=file):

            with open(os.path.join(CHAT_DIR, file), "r") as f:
                st.session_state.messages = json.load(f)

            st.rerun()

    st.sidebar.divider()

    # -------- EXAMPLE QUERIES --------
    st.sidebar.subheader("💡 Example Queries")

    st.sidebar.markdown("""
    • Show revenue by region  
    • Show monthly revenue trend  
    • Show top product categories  
    """)

    st.sidebar.divider()

    # -------- LOGOUT --------
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.page = "landing"
        st.session_state.messages = []
        st.rerun()