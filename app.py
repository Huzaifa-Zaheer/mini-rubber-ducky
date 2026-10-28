import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Function to Load Gemini API Key
def load_gemini_api_key():
    """Load the Gemini API key from .env file, then fall back to streamlit secrets or GOOGLE_API_KEY"""
    key = os.getenv("GEMINI_API_KEY") or os.getenv("Gemini_API_KEY")
    if not key:
        try:
            key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass
    if not key:
        key = os.getenv("GOOGLE_API_KEY")
    if not key:
        try:
            key = st.secrets.get("GOOGLE_API_KEY")
        except Exception:
            pass
    return key

# Initialize Google Gemini client
api_key = load_gemini_api_key()
try:
    client = genai.Client(api_key=api_key) if api_key else None
except Exception:
    client = None

# Define the model
MODEL = "gemini-3.5-flash-lite"

# Set the page configuration
st.set_page_config(
    page_title="Mini Rubber Ducky",
    page_icon=":duck:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "GEMINI_FILE_SEARCH_STORE_NAME" not in st.session_state:
    st.session_state["GEMINI_FILE_SEARCH_STORE_NAME"] = None
if "previous_interaction_id" not in st.session_state:
    st.session_state["previous_interaction_id"] = None

# Function to Load Gemini File Search Store 
def load_gemini_file_search_store():
    """Load the Gemini File Search Store from .env file, then fall back to streamlit secrets"""
    try:
        files_search_store = os.getenv("GEMINI_FILE_SEARCH_STORE_NAME")
        if not files_search_store:
            try:
                files_search_store = st.secrets.get("GEMINI_FILE_SEARCH_STORE_NAME")
            except Exception:
                pass
        if not files_search_store:
            st.error("No Gemini File Search Store found. Please set GEMINI_FILE_SEARCH_STORE_NAME in .env or add it to Streamlit secrets.")
            return None
        return files_search_store
    except Exception as e:
        st.error(f"Error loading Gemini File Search Store: {e}")
        return None

# Define the initial message
INITIAL_MESSAGE = """
Hello, I'm Mini Rubber Ducky.
How can I help you today?
I can help you in many modes.
"""

# Function to Ask the Bot
def ask_bot(user_prompt: str) -> str:
    """Ask the bot a question and return the response"""
    if not client:
        return "Gemini API client is not initialized. Please ensure GEMINI_API_KEY is configured in .env or Streamlit secrets."
    common_kwargs = {
        "model": MODEL,
        "tools": [{
            "type": "file_search",
            "file_search_store_names": [st.session_state.GEMINI_FILE_SEARCH_STORE_NAME]
        }],
        "system_instruction": (
            "You are a RAG assistant. Answer ONLY using information retrieved "
            "from the file search store. If the answer is not present in the "
            "retrieved documents, reply exactly: 'I could not find that in the "
            "provided documents.' Do not use outside knowledge. Do not guess."
        ),
    }

    if st.session_state["previous_interaction_id"]:
        interaction = client.interactions.create(
            previous_interaction_id=st.session_state.previous_interaction_id,
            input=user_prompt,
            **common_kwargs
        )
    else:
        interaction = client.interactions.create(
            input=user_prompt,
            **common_kwargs
        )
    st.session_state.previous_interaction_id = interaction.id
    return interaction.output_text

    
# Function to Reset Conversation
def reset_conversation():
    """Reset the conversation history"""
    st.session_state.messages = [{
        "role": "assistant",
        "content": INITIAL_MESSAGE.strip()
    }]
    st.rerun()


def main():
    # Sidebar with reset button
    with st.sidebar:
        st.header("Settings")
        if st.button("Reset Conversation"):
            reset_conversation()

    # Check for Gemini Client
    if not client:
        st.error("No Gemini API key found. Please set GEMINI_API_KEY in .env or add it to Streamlit secrets.")
        return

    # Load the Gemini File Search Store
    if not st.session_state.GEMINI_FILE_SEARCH_STORE_NAME:
        st.session_state.GEMINI_FILE_SEARCH_STORE_NAME = load_gemini_file_search_store()

    # Initialize Messages
    if not st.session_state.messages:
        st.session_state.messages = [
            {"role": "assistant", "content": INITIAL_MESSAGE.strip()}
        ]

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    prompt = st.chat_input("Ask me anything about multimodal RAG")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        # Process the user prompt
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ask_bot(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

            

if __name__ == "__main__":
    main()