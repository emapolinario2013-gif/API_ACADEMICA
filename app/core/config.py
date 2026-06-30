import os
from dotenv import load_dotenv

load_dotenv(override=True)

API_SECRET_KEY = os.getenv("API_SECRET_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "anthropic/claude-sonnet-4-6")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
AULAS_DIR = os.path.join(DATA_DIR, "aulas")
TAREFAS_DIR = os.path.join(DATA_DIR, "tarefas")
