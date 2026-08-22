import os
import tempfile
from dotenv import load_dotenv

load_dotenv(override=True)

CHROMA_DB_PATH = os.path.join(
    tempfile.gettempdir(),
    "chroma_db"
)

COLLECTION_NAME = "codex_documents"

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "").strip()

if not MISTRAL_API_KEY:
    raise RuntimeError("MISTRAL_API_KEY is missing")

import os
import tempfile

RESEARCH_CHROMA_DB_PATH = os.path.join(
    tempfile.gettempdir(),
    "codex_research_db"
)

RESEARCH_COLLECTION_NAME = (
    "codex_research"
)