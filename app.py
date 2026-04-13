import streamlit as st
import tempfile
import os
from agent import ingest_documents, ingest_from_s3, list_s3_documents, query_rag

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("RAG Chatbot — AWS + LlamaIndex + Groq")

if "index" not in st.session_state:
    st.session_state.index = None
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Document Source")
    
    tab1, tab2 = st.tabs(["S3 Bucket", "Local Upload"])
    
    with tab1:
        st.subheader("Load from S3")
        s3_docs = list_s3_documents()
        if s3_docs:
            selected_doc = st.selectbox(
                "Select document",
                s3_docs
            )
            if st.button("Load from S3", type="primary"):
                with st.spinner("Loading from S3..."):
                    index, message = ingest_from_s3(selected_doc)
                    if index:
                        st.session_state.index = index
                        st.success(message)
                    else:
                        st.error(message)
        else:
            st.warning("No documents found in S3 bucket")

    with tab2:
        st.subheader("Upload Local File")
        uploaded_file = st.file_uploader(
            "Choose PDF or TXT",
            type=["pdf", "txt"]
        )
        if uploaded_file is not None:
            if st.button("Ingest Document", type="primary"):
                with st.spinner("Processing..."):
                    suffix = os.path.splitext(uploaded_file.name)[1]
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=suffix
                    ) as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name
                    index, message = ingest_documents(tmp_path)
                    if index:
                        st.session_state.index = index
                        st.success(message)
                    else:
                        st.error(message)

    if st.session_state.index is not None:
        st.success("Document ready!")
    else:
        st.warning("No document loaded")

st.subheader("Chat")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask a question about your document...")

if query:
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })
    with st.chat_message("user"):
        st.markdown(query)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_rag(st.session_state.index, query)
        st.markdown(response)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })