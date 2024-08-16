from dotenv import load_dotenv 
import streamlit as st 
from langchain_community.vectorstores import Chroma 
import uuid, os 
from langchain_core.prompts import SystemMessagePromptTemplate 
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI 
from langchain.chains import RetrievalA, ConversationalRetrievalChain 
from langchain.prompts import PromptTemplate 
from langchain.memory import ConversationBufferWindowMemory 
from gen_token import TokenGenerator

load_dotenv ()

azure_tenant = st. secrets ["azure_tenant"]
client_id = st. secrets ["client_id"]
scope = st. secrets ["azure_oai_api_scope"]
azure_endpoint = st. secrets ["OPENAI_API_ENDPOINT" ]
openai_api_version = st. secrets ["OPENAI_API_VERSION" ]
subscription_key = st. secrets ["SUBSCRIPTION_KEY"]
embedding_deployment_name = 'text-embedding-ada-002'
deployment_name = 'gpt-4-turbo'
chroma_store = st.secrets["CHROMA_STORE"]

token_auth = TokenGenerator()
generate_token = token_auth.get_access_token()
access_token = os.getenv("access_token")

@st.cache_resource 
def load_chain( ):
    embeddings = AzureOpenAIEmbeddings (
        azure_deployment=embedding_deployment_name,
        model=embedding_deployment_name, 
        api_key=access_token,
        azure_endpoint=azure_endpoint,
        openai_api_version=openai_api_version,
        chunk_size=5, 
        show_progress_bar=True, 
        max_retries=60, 
        default_headers={
                "x-subscription-key": subscription_key,
                "X-correlation-id": str(uuid.uuid4())}
    )

    llm1 = AzureChatOpenAI(
            azure_deployment=deployment_name,
            api_key=access_token,
            azure_endpoint=azure_endpoint,
            openai_api_version=openai_api_version,
            temperature=0.0,
            default_headers={
            "x-subscription-key": subscription_key,
            "x-correlation-id": str(uuid.uuid4())
            })
    
    vectordb = Chroma(
        persist_directory=chroma_store,
        embedding_function=embeddings, 
        collection_name="consent_collection"
    )

    # Build prompt
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know don't know, don't try to make up an answer.
        (context}
        Question: {question}
        Helpful Answer: """
    
    qa_chain_prompt = PromptTemplate.from_template(template)

    memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history") #output_key='answer' # or 'source_documents'

    qa = ConversationalRetrievalChain.from_llm(
            llm1,
            retriever=vectordb.as_retriever(search_kwargs={"k": 50}), 
            memory=memory,
            get_chat_history=lambda h: h, 
            return_source_documents=False
        )
    
    qa.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate(prompt=qa_chain_prompt)

    return qa