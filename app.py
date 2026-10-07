import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

# 1. Page title & browser tab configuration
st.set_page_config(page_title="Odyssey AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Odyssey AI Chatbot")
st.caption("Built with LangChain & Streamlit • CSI Bootcamp")

# 2. Safely read API key (works on local .env and Streamlit Cloud Secrets)
load_dotenv()
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

if not api_key:
    st.error("Please add your GROQ_API_KEY to your .env file or Streamlit Secrets.")
    st.stop()

# 3. Create the LangChain ChatGroq model
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.7)

# 4. Streamlit memory: st.session_state keeps chat history across script reruns!
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display prior conversation turns in chat bubbles
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# 6. Capture user input from the bottom chat bar
if prompt := st.chat_input("Ask Odyssey anything..."):
    # Display the user's question immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    # Stream assistant response live on screen
    with st.chat_message("assistant"):
        def generate_response():
            for chunk in llm.stream(st.session_state.messages):
                yield chunk.content

        full_response = st.write_stream(generate_response)

    # Save assistant response to conversation history
    st.session_state.messages.append(AIMessage(content=full_response))


#Test locally 
#streamlit run app.py

# use Ctrl+C to stop the server for local testing