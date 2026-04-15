import streamlit as st
import requests
import uuid

BACKEND_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Streamlit Chatbot")

# ----------------------------
# Session State
# ----------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat_id" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat_id = chat_id
    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }

# ----------------------------
# Sidebar: Chat History
# ----------------------------
st.sidebar.title("💬 Chats")

if st.sidebar.button("➕ New Chat"):
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat_id = chat_id
    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }
    st.rerun()

for cid, chat in st.session_state.chats.items():
    if st.sidebar.button(chat["title"], key=cid):
        st.session_state.current_chat_id = cid
        st.rerun()

current_chat = st.session_state.chats[st.session_state.current_chat_id]

# ----------------------------
# Display Messages
# ----------------------------
for msg in current_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# Input
# ----------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    current_chat["messages"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    payload = {
        "chat_id": st.session_state.current_chat_id,
        "message": user_input
    }

    response = requests.post(BACKEND_URL, json=payload)
    reply = response.json()["reply"]

    with st.chat_message("assistant"):
        st.markdown(reply)

    current_chat["messages"].append(
        {"role": "assistant", "content": reply}
    )

    if current_chat["title"] == "New Chat":
        current_chat["title"] = user_input[:30]