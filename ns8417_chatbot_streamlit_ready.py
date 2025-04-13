import streamlit as st
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
import os

# 🔐 Henter API-nøkkelen fra secrets eller miljøvariabel
openai_api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="NS 8417 Chatbot 💬", layout="wide")
st.title("🤖 NS 8417 Chatbot")
st.caption("Svarer kun basert på innhold fra kontrakten NS 8417")

# 🔠 Leser og renser tekst
def clean_text(text):
    return text.encode("utf-8", "ignore").decode("utf-8")

with open("ns8417_chunks.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

chunks = raw_text.split("--- CHUNK ")
documents = [Document(page_content=clean_text(chunk.strip())) for chunk in chunks if chunk.strip()]
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(documents)

# 🔍 Oppretter vektorbasert søk
vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings(openai_api_key=openai_api_key))
retriever = vectorstore.as_retriever()

# 💬 Oppretter LLM
llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=openai_api_key)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 🧠 Brukergrensesnitt
query = st.text_input("Still et spørsmål til kontrakten NS 8417:")
if query:
    with st.spinner("Henter svar..."):
        result = qa_chain.run(query)
        st.success(result)