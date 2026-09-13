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
    def test_prompt_requires_plain_and_direct_answer_formatting(self):
        self.assertIn("Use plain text only", chatbot.SYSTEM_PROMPT)
        self.assertIn("Write scientific names as ordinary text", chatbot.SYSTEM_PROMPT)
        self.assertIn('use flat "- " bullets only', chatbot.SYSTEM_PROMPT)
        self.assertIn("answer in one complete sentence", chatbot.SYSTEM_PROMPT)
        self.assertIn("During the [stage], irrigate [tree] plants [frequency]", chatbot.SYSTEM_PROMPT)
        self.assertIn("provide at most three distinct benefits", chatbot.SYSTEM_PROMPT)

    def test_answer_format_normalization_keeps_plain_text_and_values(self):
        answer = chatbot.normalize_answer_format(
            "**4 m × 4 m**\n* Use _Hyblaea puera_ control measures."
        )

        self.assertEqual(
            answer,
            "4 m × 4 m\n- Use Hyblaea puera control measures.",
        )

    def test_tamil_common_name_maps_to_corpus_species_name(self):
        self.assertEqual(
            chatbot.normalize_tamil_query_terms(
                "What is the recommended spacing for a Punnai tree?"
            ),
            "What is the recommended spacing for a Calophyllum inophyllum tree?",
        )

    def test_tamil_translation_preparation_preserves_two_week_interval(self):
        self.assertEqual(
            chatbot.prepare_answer_for_tamil_translation(
                "Spray at fortnightly intervals."
            ),
            "Spray once every two weeks.",
        )

    @patch("src.chatbot.translate_text", side_effect=lambda text, *_: f"TA:{text}")
    def test_tamil_bullet_answers_are_translated_line_by_line(self, mock_translate):
        translated = chatbot.translate_answer_to_tamil(
            "Casuarina trees have these benefits:\n\n- Fix nitrogen.\n- Tolerate salt-laden winds."
        )

        self.assertEqual(
            translated,
            "TA:Casuarina trees have these benefits:\n- TA:Fix nitrogen.\n- TA:Tolerate salt-laden winds.",
        )
        self.assertEqual(mock_translate.call_count, 3)

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
