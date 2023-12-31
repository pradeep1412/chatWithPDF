import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import GooglePalmEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatGooglePalm
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
import os


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = GooglePalmEmbeddings()
    if text_chunks == "with existing data": 
        return FAISS.load_local('db', embeddings=embeddings)
    current_vectorStore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    if "./db/index.pkl" in os.listdir():
        old_vectorstore = FAISS.load_local('db', embeddings=embeddings)
        old_vectorstore.merge_from(current_vectorStore)
        old_vectorstore.save_local('db')
        return old_vectorstore
    else:
        current_vectorStore.save_local('db')
        return current_vectorStore


def get_conversation_chain(vectorstore):
    llm = ChatGooglePalm()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if st.button("Search") and user_question:
        vectorstore = get_vectorstore("with existing data")
        st.session_state.conversation = get_conversation_chain(vectorstore)
        handle_userinput(user_question)

    # with st.sidebar:
    #     st.subheader("Your documents")
    #     pdf_docs = st.file_uploader(
    #         "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    #     if st.button("Process"):
    #         with st.spinner("Processing"):
    #             # get pdf text
    #             raw_text = get_pdf_text(pdf_docs)

    #             # get the text chunks
    #             text_chunks = get_text_chunks(raw_text)

    #             # create vector store
    #             vectorstore = get_vectorstore(text_chunks)
                
    #             # create conversation chain
    #             st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':
    main()
