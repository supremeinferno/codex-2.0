import base64

from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    MISTRAL_API_KEY,
)


def load_embeddings():
    return MistralAIEmbeddings(
        api_key=MISTRAL_API_KEY
    )


def load_llm(response_style="⚖️ Balanced"):

    temperature = {
        "📖 Accurate": 0.0,
        "⚖️ Balanced": 0.3,
        "🎨 Creative": 0.7,
    }.get(response_style, 0.3)

    return ChatMistralAI(
        model="mistral-large-latest",
        temperature=temperature,
        api_key=MISTRAL_API_KEY,
    )


def load_vectorstore():

    return Chroma(
        persist_directory=CHROMA_DB_PATH,
        collection_name=COLLECTION_NAME,
        embedding_function=load_embeddings(),
    )


def get_retriever():

    vectorstore = load_vectorstore()

    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 8,
            "lambda_mult": 0.5,
        },
    )


STYLE_INSTRUCTIONS = {
    "📖 Accurate":
        "Be strictly factual. Do not guess.",

    "⚖️ Balanced":
        "Be clear, informative, and easy to understand.",

    "🎨 Creative":
        "Explain concepts engagingly while staying faithful to the document.",
}


LENGTH_INSTRUCTIONS = {
    "Short":
        "Answer briefly.",

    "Medium":
        "Give a clear and well-structured answer.",

    "Detailed":
        "Give a comprehensive answer using headings and bullet points.",
}


def generate_response(
    question,
    image=None,
    response_style="⚖️ Balanced",
    answer_length="Medium",
):

    retriever = get_retriever()

    docs = retriever.invoke(question)

    if not docs:
        return (
            "I could not find the answer in the document.",
            []
        )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
        if doc.page_content.strip()
    )

    if not context.strip():
        return (
            "I could not find readable text in the document.",
            docs
        )

    llm = load_llm(response_style)

    system_prompt = f"""
You are a document question-answering assistant.

Use ONLY the supplied document context.

Rules:
- Do not invent information.
- Do not use outside knowledge.
- Base the answer on the document.
- If the answer is not supported by the context, say:
  "I could not find the answer in the document."

Style:
{STYLE_INSTRUCTIONS.get(
    response_style,
    STYLE_INSTRUCTIONS["⚖️ Balanced"]
)}

Length:
{LENGTH_INSTRUCTIONS.get(
    answer_length,
    LENGTH_INSTRUCTIONS["Medium"]
)}

DOCUMENT CONTEXT:
{context}
"""

    # PDF + IMAGE
    if image is not None:

        image_base64 = base64.b64encode(
            image.getvalue()
        ).decode("utf-8")

        image_type = getattr(
            image,
            "type",
            "image/png"
        )

        messages = [
            (
                "system",
                system_prompt
            ),
            (
                "human",
                [
                    {
                        "type": "text",
                        "text": question,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:{image_type};"
                                f"base64,{image_base64}"
                            )
                        },
                    },
                ],
            ),
        ]

        response = llm.invoke(messages)

    # PDF ONLY
    else:

        prompt = f"""
{system_prompt}

QUESTION:
{question}
"""

        response = llm.invoke(prompt)

    return response.content, docs