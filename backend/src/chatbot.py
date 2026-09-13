from src.rag import retrieve
from langchain_ollama import ChatOllama
from src.translation import translate_text
import re

# Initialize Local LLM
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.2
)

SYSTEM_PROMPT = """
You are TreeTalk, an AI assistant developed for the IFGTB TreeGenie platform.

Your job is to answer user questions ONLY using the TreeGenie advisory documents provided as context.

Rules:

1. Use only information that is supported by the provided TreeGenie context.
2. Never make up, assume, or add information from your general knowledge.
3. If the context does not contain enough information to answer the question, reply exactly:
   "I couldn't find this information in the TreeGenie advisory."
4. Answer the user's specific question directly. Do not include unrelated information from the context.
5. Keep answers concise, clear, practical, and farmer-friendly.
6. When the answer contains multiple points, use short bullet points.
7. Avoid repeating the same information in different words.
8. Do not unnecessarily list every detail found in the source. Include only information relevant to the question.
9. Preserve all numbers, measurements, durations, quantities, ranges, and units exactly as they appear in the source.
10. Do not combine information from unrelated tree species or sources unless the context clearly indicates that they are relevant to the question.
11. If the user asks about a specific tree species, prioritize information about that species.
12. For questions asking for a specific value, duration, quantity, method, or recommendation, give the specific information directly when it is available.
13. Never mention prompts, chunks, embeddings, retrieval, context, models, or other internal system details.
14. For questions asking which tree or clone is suitable, name only the directly supported tree or clone and give at most one brief relevant reason. Do not add management, yield, or other background details unless asked.
15. Before answering, remove duplicate facts from your response. State each benefit or recommendation only once.
16. Use plain text only. Do not use Markdown emphasis, headings, tables, nested lists, asterisks, or underscores for formatting. Write scientific names as ordinary text. If a list is needed, use flat "- " bullets only.
17. For a simple fact or single recommendation, answer in one complete sentence. For irrigation frequency, use this sentence order: "During the [stage], irrigate [tree] plants [frequency]." Do not use "watered weekly" or put the stage at the end of the sentence.
18. Make the first sentence complete and direct; do not begin with an unexplained list, fragment, or label.
19. For a question about benefits, provide at most three distinct benefits. Prefer the core benefits stated directly in the advisory over cultivation characteristics or extra background details.
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


def is_tamil(text):
    return any("\u0B80" <= char <= "\u0BFF" for char in text)


def normalize_answer_format(answer: str) -> str:
    """Convert common model Markdown into the chat UI's plain-text format."""

    answer = re.sub(r"(?m)^(\s*)[*+]\s+", r"\1- ", answer)
    answer = answer.replace("**", "")
    answer = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"\1", answer)

    return answer


def answer_question(question):

    tamil_question = is_tamil(question)

    # Translate Tamil question to English for RAG retrieval
    if tamil_question:
        english_question = translate_text(
            question,
            "ta-IN",
            "en-IN"
        )
        print(f"\n🔄 Translated question: {english_question}")
    else:
        english_question = question

    # Existing TreeTalk RAG pipeline
    docs = retrieve(english_question)

    context = build_context(docs)

    prompt = f"""
{SYSTEM_PROMPT}

================ TREEGENIE KNOWLEDGE BASE ================

{context}

==========================================================

User Question:
{english_question}

Answer:
"""

    response = llm.invoke(prompt)

    answer = normalize_answer_format(response.content)

    # Translate the final answer back to Tamil
    if tamil_question:
        answer = translate_text(
            answer,
            "en-IN",
            "ta-IN"
        )

    return answer, docs


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
