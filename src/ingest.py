import re

import yaml

from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Locate the project and knowledge-base folders
PROJECT_DIR = Path(__file__).resolve().parents[1]
KNOWLEDGE_BASE_DIR = PROJECT_DIR / "ictukb"

CONTENT_DIRS = [
    KNOWLEDGE_BASE_DIR / "content",
    KNOWLEDGE_BASE_DIR / "sources",
]



def load_documents():
    """Load text files and extract YAML frontmatter as metadata."""

    documents = []

    for folder in CONTENT_DIRS:
        if not folder.exists():
            print(f"Folder not found: {folder}")
            continue

        for file_path in folder.rglob("*"):
            if file_path.suffix.lower() not in [".md", ".txt"]:
                continue

            try:
                raw_text = file_path.read_text(
                    encoding="utf-8",
                    errors="replace"
                )

                if not raw_text.strip():
                    continue

                frontmatter = {}

                # Extract YAML frontmatter from Markdown files
                match = re.match(
                    r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z",
                    raw_text,
                    flags=re.DOTALL
                )

                if match:
                    frontmatter = yaml.safe_load(match.group(1)) or {}
                    raw_text = match.group(2)

                if not raw_text.strip():
                    continue

                metadata = {
                    "source": str(
                        file_path.relative_to(KNOWLEDGE_BASE_DIR)
                    ),
                    "title": str(frontmatter.get("title") or ""),
                    "category": str(frontmatter.get("category") or ""),
                    "source_type": str(
                        frontmatter.get("source_type") or ""
                    ),
                    "source_url": str(
                        frontmatter.get("source_url") or ""
                    ),
                }

                document = Document(
                    page_content=raw_text.strip(),
                    metadata=metadata
                )

                documents.append(document)

            except Exception as error:
                print(f"Could not read {file_path}: {error}")

    return documents


def split_documents(documents):
    """Split documents into smaller chunks for retrieval."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Text chunks created: {len(chunks)}")

    if chunks:
        print("\nExample source:")
        print(chunks[0].metadata["source"])

        print("\nExample chunk:")
        print(chunks[0].page_content[:500])
