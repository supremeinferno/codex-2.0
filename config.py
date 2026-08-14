import os
import tempfile

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# ChromaDB location
CHROMA_DB_PATH = os.path.join(
    tempfile.gettempdir(),
    "chroma_db"
)


# Mistral API key
MISTRAL_API_KEY = os.getenv(
    "MISTRAL_API_KEY"
)