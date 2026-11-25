
import streamlit as st

from src.chat import generate_answer


st.set_page_config(
    page_title="ICTU Student Assistant",
    page_icon="assets/ictlogo.png",
    layout="centered"
)


col1, col2 = st.columns([1, 5])

with col1:
    st.image("assets/ictlogo.png", width=75)

with col2:
    st.title("ICT University Assistant")


st.caption(
    "Ask questions about ICT University using information "
    "from the university knowledge base."
)

st.info(
    "This assistant uses university documents to answer questions. "
    "Always confirm important or time-sensitive information "
    "with the university."
)

# Store the conversation during the user's session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display sources for assistant messages
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    source_number = source.get("number", "")
                    title = source.get("title", "University document")
                    path = source.get("source", "")
                    url = source.get("url", "")

                    st.markdown(
                        f"**Source {source_number}: {title}**"
                    )

                    if path:
                        st.caption(f"File: {path}")

                    if url:
                        st.markdown(f"[Open source document]({url})")

# Accept a new question
question = st.chat_input(
    "Ask a question about ICT University..."
)

if question:
    # Display and save the student's question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate the answer
    with st.chat_message("assistant"):
        with st.spinner("Searching university information..."):
            try:
                result = generate_answer(question)

                answer = result["answer"]
                sources = result["sources"]

                st.markdown(answer)

                if sources:
                    with st.expander("📚 Sources"):
                        for source in sources:
                            source_number = source.get("number", "")
                            title = source.get(
                                "title",
                                "University document"
                            )
                            path = source.get("source", "")
                            url = source.get("url", "")

                            st.markdown(
                                f"**Source {source_number}: {title}**"
                            )

                            if path:
                                st.caption(f"File: {path}")

                            if url:
                                st.markdown(
                                    f"[Open source document]({url})"
                                )

                # Save answer and sources
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception:
                st.error(
                    "The chatbot could not generate an answer right now. "
                    "Please try again in a moment."
                )
