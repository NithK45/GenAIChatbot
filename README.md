# GenAIChatbot
Chat with your documents using generative AI

## Python Requirements
- Langchain
- Chromadb
- Streamlit

## Other requirements
Embedding model used: text-embedding-ada-002
Chatgpt version: gpt-4-turbo

## USAGE
Update the env_params.env and secrets.toml files with necessary environment variables.

To load source pdfs into Chromadb, run
```
python load_chromadb.py
```
To run the GenAI chatbot
```
streamlit run streamllt.py
