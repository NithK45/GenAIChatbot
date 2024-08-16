import streamlit as st
import query_llm_vectordb 
import time

st.set_page_config(page_title="Doc Searcher", page_icon=": robot:") 
st. header ("Query PDF Source")
chain = query_llm_vectordb. load_chain()
company_logo = '/Users/nkothal/PycharmProjects/pythonProject/chat_icon.png'

# Initialize chat history
if 'messages' not in st.session_state:
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "assistant",
                    "content": "Hi human! I am AthenaAT's smart AI. How can I help you today?"}]

# Custom avatar for the assistant, default avatar for user 

for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=company_logo):
            st.markdown (message ["content"] )
    else:
        with st.chat_message(message["role"]):
            st. markdown (message ["content"])

# Chat logic
if query:= st.chat_input("Ask me anything"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    # Display user message in chat message container
    with st.chat_message("user"):
        st. markdown (query)
    with st.chat_message("assistant", avatar=company_logo):
        message_placeholder = st.empty()
        #send user's question to our chain
        result = chain({"question": query})
        response = result['answer']
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.85)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown (full_response)
    # Add assistant message to chat history
    st. session_state.messages.append ({"role": "assistant", "content": response})

