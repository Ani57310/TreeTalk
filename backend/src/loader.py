from pathlib import Path
from langchain_core.documents import Document

# Root data folder


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_documents():
    """
    Loads all markdown files from the data directory
    and attaches metadata to each document.
    """

    documents = []

    # Walk through every subfolder
    for category_folder in DATA_DIR.iterdir():

        if not category_folder.is_dir():
            continue

        category = category_folder.name

        for md_file in category_folder.glob("*.md"):

            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            tree_name = md_file.stem.replace("-", " ").title()

            doc = Document(
                page_content=content,
                metadata={
                    "tree": tree_name,
                    "category": category,
                    "file": md_file.name,
                    "source": str(md_file),
                }
            )

            documents.append(doc)

    return documents