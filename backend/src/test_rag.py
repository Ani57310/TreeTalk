from src.rag import retrieve

query = input("Ask a question: ")

docs = retrieve(query)

print("\n" + "=" * 80)

for i, doc in enumerate(docs, 1):

    print(f"\nResult {i}")
    print("-" * 80)

    print("Metadata:")
    print(doc.metadata)

    print("\nContent:")
    print(doc.page_content[:700])

    print("\n")