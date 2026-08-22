import hashlib

import streamlit as st

from langchain_community.vectorstores import Chroma
from langchain_mistralai import (
    ChatMistralAI,
    MistralAIEmbeddings
)

from config import (
    RESEARCH_CHROMA_DB_PATH,
    RESEARCH_COLLECTION_NAME,
    MISTRAL_API_KEY,
)


# ==========================================================
# LOAD EMBEDDINGS
# ==========================================================

@st.cache_resource
def load_embeddings():

    return MistralAIEmbeddings(
        api_key=MISTRAL_API_KEY
    )


# ==========================================================
# LOAD CHROMA
# ==========================================================

@st.cache_resource
def load_vectorstore():

    return Chroma(
        persist_directory=(
            RESEARCH_CHROMA_DB_PATH
        ),
        collection_name=(
            RESEARCH_COLLECTION_NAME
        ),
        embedding_function=load_embeddings()
    )


# ==========================================================
# LOAD LLM
# ==========================================================

@st.cache_resource
def load_llm():

    return ChatMistralAI(
        model="mistral-large-latest",
        temperature=0.2,
        api_key=MISTRAL_API_KEY
    )


# ==========================================================
# QUERY CLASSIFICATION
# ==========================================================

def classify_query(question):

    q = question.lower()

    # ------------------------------------------------------
    # VISUAL
    # ------------------------------------------------------

    visual_words = [
        "figure",
        "graph",
        "plot",
        "diagram",
        "image",
        "chart",
        "visual",
        "illustration"
    ]

    if any(
        word in q
        for word in visual_words
    ):

        return "visual"

    # ------------------------------------------------------
    # TABLE
    # ------------------------------------------------------

    table_words = [
        "table",
        "rows",
        "columns",
        "tabular"
    ]

    if any(
        word in q
        for word in table_words
    ):

        return "table"

    # ------------------------------------------------------
    # EQUATION
    # ------------------------------------------------------

    equation_words = [
        "equation",
        "formula",
        "calculate",
        "calculation",
        "derive",
        "derivation",
        "mathematical",
        "math"
    ]

    if any(
        word in q
        for word in equation_words
    ):

        return "equation"

    # ------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------

    summary_words = [
        "summarize",
        "summary",
        "briefing",
        "overview",
        "overall"
    ]

    if any(
        word in q
        for word in summary_words
    ):

        return "summary"

    # ------------------------------------------------------
    # DEFAULT
    # ------------------------------------------------------

    return "text"


# ==========================================================
# SINGLE FAST RETRIEVAL
# ==========================================================

def retrieve_documents(
    question,
    query_type,
    k=5
):

    vectorstore = load_vectorstore()

    # ------------------------------------------------------
    # IMPORTANT:
    # Use ONE retrieval call.
    # ------------------------------------------------------

    try:

        if query_type == "visual":

            documents = vectorstore.similarity_search(
                question,
                k=k
            )

        elif query_type == "table":

            documents = vectorstore.similarity_search(
                question,
                k=k
            )

        elif query_type == "equation":

            documents = vectorstore.similarity_search(
                question,
                k=k
            )

        elif query_type == "summary":

            # Summary needs more coverage than a
            # normal question, but still only ONE call.
            documents = vectorstore.similarity_search(
                question,
                k=10
            )

        else:

            documents = vectorstore.similarity_search(
                question,
                k=k
            )

        return documents

    except Exception as error:

        print(
            f"Retrieval error: {error}"
        )

        return []


# ==========================================================
# BUILD CONTEXT
# ==========================================================

def build_context(
    documents
):

    context_parts = []

    for document in documents:

        metadata = document.metadata

        paper_name = metadata.get(
            "paper_name",
            "Unknown paper"
        )

        page = metadata.get(
            "page",
            "Unknown"
        )

        section = metadata.get(
            "section",
            "Unknown section"
        )

        content_type = metadata.get(
            "content_type",
            "unknown"
        )

        context_parts.append(
            f"""
PAPER:
{paper_name}

SECTION:
{section}

PAGE:
{page}

CONTENT TYPE:
{content_type}

CONTENT:
{document.page_content}
"""
        )

    return "\n\n--------------------\n\n".join(
        context_parts
    )


# ==========================================================
# CACHE KEY
# ==========================================================

def create_cache_key(
    question,
    document_count
):

    raw = (
        question.strip().lower()
        + "|"
        + str(document_count)
    )

    return hashlib.md5(
        raw.encode("utf-8")
    ).hexdigest()


# ==========================================================
# ANSWER RESEARCH QUESTION
# ==========================================================

def answer_research_question(
    question,
    document_count
):

    # ======================================================
    # CACHE
    # ======================================================

    cache = st.session_state.setdefault(
        "research_answer_cache",
        {}
    )

    key = create_cache_key(
        question,
        document_count
    )

    if key in cache:

        return (
            cache[key],
            "cache"
        )

    # ======================================================
    # CLASSIFY
    # ======================================================

    query_type = classify_query(
        question
    )

    # ======================================================
    # SINGLE RETRIEVAL
    # ======================================================

    if query_type == "summary":

        documents = retrieve_documents(
            question,
            query_type,
            k=10
        )

    else:

        documents = retrieve_documents(
            question,
            query_type,
            k=5
        )

    # ======================================================
    # NO RESULTS
    # ======================================================

    if not documents:

        return (
            "I could not find relevant information "
            "in the uploaded research papers.",
            "retrieval"
        )

    # ======================================================
    # BUILD CONTEXT
    # ======================================================

    context = build_context(
        documents
    )

    # ======================================================
    # LLM
    # ======================================================

    llm = load_llm()

    prompt = f"""
You are CODEX Research Mode.

Analyze the uploaded research papers and answer
the user's question using the supplied context.

IMPORTANT RULES:

1. Use the research context as your primary source.
2. Do not invent information.
3. Do not claim something is present in the paper
   unless the context supports it.
4. Keep the answer focused on the user's question.
5. Mention the paper name, section, or page when
   useful.
6. If the available context is insufficient, say so.
7. For complex questions, combine the retrieved
   information carefully.
8. Keep the answer concise unless the user asks
   for detail.

QUERY TYPE:
{query_type}

USER QUESTION:
{question}

RELEVANT RESEARCH CONTEXT:
{context}

Now answer the user's question.
"""

    response = llm.invoke(
        prompt
    )

    answer = response.content

    # ======================================================
    # SAVE CACHE
    # ======================================================

    cache[key] = answer

    return (
        answer,
        "llm"
    )