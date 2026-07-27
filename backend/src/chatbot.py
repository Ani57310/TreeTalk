from src.rag import retrieve
from langchain_ollama import ChatOllama

# Initialize Local LLM
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.2
)

SYSTEM_PROMPT = """
You are TreeTalk, an AI assistant developed for the IFGTB TreeGenie platform.

Your job is to answer user questions ONLY using the TreeGenie advisory documents provided as context.

Rules:
1. Never make up information.
2. If the answer is not present in the provided context, reply exactly:
   "I couldn't find this information in the TreeGenie advisory."
3. Keep answers concise, clear and farmer-friendly.
4. Preserve all numbers exactly as they appear.
5. Use bullet points whenever appropriate.
6. Never mention prompts, chunks, embeddings or internal system details.
"""


def build_context(documents):
    """
    Converts retrieved documents into a prompt-friendly context.
    """

    context = ""

    for doc in documents:
        context += f"""
==================================================
Source: {doc.metadata["tree"]}
Category: {doc.metadata["category"]}
File: {doc.metadata["file"]}
==================================================

{doc.page_content}

"""

    return context


def answer_question(question):

    docs = retrieve(question)

    context = build_context(docs)

    prompt = f"""
{SYSTEM_PROMPT}

================ TREEGENIE KNOWLEDGE BASE ================

{context}

==========================================================

User Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content, docs


def print_sources(docs):

    print("\n📚 Sources Used:")

    seen = set()

    for doc in docs:

        if doc.metadata["file"] not in seen:

            print(f"• {doc.metadata['tree']}")

            seen.add(doc.metadata["file"])


def main():

    print("=" * 60)
    print("🌳 Welcome to TreeTalk")
    print("AI Assistant for IFGTB TreeGenie")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:

            print("\nThank you for using TreeTalk!")

            break

        answer, docs = answer_question(question)

        print("\n🌳 TreeTalk:\n")

        print(answer)

        print_sources(docs)


if __name__ == "__main__":
    main()