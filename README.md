\# ICTU RAG Chatbot



A Retrieval-Augmented Generation (RAG) chatbot designed to answer student questions about ICT University using university knowledge sources.



\## Project Goal



The goal of this project is to help students find information about ICT University, including:



\- Admissions and registration

\- Academic programs

\- Fees and payments

\- Academic regulations

\- University services and contacts



The chatbot will retrieve relevant information from university documents before generating an answer.



\## Technology Stack



\- Python

\- Streamlit

\- LangChain

\- Sentence Transformers

\- FAISS

\- PyPDF

\- python-docx



\## How RAG Works



1\. Load university documents.

2\. Split the documents into smaller text chunks.

3\. Convert chunks into embeddings.

4\. Store embeddings in a FAISS vector index.

5\. Retrieve relevant chunks for a student's question.

6\. Generate an answer grounded in the retrieved information.



\## Project Status



Currently setting up the document ingestion and retrieval pipeline.



\## Disclaimer



This is an academic student project. Answers depend on the availability, accuracy, and freshness of the university information sources used.

