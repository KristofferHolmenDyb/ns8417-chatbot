
import streamlit as st
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA

import unicodedata

# 🔑 Sett inn din egen OpenAI-nøkkel her
openai_api_key = "sk-din-api-nøkkel-her"

st.set_page_config(page_title="NS 8417 Chatbot 💬", layout="wide")
st.title("🤖 NS 8417 Chatbot")
st.caption("Svarer kun basert på innhold fra kontrakten NS 8417")

# 📄 Last inn tekstfil og filtrer spesialtegn
def clean_text(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

with open("ns8417_chunks.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

chunks = raw_text.split("--- CHUNK ")
documents = [Document(page_content=clean_text(chunk.strip())) for chunk in chunks if chunk.strip()]
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(documents)

# 🔍 Lag vektorsøk
vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings(openai_api_key=openai_api_key))
retriever = vectorstore.as_retriever()

# 🧠 Chatmodell
llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=openai_api_key)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 💬 UI
query = st.text_input("Still et spørsmål til kontrakten NS 8417:")
if query:
    with st.spinner("Henter svar..."):
        result = qa_chain.run(query)
        st.success(result)
