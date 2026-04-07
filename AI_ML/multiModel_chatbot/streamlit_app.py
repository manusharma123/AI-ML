import os
import streamlit as st
from google import genai
from dotenv import load_dotenv
from datetime import datetime

# Load env
load_dotenv()

# ------------------- CONFIG -------------------
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ------------------- CACHE CLIENT -------------------
@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)

# ------------------- SESSION -------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------- SIDEBAR -------------------
with st.sidebar:
    st.title("⚙️ Settings")

    api_key = st.text_input("Gemini API Key", type="password")

    model_name = st.selectbox(
        "Model",
        ["gemini-3.1-flash-lite-preview", "gemini-3-flash-preview","gemini-2.5-flash-lite","gemini-2.5-flash"]
    )

    temperature = st.slider("Temperature", 0.0, 1.5, 0.7)

    st.divider()

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.messages:
        chat_export = "\n".join(
            [f"{m['role']}: {m['content']}" for m in st.session_state.messages]
        )
        st.download_button(
            "📥 Export Chat",
            chat_export,
            file_name=f"chat_{datetime.now().strftime('%H%M%S')}.txt"
        )

# ------------------- API KEY CHECK -------------------
api_key = api_key or os.getenv("gemini_key")

if not api_key:
    st.warning("Enter API key in sidebar")
    st.stop()

client = get_client(api_key)

# ------------------- HEADER -------------------
st.title("🤖 Gemini AI Chatbot")

# ------------------- DISPLAY CHAT -------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------- USER INPUT -------------------
if prompt := st.chat_input("Ask something..."):
    
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # 🔥 Pass full chat history (important!)
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    {"role": m["role"], "parts": [{"text": m["content"]}]}
                    for m in st.session_state.messages
                ],
            )

            full_response = response.text
            message_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"Error: {str(e)}"
            message_placeholder.error(full_response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )