
import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


PROJECT_DIR = Path(__file__).resolve().parents[1]
VECTORSTORE_DIR = PROJECT_DIR / "vectorstore"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def search_knowledge_base(question, top_k=3):
    index_path = VECTORSTORE_DIR / "ictu.index"
    documents_path = VECTORSTORE_DIR / "documents.json"

    index = faiss.read_index(str(index_path))

    with documents_path.open("r", encoding="utf-8") as file:
        documents = json.load(file)

    model = SentenceTransformer(MODEL_NAME)

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue

        results.append({
            "score": float(score),
            "text": documents[idx]["text"],
            "metadata": documents[idx]["metadata"]
        })

    return results


if __name__ == "__main__":
    question = input("Ask an ICT University question: ")

    results = search_knowledge_base(question)

    print("\n--- Retrieved information ---")

    for number, result in enumerate(results, start=1):
        print(f"\nResult {number}")
        print(f"Similarity score: {result['score']:.4f}")
        print(f"Source: {result['metadata']['source']}")
        print(result["text"])
