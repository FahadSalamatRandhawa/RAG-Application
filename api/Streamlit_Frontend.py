import streamlit as st

st.set_page_config(
    page_title="RAG app",
    page_icon="💻",
)
st.session_state.messages=[]
st.write("# Welcome to RAG application where you can chat with your data! 👋")

st.markdown("#### Upload to database ")
document=st.file_uploader("Upload document")
if document:
    print(document.read())


st.markdown("#### Chat with database ")
chat=st.chat_input("Enter your message")
if(chat):
    st.success("Chatted")
