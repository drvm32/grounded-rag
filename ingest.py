import os
import time
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def load_documents(data_dir="data"):
    loader = DirectoryLoader(
        data_dir,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} documents")
    return documents

def chunk_documents(documents, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks

def embed_and_store(chunks, persist_dir="chroma_db", batch_size=50, delay_seconds=35):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = Chroma(embedding_function=embeddings, persist_directory=persist_dir)

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        vectorstore.add_documents(batch)
        print(f"Embedded and stored chunks {i + 1}-{i + len(batch)} of {len(chunks)}")
        if i + batch_size < len(chunks):
            time.sleep(delay_seconds)

    print(f"Stored {len(chunks)} chunks in Chroma at '{persist_dir}'")
    return vectorstore

if __name__ == "__main__":
    documents = load_documents()
    chunks = chunk_documents(documents)
    embed_and_store(chunks)