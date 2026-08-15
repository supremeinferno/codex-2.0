import base64

from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import (
    ChatMistralAI,
    MistralAIEmbeddings
)

from config import CHROMA_DB_PATH, COLLECTION_NAME


# ==========================================================
# EMBEDDINGS
# ==========================================================

def load_embeddings():

    return MistralAIEmbeddings()


# ==========================================================
# LLM
# ==========================================================

def load_llm(response_style: str):

    temperature = {

        "📖 Accurate": 0.0,

        "⚖️ Balanced": 0.3,

        "🎨 Creative": 0.8

    }.get(response_style, 0.3)

    return ChatMistralAI(
        model="mistral-large-latest",
        temperature=temperature
    )


# ==========================================================
# VECTOR STORE
# ==========================================================

def load_vectorstore():

    embeddings = load_embeddings()

    return Chroma(
        persist_directory=CHROMA_DB_PATH,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )


# ==========================================================
# RETRIEVER
# ==========================================================

def get_retriever():

    vectorstore = load_vectorstore()

    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 10,
            "lambda_mult": 0.5
        }
    )


# ==========================================================
# RESPONSE STYLE
# ==========================================================

STYLE_INSTRUCTIONS = {

    "📖 Accurate":
        "Be strictly factual. Never guess.",

    "⚖️ Balanced":
        "Be clear, informative and easy to understand.",

    "🎨 Creative":
        "Explain concepts in an engaging way while remaining faithful to the document."
}


# ==========================================================
# ANSWER LENGTH
# ==========================================================

LENGTH_INSTRUCTIONS = {

    "Short":
        "Answer briefly.",

    "Medium":
        "Provide a well-structured explanation.",

    "Detailed":
        "Provide a comprehensive explanation using headings and bullet points."
}


# ==========================================================
# RESPONSE GENERATOR
# ==========================================================

def generate_response(
    question,
    image=None,
    response_style="⚖️ Balanced",
    answer_length="Medium"
):

    # ------------------------------------------------------
    # Retrieve relevant documents
    # ------------------------------------------------------

    retriever = get_retriever()

    docs = retriever.invoke(question)

    # ------------------------------------------------------
    # Build context
    # ------------------------------------------------------

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # ------------------------------------------------------
    # Load LLM
    # ------------------------------------------------------

    llm = load_llm(response_style)

    # ======================================================
    # IMAGE + PDF
    # ======================================================

    if image:

        img64 = base64.b64encode(
            image.getvalue()
        ).decode()

        messages = [

            (
                "system",

                f"""
You are an expert multimodal AI assistant.

Use the supplied PDF context as the primary source.

Use the uploaded image only when it helps answer
the question.

Never invent information.

If the answer cannot be found in the PDF context,
say:

"I could not find the answer in the document."

Response Style:

{STYLE_INSTRUCTIONS[response_style]}

Answer Length:

{LENGTH_INSTRUCTIONS[answer_length]}

PDF Context:

{context}
"""
            ),

            (
                "human",

                [
                    {
                        "type": "text",
                        "text": question
                    },

                    {
                        "type": "image_url",

                        "image_url": {

                            "url":
                            f"data:{image.type};base64,{img64}"

                        }
                    }
                ]
            )
        ]

        response = llm.invoke(messages)

    # ======================================================
    # PDF ONLY
    # ======================================================

    else:

        prompt = ChatPromptTemplate.from_messages(

            [

                (
                    "system",

                    f"""
You are an expert AI assistant.

Use ONLY the supplied PDF context.

{STYLE_INSTRUCTIONS[response_style]}

{LENGTH_INSTRUCTIONS[answer_length]}

Never invent information.

If the answer cannot be found in the document,
reply:

"I could not find the answer in the document."
"""
                ),

                (
                    "human",

                    """
Context:

{context}

Question:

{question}
"""
                )

            ]
        )

        final_prompt = prompt.invoke(

            {
                "context": context,
                "question": question
            }
        )

        response = llm.invoke(final_prompt)

    return response.content, docs