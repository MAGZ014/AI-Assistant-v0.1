# tts.py
import subprocess
import tempfile
import os
from playsound import playsound
from config import PIPER_EXE, VOICE_MODEL


def speak_piper(text: str):
    if not text or not text.strip():
        return

    text = _clean_text(text)

    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        subprocess.run(
        [str(PIPER_EXE), "--model", str(VOICE_MODEL), "--output_file", tmp_path],
            input=text.encode("utf-8"),
            capture_output=True,
            timeout=15
        )

        playsound(tmp_path)
        os.unlink(tmp_path)

    except subprocess.TimeoutExpired:
        print("Piper tardó demasiado.")
    except Exception as e:
        print(f"Error en TTS: {str(e)}")


def _clean_text(text: str) -> str:
    clean = ""
    for char in text:
        if ord(char) < 65536:
            clean += char

    replacements = {
        "•": ",", "─": "", "═": "", "→": ",",
        "✓": "sí", "❌": "no", "📁": "", "📄": "",
        "🤖": "", "👤": "", "🎤": "", "⚠️": "advertencia:",
        "\n": " ", "  ": " ",
    }
    for old, new in replacements.items():
        clean = clean.replace(old, new)

    return clean.strip()