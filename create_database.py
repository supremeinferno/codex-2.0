import os
import chromadb

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings

from config import CHROMA_DB_PATH, COLLECTION_NAME


# ==========================================================
# EMBEDDINGS
# ==========================================================

def load_embeddings():
    return MistralAIEmbeddings()


# ==========================================================
# CREATE / REPLACE VECTOR DATABASE
# ==========================================================

def create_vector_database(pdf_path: str):

    # ------------------------------------------------------
    # 1. Make sure database directory exists
    # ------------------------------------------------------

    os.makedirs(CHROMA_DB_PATH, exist_ok=True)

    # ------------------------------------------------------
    # 2. Load PDF
    # ------------------------------------------------------

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

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