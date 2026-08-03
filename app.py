import streamlit as st
from config.settings import settings
from core.engine import HuskEngine
from core.memory import ConversationMemory

# Page setup
st.set_page_config(page_title=f"{settings.HUSK_NAME} AI", page_icon="🤖", layout="centered")
st.title(f"🤖 {settings.HUSK_NAME} AI")
st.caption(f"Powered by {settings.DEFAULT_MODEL} | Live Web & System Integration")

# Initialize session state engine & memory
if "engine" not in st.session_state:
    st.session_state.engine = HuskEngine()

if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory(max_history=15)

# Render chat history from memory
for msg in st.session_state.memory.get_messages():
    if msg["role"] in ["user", "assistant"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# User Chat Input
if user_input := st.chat_input("Message Husk..."):
    # Display user input in UI
    with st.chat_message("user"):
        st.write(user_input)
    
    # Store user input
    st.session_state.memory.add_message("user", user_input)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Husk is processing..."):
            response_text = st.session_state.engine.generate_response(
                messages=st.session_state.memory.get_messages()
            )
            
            if response_text:
                st.write(response_text)
                st.session_state.memory.add_message("assistant", response_text)
            else:
                st.error("Failed to generate a response from Husk.")