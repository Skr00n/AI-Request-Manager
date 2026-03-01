# Source: Below code is provided by Streamlit and AWS 

# import streamlit and chatbot file
import streamlit as st 
import memory_agent as cb

from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryBufferMemory
from langchain_aws import ChatBedrock

# Set Title for Chatbot - https://docs.streamlit.io/library/api-reference/text/st.title
st.title("AI Request Approval System") # **Modify this based on the title you want in want

# LangChain memory to the session cache - Session State - https://docs.streamlit.io/library/api-reference/session-state
if 'memory' not in st.session_state:

    llm=ChatBedrock(
        # credentials_profile_name='default',
        credentials_profile_name='krishna_paruchuri',
        model_id='anthropic.claude-3-haiku-20240307-v1:0',
        # model_id='amazon.titan-text-express-v1',
        model_kwargs= {
            "max_tokens": 300,
            "temperature": 0,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman:"]} )
    
    memory = ConversationSummaryBufferMemory(llm=llm, memory_key="chat_history", return_messages=True, human_prefix="user", ai_prefix="assistant")

    # conversational_memory = ConversationSummaryBufferMemory(llm=llm,max_token_limit=300,
#         memory_key='chat_history',
#         return_messages=True,
# )
    
    st.session_state.memory = memory #** Modify the import and memory function() attributes initialize the memory

# Add the UI chat history to the session cache - Session State - https://docs.streamlit.io/library/api-reference/session-state
if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
    st.session_state.chat_history = [] #initialize the chat history

# Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history: 
    with st.chat_message(message["role"]): 
        st.markdown(message["text"]) 

# Enter the details for chatbot input box
input_text = st.chat_input("Powered by Bedrock and Claude") # **display a chat input box
if input_text: 
    
    with st.chat_message("user"): 
        st.markdown(input_text) 
    
    st.session_state.chat_history.append({"role":"user", "text":input_text}) 

    chat_response = cb.result(input_text=input_text, conversational_memory=st.session_state.memory) #** replace with ConversationChain Method name - call the model through the supporting library
    
    with st.chat_message("assistant"): 
        st.markdown(chat_response) 
    
    st.session_state.chat_history.append({"role":"assistant", "text":chat_response})