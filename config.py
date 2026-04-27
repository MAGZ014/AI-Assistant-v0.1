import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

BASE_DIR = Path(__file__).parent
# ---------------{IA}------------------------
# --- Groq ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")  # o mixtral-8x7b-32768

# --- LM Studio (corre local en puerto 1234) ---
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL")
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL")  # el que tengas cargado

# --- Preferencia de LLM ---
# "groq" para tareas complejas, "local" para charla rápida
DEFAULT_LLM = "groq"

#---------------{Tools}-------------------
# --- Carpeta de trabajo de documentos ---
DOCS_FOLDER = BASE_DIR / "documentos"
# --- Clima ---
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
# --- Voz ---
VOICE_ENABLED = True
# --- Piper ---
PIPER_DIR   = BASE_DIR / "piper"
PIPER_EXE   = PIPER_DIR / "piper.exe"
VOICE_MODEL = PIPER_DIR / "voices" / "es_MX-claude-high.onnx"
