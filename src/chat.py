
from dotenv import load_dotenv
from google import genai

from src.search import search_knowledge_base


# Load the API key from .env
load_dotenv()

# Create Gemini client
client = genai.Client()


def generate_answer(question):
    # Step 1: Retrieve relevant information from FAISS
    retrieved_results = search_knowledge_base(question, top_k=3)

    if not retrieved_results:
        return {
            "answer": "I could not find relevant information in the ICTU knowledge base.",
            "sources": []
        }

    # Step 2: Build the context for Gemini
    context_parts = []
    sources = []

    for number, result in enumerate(retrieved_results, start=1):
        metadata = result["metadata"]

        source_name = metadata.get("title") or metadata.get("source", "Unknown source")
        source_url = metadata.get("source_url", "")

        context_parts.append(
            f"""
Source {number}: {source_name}
Source URL: {source_url}

Information:
{result["text"]}
"""
        )

        sources.append({
        "number": number,
        "title": source_name,
        "source": metadata.get("source", ""),
        "url": source_url
    })
    context = "\n\n".join(context_parts)

    # Step 3: Tell Gemini how to answer
    prompt = f"""
You are an official ICT University student information assistant.

Answer the student's question using ONLY the information
provided in the context below.

Rules:
- Do not invent university policies, dates, fees, or procedures.
- If the context does not contain the answer, clearly say so.
- Give a clear and helpful answer in simple English.
- If information is incomplete, explain what is missing.
- Do not claim that you are an official university employee.
- Cite the supporting context using labels such as [Source 1] or [Source 2].
- Only cite a source if it supports the claim being made.

ICT UNIVERSITY KNOWLEDGE:

{context}

STUDENT QUESTION:
{question}

YOUR ANSWER:
"""

    # Step 4: Generate the answer with Gemini
    
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt
    )

    answer = interaction.output_text

    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":
    question = input("Ask ICT University Chatbot: ")

    result = generate_answer(question)

    print("\n--- CHATBOT ANSWER ---")
    print(result["answer"])

    print("\n--- SOURCES ---")
    for source in result["sources"]:
        print(f"- {source['title']}")
        if source["url"]:
            print(f"  {source['url']}")
