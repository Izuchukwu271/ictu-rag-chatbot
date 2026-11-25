
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
            "answer": (
                "I could not find relevant information "
                "in the ICTU knowledge base."
            ),
            "sources": []
        }

    # Step 2: Build context and remove duplicate sources
    context_parts = []
    sources = []
    source_numbers = {}

    for result in retrieved_results:
        metadata = result["metadata"]

        source_name = (
            metadata.get("title")
            or metadata.get("source")
            or "Unknown source"
        )

        source_path = metadata.get("source", "")
        source_url = metadata.get("source_url", "")

        # Identify the document so repeated chunks
        # from the same file share one source number.
        source_key = (
            source_path.lower().replace("\\", "/")
            if source_path
            else source_url or source_name
        )

        if source_key not in source_numbers:
            source_number = len(sources) + 1
            source_numbers[source_key] = source_number

            sources.append({
                "number": source_number,
                "title": source_name,
                "source": source_path,
                "url": source_url
            })

        source_number = source_numbers[source_key]

        # Add the retrieved chunk to Gemini's context
        context_parts.append(
            f"""
Source {source_number}: {source_name}
File: {source_path}
Source URL: {source_url}

Information:
{result["text"]}
"""
        )

    context = "\n\n".join(context_parts)

    # Step 3: Give Gemini clear citation instructions
    prompt = f"""
You are an AI assistant that helps students understand
ICT University information.

Answer the student's question using ONLY the information
provided in the knowledge context below.

Rules:
- Do not invent university policies, dates, fees,
  requirements, or procedures.
- If the context does not contain the answer,
  clearly say that the information was not found.
- Answer in clear and helpful simple English.
- If information is incomplete, explain what is missing.
- Do not claim to be a university employee.
- Cite factual claims using the source numbers provided,
  for example [Source 1].
- Place citations directly beside the claims they support.
- Use only source numbers that appear in the context.
- A source must directly support the claim being cited.
- Do not cite a document just because it is related
  to the general topic.
- If multiple sources support a claim, cite them together.
- Do not make up source titles or source numbers.

KNOWLEDGE CONTEXT:

{context}

STUDENT QUESTION:
{question}

ANSWER:
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
        print(f"- Source {source['number']}: {source['title']}")
        print(f"  File: {source['source']}")

        if source["url"]:
            print(f"  URL: {source['url']}")
