from pathlib import Path
from functools import lru_cache

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


@lru_cache(maxsize=1)
def get_embeddings():
    """
    Load the embedding model only when it is actually needed.

    The @lru_cache ensures the model is loaded only once
    and then reused for subsequent requests.
    """

    print("\n🌱 Loading TreeTalk embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("✅ Embedding model loaded.")

    return embeddings


@lru_cache(maxsize=1)
def get_vectorstore():
    """
    Create the Chroma vector store using the cached
    embedding model.
    """

    print("🌳 Connecting to TreeTalk knowledge base...")

    vectorstore = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=get_embeddings(),
    )

    print("✅ Knowledge base connected.")

    return vectorstore


@lru_cache(maxsize=1)
def get_retriever():
    """
    Create and cache the TreeTalk retriever.
    """

    vectorstore = get_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 10,
        },
    )

    return retriever


def retrieve(query: str):
    """
    Retrieve relevant TreeGenie documents for a query.

    RAG components are loaded lazily on the first request
    and reused afterwards.
    """

    retriever = get_retriever()

    return retriever.invoke(query)