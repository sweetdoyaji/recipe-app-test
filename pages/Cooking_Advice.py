import streamlit as st
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, SafetySetting, FinishReason, Tool
from vertexai.preview.generative_models import grounding

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
    "seed": 0,
}

tools = [
    Tool.from_retrieval(
        retrieval=grounding.Retrieval(
            source=grounding.VertexAISearch(datastore="projects/YOUR_PROJECT_ID/locations/global/collections/default_collection/dataStores/old-cookbooks-id"),
        )
    ),
]
safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]

def start_chat_session():
    vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")
    model = GenerativeModel(
        "gemini-2.0-flash-001",
        tools=tools,
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    chat = model.start_chat()
    return chat





if "chat" not in st.session_state:
  st.session_state.chat = start_chat_session()
else:
  chat = st.session_state.chat

if "history" not in st.session_state:
  st.session_state.history = st.session_state.chat.history


# Setup done, let's build the page UI
st.set_page_config(page_title="AI Recipe Haven - AI Cooking Advisor", page_icon="🍲")
st.title("Your AI Cooking Advisor")

#
# Here's the code to create the chat interface
# Uncomment the below code when instructed
# 


for message in st.session_state.history:
    with st.chat_message(message.role):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("How can I help you today?"):

    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = chat.send_message(prompt)

    with st.chat_message("assistant"):
        st.markdown(response.candidates[0].content.parts[0].text)
