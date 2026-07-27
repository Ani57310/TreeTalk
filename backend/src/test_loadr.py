from src.loader import load_documents

docs = load_documents()

print(f"Loaded {len(docs)} documents\n")

for doc in docs[:5]:
    print(doc.metadata)