import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

DOCS_FOLDER = os.getenv("DOCS_FOLDER", "docs")

if not os.path.exists(DOCS_FOLDER):
    os.makedirs(DOCS_FOLDER)