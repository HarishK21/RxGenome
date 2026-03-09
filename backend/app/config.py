"""Backend configuration."""

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rxgenome.db")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_STRONG_MODEL = os.getenv("GEMINI_STRONG_MODEL", "gemini-2.5-pro-preview-06-05")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(os.path.dirname(__file__), "..", "uploads"))
ML_ARTIFACT_DIR = os.getenv("ML_ARTIFACT_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "ml", "artifacts"))
PGX_RULES_PATH = os.getenv("PGX_RULES_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "data", "pgx_rules.json"))
DEMO_DATA_DIR = os.getenv("DEMO_DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "data", "demo"))
default_cors_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]
cors_origins_env = os.getenv("CORS_ORIGINS", "")
CORS_ORIGINS = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()] or default_cors_origins
CORS_ORIGIN_REGEX = os.getenv("CORS_ORIGIN_REGEX", r"https?://(localhost|127\.0\.0\.1)(:\d+)?$")

os.makedirs(UPLOAD_DIR, exist_ok=True)
