'''
# 1.Load needed packages functions
'''
import streamlit as st
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
import os

'''
# 2.setup OpenAI LLM and Embedding models
'''
load_dotenv()
OPENAI_API_KEY  = os.getenv("openai_api_key")  

# llm = OpenAI(temperature=0.01)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002") 
# text-embedding-ada-002 is a cost-efficient model https://platform.openai.com/docs/guides/embeddings/embedding-models
# print(llm('tell me  a joke?'))
# print(embeddings.embed_query('hello')[0:5])
'''
# 3.load pdf earning callls data into Vector Store and persist it 
'''
documents = []
for file in os.listdir('./data/'):
    if 'Earning_Speech' in file:
        pdf_path = f'./data/{file}'
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.split_documents(documents)

vectorstore = Chroma.from_documents(texts, embeddings, persist_directory='./chromadb/')
vectorstore.persist()

print('persist all the documents')