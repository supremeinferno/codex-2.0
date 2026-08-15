import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHROMA_DB_PATH = os.path.join(
    BASE_DIR,
    "chroma_db"
)

COLLECTION_NAME = "codex_documents"

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")