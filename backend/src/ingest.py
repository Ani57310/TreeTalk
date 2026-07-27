import os
import shutil
from pathlib import Path

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.loader import load_documents

# -------------------------------
# Project paths
# -------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = BASE_DIR / "chroma"

# -------------------------------
# Load environment variables
# -------------------------------

load_dotenv(BASE_DIR / ".env")

# -------------------------------
# Delete old database
# -------------------------------

if CHROMA_DIR.exists():
    shutil.rmtree(CHROMA_DIR)

print("Loading documents...")
documents = load_documents()

print(f"Loaded {len(documents)} documents.")

# -------------------------------
# Split documents
# -------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks.")

# -------------------------------
# Embeddings
# -------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# -------------------------------
# Create Chroma Database
# -------------------------------

print("Creating vector database...")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(CHROMA_DIR)
)

print("Done!")
print(f"Stored {len(chunks)} chunks in ChromaDB.")