import os
import streamlit as st
from dotenv import load_dotenv

# =========================================================
# LAYER 1: LANGCHAIN CORE ENGINE (The AI Brain)
# =========================================================
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# 1. Safely load credentials (supports local .env and Streamlit Cloud Secrets)
load_dotenv()
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

if not api_key:
    st.error("Please add your GROQ_API_KEY to your .env file or Streamlit Cloud Secrets.")
    st.stop()

# 2. Prompt Template: System instruction + dynamic conversational memory + user question
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are Odyssey, an inspiring AI mentor for CSI Bootcamp. Explain concepts clearly and concisely."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

# 3. Universal Chat Model: High-speed Groq LPU inference
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    max_tokens=1024,
)

# 4. String Output Parser: Extracts raw text stream from model chunks
parser = StrOutputParser()

# 5. LCEL Pipeline: Prompt -> Model -> Parser (The Unix-style assembly line)
chain = prompt_template | model | parser


# =========================================================
# LAYER 2: STREAMLIT WEB UI (The Presentation & Session Layer)
# =========================================================
# 6. Configure page title and header
st.set_page_config(page_title="Odyssey AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Odyssey AI Chatbot")
st.caption("Powered by LangChain (LCEL) & Streamlit • CSI Bootcamp")

# 7. Session State: Preserves chat history across script reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

# 8. Render past conversation turns
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# 9. Handle user query and stream LangChain LCEL response live
if user_prompt := st.chat_input("Ask Odyssey anything..."):
    # Display user's question immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Stream tokens live directly from the LangChain chain!
    with st.chat_message("assistant"):
        response_stream = chain.stream({
            "chat_history": st.session_state.messages,
            "question": user_prompt,
        })
        full_response = st.write_stream(response_stream)

    # Save turns as typed LangChain message objects
    st.session_state.messages.append(HumanMessage(content=user_prompt))
    st.session_state.messages.append(AIMessage(content=full_response))


#Test locally 
#streamlit run app.py

# use Ctrl+C to stop the server for local testing