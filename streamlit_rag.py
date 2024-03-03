 
# section 1.Load needed packages functions
 
import streamlit as st
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os
import time
 
# section 2.setup OpenAI LLM and Embedding models
 
# load_dotenv()
# OPENAI_API_KEY  = os.getenv("openai_api_key")  
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

llm = OpenAI(temperature=0.01)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002") 
# text-embedding-ada-002 is a cost-efficient model https://platform.openai.com/docs/guides/embeddings/embedding-models
# print(llm('tell me  a joke?'))
# print(embeddings.embed_query('hello')[0:5])
 
# section 3.load pdf earning callls data from Vector Store  
 
 
 
# section 4. setup the Retriever Chain
 
 
# section 5. Create Streamlit front end
 
def main():
    vectorstore = Chroma(persist_directory='./chromadb/', embedding_function=embeddings)

    retriever = vectorstore.as_retriever(search_kwargs={'k':4})

    
    # section 4. setup the Retriever Chain
    
    qa = RetrievalQA.from_chain_type(llm = llm, chain_type='stuff',
                                    retriever= retriever, return_source_documents=False)   

    st.image('./assets/shih_tzu_bot.jpg',width=300)
    st.title('🐶 Alpha Bot')

    with st.sidebar:
        
        st.image('./assets/big_banks_canada.jpg',width=300)
        st.title('🐶 Alpha Bot')
        st.caption("🚀 a dedicated bot for Toronto big 5 banks! ")

 
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

 
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            avatar = './assets/investor_avatar.jpg'
        elif msg['role'] == 'assistant':
            avatar = './assets/banks_canada.jpg'
        with st.chat_message(msg['role'], avatar=avatar):
            st.markdown(msg['content'])


    if prompt := st.chat_input():
        st.session_state.messages.append({'role':'user','avatar':'./assets/investor_avatar.jpg','content':prompt})
        st.chat_message('user', avatar= './assets/investor_avatar.jpg').write(prompt)

        response = qa.invoke(prompt)
        msg = response['result']
        st.session_state.messages.append({'role':"assistant", 'avatar':"./assets/banks_canada.jpg",'content':msg})
        st.chat_message("assistant", avatar = './assets/banks_canada.jpg').write(msg)

if __name__=='__main__':
    main()
