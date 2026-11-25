
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from ingest import load_documents, split_documents


PROJECT_DIR = Path(__file__).resolve().parents[1]
VECTORSTORE_DIR = PROJECT_DIR / "vectorstore"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def build_index():
    print("Loading university documents...")

    documents = load_documents()
    chunks = split_documents(documents)

    if not chunks:
        print("No document chunks found.")
        return

    print(f"Chunks to embed: {len(chunks)}")

    print("Loading multilingual embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk.page_content for chunk in chunks]

    print("Converting text into embeddings...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    print("Creating FAISS index...")
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    index_path = VECTORSTORE_DIR / "ictu.index"
    documents_path = VECTORSTORE_DIR / "documents.json"

    faiss.write_index(index, str(index_path))

    saved_chunks = []

    for chunk in chunks:
        saved_chunks.append({
            "text": chunk.page_content,
            "metadata": chunk.metadata
        })

    with documents_path.open("w", encoding="utf-8") as file:
        json.dump(
            saved_chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\nVector index created successfully!")
    print(f"Vectors stored: {index.ntotal}")
    print(f"Embedding dimensions: {dimension}")
    print(f"Index location: {index_path}")


if __name__ == "__main__":
    build_index()
