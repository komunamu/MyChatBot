import streamlit as st
from openai import OpenAI

# Constants
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a helpful assistant."
}

def init_openai_client(api_key):
    try:
        client = OpenAI(api_key=api_key)
        # Test API key validity with a simple request
        client.models.list()
        return client
    except Exception as e:
        st.error("Invalid API key. Please check your key and try again.")
        return None

st.title("ChatGPT-like clone")

# Clear chat history button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = [SYSTEM_MESSAGE]
    st.rerun()

# Get the API key from the user
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if not api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

# Initialize OpenAI client
client = init_openai_client(api_key)
if not client:
    st.stop()

st.session_state["api_key"] = api_key

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_MESSAGE]

# Display chat history
for idx, message in enumerate(st.session_state.messages):
    if idx > 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # OpenAI API call
    try:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
    except APIError as e:
        st.error(f"OpenAI API Error occurred: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")