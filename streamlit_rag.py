# This code use MultiQuery chain 

# section 1.Load needed packages functions
 
import streamlit as st
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv
import os
import time

from ui.chat_ui import message_func, user_avatar, bot_avatar
 
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

    # retriever = vectorstore.as_retriever(search_kwargs={'k':4})
    retriever=MultiQueryRetriever.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_type='mmr'),
    )
        
    # section 4. setup the Retriever Chain
    
    # qa = RetrievalQA.from_chain_type(llm = llm, chain_type='stuff',
    #                                 retriever= retriever, return_source_documents=False)   
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
        return_source_documents=False
        )

    st.image('./assets/fintech-header.png')
    st.title('📈🤖 Alpha Bot')

    # with st.sidebar:
        
        # st.image('./assets/big_banks_canada.jpg',width=300)
        # st.title('🤖 Alpha Bot')
        # st.caption("🚀 a dedicated bot for Toronto big 5 banks! ")



    with open("ui/sidebar.md", "r") as sidebar_file:
        sidebar_content = sidebar_file.read()

    with open("./ui/styles.md", "r") as styles_file:
        styles_content = styles_file.read()

    st.sidebar.markdown(sidebar_content)

    st.write(styles_content, unsafe_allow_html=True)

    gradient_text_html = """
    <style>
    .gradient-text {
        font-weight: bold;
        background: -webkit-linear-gradient(left, purple, blue);
        background: linear-gradient(to right, purple, blue);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline;
        font-size: 3em;
    }
    </style>
    <div class="gradient-text">Alpha Bot</div>
    """

    st.markdown(gradient_text_html, unsafe_allow_html=True)
    # Add a reset button
    if st.sidebar.button("Reset Chat"):
        for key in st.session_state.keys():
            del st.session_state[key]

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    if prompt := st.chat_input():
        st.session_state.messages.append({'role':'user','avatar':user_avatar,'content':prompt})
        # st.chat_message('user', avatar= user_avatar).write(prompt)

        response = qa.invoke(prompt)
        msg = response['result']
        st.session_state.messages.append({'role':"assistant", 'avatar':bot_avatar,'content':msg})
        # st.chat_message("assistant", avatar = bot_avatar).write(msg)
 
    for msg in st.session_state.messages:
        message_func(msg)


if __name__=='__main__':
    main()
