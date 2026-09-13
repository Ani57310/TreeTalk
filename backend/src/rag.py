from pathlib import Path
from functools import lru_cache
import re

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# Generic words in source labels should not make a source appear focused.  For
# example, a question about "trees" should not select "Windbreak Tree
# Varieties" merely because both contain the word "tree".
SOURCE_FOCUS_STOPWORDS = {
    "and",
    "disease",
    "of",
    "pest",
    "the",
    "tree",
    "trees",
    "variety",
    "varieties",
}


def _meaningful_words(text: str) -> set[str]:
    """Return normalized, non-generic words used to match a source label."""

    words = re.findall(r"[a-z]+", text.lower())

    return {
        word[:-1] if word.endswith("s") and len(word) > 3 else word
        for word in words
        if word not in SOURCE_FOCUS_STOPWORDS
    }


def filter_documents_by_query_focus(query: str, documents):
    """
    Keep source groups explicitly named by the query when they are present.

    MMR still supplies the initial candidates.  This small post-retrieval step
    only removes an unrelated source when a meaningful word from a retrieved
    source label (for example, "Casuarina" or "Windbreak") is also present in
    the query.  If no source label matches, all retrieved documents are kept.
    """

    query_words = _meaningful_words(query)
    focused_sources = {
        doc.metadata.get("file")
        for doc in documents
        if query_words & _meaningful_words(doc.metadata.get("tree", ""))
    }

    if not focused_sources:
        return documents

    return [
        doc
        for doc in documents
        if doc.metadata.get("file") in focused_sources
    ]


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

    documents = retriever.invoke(query)

    return filter_documents_by_query_focus(query, documents)
