import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="Airport Lounge Assistant", page_icon="✈️")

# -------- Sidebar --------
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -------- Main UI --------
st.title("✈️ Airport Lounge Assistant")
st.caption("Flight • Card • Lounge • Payment Support")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask about flights, lounge, card or payments...")

if user_input:
    # Store & show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call Flask backend
    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(
                    BACKEND_URL,
                    json={"msg": user_input},
                    timeout=60
                )

                if response.status_code == 200:
                    bot_reply = response.json().get("result", "⚠️ No response")
                else:
                    bot_reply = "❌ Backend error"

                st.markdown(bot_reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )

    except Exception as e:
        st.error(f"❌ Cannot connect to backend: {e}")
