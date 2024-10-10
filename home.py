import streamlit as st
from openai import OpenAI

def hide_streamlit_defualt_menu_footer():
   hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
   st.markdown(hide_menu_style, unsafe_allow_html=True)
    
hide_streamlit_defualt_menu_footer()

st.title("Article Summarization Bot")
st.warning("We appreciate your engagement! Please note, this demo is designed to process a maximum of 3 interactions and may be unavailable if too many people use the service concurrently. Thank you for your understanding.")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter article's URL"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
