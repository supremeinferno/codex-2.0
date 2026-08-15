import io
import os

import chromadb
from pypdf import PdfReader

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    MISTRAL_API_KEY,
)


# ==========================================================
# EMBEDDINGS
# ==========================================================

def load_embeddings():
    return MistralAIEmbeddings(
        api_key=MISTRAL_API_KEY
    )


# ==========================================================
# MINIMUM CHARACTERS BEFORE A PAGE IS CONSIDERED "EMPTY"
# ==========================================================

MIN_PAGE_TEXT_CHARS = 30


# ==========================================================
# EXTRACT ACROFORM FIELD VALUES (fillable PDF forms)
# ==========================================================

def _extract_form_fields(pdf_path: str) -> str:

    try:
        reader = PdfReader(pdf_path)
        fields = reader.get_fields()
    except Exception:
        return ""

    if not fields:
        return ""

    lines = []

    for name, field in fields.items():

        value = field.get("/V") if field else None

        if value is None:
            continue

        value = str(value).strip()

        if not value:
            continue

        label = str(name).strip()

        lines.append(f"{label}: {value}")

    return "\n".join(lines)


# ==========================================================
# OCR FALLBACK FOR SCANNED / IMAGE-ONLY PAGES
# ==========================================================

def _ocr_page(pdf_path: str, page_number: int) -> str:
    """
    page_number is 0-indexed to match PyPDFLoader's page metadata.
    Only imports pdf2image/pytesseract when actually needed, so
    environments without poppler/tesseract installed still work
    for normal text PDFs.
    """

    try:
        from pdf2image import convert_from_path
        import pytesseract
    except ImportError:
        return ""

    try:
        images = convert_from_path(
            pdf_path,
            first_page=page_number + 1,
            last_page=page_number + 1,
        )

        if not images:
            return ""

        return pytesseract.image_to_string(images[0]).strip()

    except Exception:
        return ""


# ==========================================================
# LOAD PDF WITH FALLBACKS
# ==========================================================

def _load_documents_with_fallback(pdf_path: str):

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Form-field values apply to the whole PDF, not one page,
    # so only pull them once and only if needed.
    form_text_cache = None

    repaired_documents = []

    for doc in documents:

        text = (doc.page_content or "").strip()

        if len(text) >= MIN_PAGE_TEXT_CHARS:
            repaired_documents.append(doc)
            continue

        # --- Page text is too short: try form fields first ---

        if form_text_cache is None:
            form_text_cache = _extract_form_fields(pdf_path)

        if form_text_cache:
            merged = (text + "\n\n" + form_text_cache).strip()

            repaired_documents.append(
                Document(
                    page_content=merged,
                    metadata=doc.metadata,
                )
            )
            continue

        # --- No form fields: try OCR (scanned page) ---

        page_number = doc.metadata.get("page", 0)
        ocr_text = _ocr_page(pdf_path, page_number)

        if ocr_text:
            repaired_documents.append(
                Document(
                    page_content=ocr_text,
                    metadata=doc.metadata,
                )
            )
            continue

        # --- Still nothing: keep the (possibly empty) original ---
        repaired_documents.append(doc)

    return repaired_documents


# ==========================================================
# CREATE / REPLACE VECTOR DATABASE
# ==========================================================

def create_vector_database(pdf_path: str):

    # ------------------------------------------------------
    # 1. Make sure database directory exists
    # ------------------------------------------------------

    os.makedirs(CHROMA_DB_PATH, exist_ok=True)

    # ------------------------------------------------------
    # 2. Load PDF (with form-field / OCR fallback)
    # ------------------------------------------------------

    documents = _load_documents_with_fallback(pdf_path)

    # ------------------------------------------------------
    # 2b. Bail out early with a clear error if there is
    #     still no usable text — instead of silently
    #     building an empty / useless vector database.
    # ------------------------------------------------------

    total_chars = sum(
        len((doc.page_content or "").strip())
        for doc in documents
    )

    if total_chars < MIN_PAGE_TEXT_CHARS:
        raise ValueError(
            "No readable text could be extracted from this PDF. "
            "It may be a scanned document (install pdf2image + "
            "pytesseract, plus the poppler and tesseract system "
            "packages, to enable OCR) or a fillable form whose "
            "fields could not be read."
        )

    # ------------------------------------------------------
    # 3. Split PDF into chunks
    # ------------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300
    )

    chunks = splitter.split_documents(documents)

    # ------------------------------------------------------
    # 4. Load embedding model
    # ------------------------------------------------------

    embedding_model = load_embeddings()

    # ------------------------------------------------------
    # 5. Open persistent Chroma client
    # ------------------------------------------------------

    client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH
    )

    # ------------------------------------------------------
    # 6. Delete OLD collection
    #
    # IMPORTANT:
    # We delete the collection, NOT the whole folder.
    # This prevents SQLite readonly / locked database errors.
    # ------------------------------------------------------

    try:

        client.delete_collection(
            name=COLLECTION_NAME
        )

    except Exception:
        # Collection doesn't exist yet
        pass

    # ------------------------------------------------------
    # 7. Create fresh Chroma collection
    # ------------------------------------------------------

    vectorstore = Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model
    )

    # ------------------------------------------------------
    # 8. Add new PDF chunks
    # ------------------------------------------------------

    vectorstore.add_documents(chunks)

    # ------------------------------------------------------
    # 9. Return information to UI
    # ------------------------------------------------------

    return len(documents), len(chunks)