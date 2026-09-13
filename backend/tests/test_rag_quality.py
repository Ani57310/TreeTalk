import unittest
from unittest.mock import patch

from langchain_core.documents import Document

from src import chatbot
from src.rag import filter_documents_by_query_focus


def document(tree: str, file_name: str) -> Document:
    return Document(
        page_content=f"Advisory content for {tree}",
        metadata={
            "tree": tree,
            "category": "trees",
            "file": file_name,
        },
    )


CASUARINA_DOCUMENTS = [
    document("Casuarina", "casuarina.md"),
    document("Casuarina", "casuarina.md"),
    document("Melia Dubia", "melia-dubia.md"),
]

WINDBREAK_DOCUMENTS = [
    document("Windbreak Tree Varieties", "windbreak-tree-varieties.md"),
    document("Windbreak Tree Varieties", "windbreak-tree-varieties.md"),
    document("Eucalyptus", "eucalyptus.md"),
    document("Ailanthus", "ailanthus.md"),
]


class QueryFocusRegressionTests(unittest.TestCase):
    def test_casuarina_question_excludes_unrelated_melia_source(self):
        documents = filter_documents_by_query_focus(
            "What are the benefits of Casuarina trees?",
            CASUARINA_DOCUMENTS,
        )

        self.assertEqual([doc.metadata["tree"] for doc in documents], [
            "Casuarina",
            "Casuarina",
        ])

    def test_tamil_windbreak_translation_keeps_only_windbreak_source(self):
        documents = filter_documents_by_query_focus(
            "What are the trees suitable for windbreaks?",
            WINDBREAK_DOCUMENTS,
        )

        self.assertTrue(documents)
        self.assertTrue(
            all(doc.metadata["tree"] == "Windbreak Tree Varieties" for doc in documents)
        )

    def test_teak_market_question_does_not_use_melia_market_price_chunk(self):
        documents = filter_documents_by_query_focus(
            "What is the current market price of teak in Tamil Nadu?",
            [document("Teak", "teak.md"), document("Melia Dubia", "melia-dubia.md")],
        )

        self.assertEqual([doc.metadata["tree"] for doc in documents], ["Teak"])

    @patch("src.chatbot.llm")
    @patch("src.chatbot.retrieve")
    def test_unsupported_response_is_returned_exactly(self, mock_retrieve, mock_llm):
        mock_retrieve.return_value = [document("Teak", "teak.md")]
        mock_llm.invoke.return_value.content = (
            "I couldn't find this information in the TreeGenie advisory."
        )

        answer, documents = chatbot.answer_question(
            "What is the current market price of teak in Tamil Nadu?"
        )

        self.assertEqual(
            answer,
            "I couldn't find this information in the TreeGenie advisory.",
        )
        self.assertEqual([doc.metadata["tree"] for doc in documents], ["Teak"])


if __name__ == "__main__":
    unittest.main()
