from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR
MODELS_DIR = BASE_DIR / "models"

ME_FILE = DATA_DIR / "me.json"
DEVELOPERS_FILE = DATA_DIR / "developers.json"
PROJECT_MODEL_FILE = DATA_DIR / "project_classifier.pkl"
SPAM_MODEL_FILE = DATA_DIR / "spam_detector.pth"
SPAM_VOCAB_FILE = DATA_DIR / "vocab.pkl"

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1/")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
DB_URL = os.getenv("DB_FOR_TOOLS")
