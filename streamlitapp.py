import os  
import base64
from openai import AzureOpenAI  
import streamlit as st

endpoint = os.getenv("ENDPOINT_URL", "https://foundry25032026080322994.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "75tUolqJslX2jm7cdtolUZCjuJUwXcM61HFc5tOXwwOJRxFxcY1iJQQJ99BCACfhMk5XJ3w3AAAAACOG7v3w")  

client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",
)

# Streamlit UI
st.set_page_config(page_title="Azure OpenAI Chatbot", layout="wide")
st.title("🤖 Azure OpenAI Chatbot")

# Store chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask me anything...")
if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send request to Azure OpenAI
    chat_prompt = [{"role": "system", "content": "You are a helpful AI assistant."}]
    for msg in st.session_state.messages:
        chat_prompt.append({"role": msg["role"], "content": msg["content"]})

    response = client.chat.completions.create(
        model=deployment,
        messages=chat_prompt,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Extract AI response
    ai_response = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)