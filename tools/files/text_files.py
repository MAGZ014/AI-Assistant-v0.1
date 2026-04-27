# tools/files/text_files.py
import os
from datetime import datetime
from config import DOCS_FOLDER


def _build_path(filename: str, ext: str) -> str:
    """Asegura que el archivo tenga la extensión correcta y regresa la ruta completa."""
    if not filename.endswith(f".{ext}"):
        filename += f".{ext}"
    return os.path.join(DOCS_FOLDER, filename), filename


# ─────────────────────────────────────────
#  TXT
# ─────────────────────────────────────────

def create_txt(filename: str, content: str = "") -> str:
    """Crea un archivo .txt con contenido."""
    path, filename = _build_path(filename, "txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Archivo '{filename}' creado correctamente."
    except Exception as e:
        return f"Error creando '{filename}': {str(e)}"


def append_txt(filename: str, content: str) -> str:
    """Agrega contenido al final de un .txt existente."""
    path, filename = _build_path(filename, "txt")
    if not os.path.exists(path):
        return f"No encontré '{filename}'. ¿Quieres crearlo primero?"
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n{content}")
        return f"Contenido agregado a '{filename}'."
    except Exception as e:
        return f"Error agregando a '{filename}': {str(e)}"


# ─────────────────────────────────────────
#  MD
# ─────────────────────────────────────────

def create_md(filename: str, content: str = "", title: str = None) -> str:
    """
    Crea un archivo .md con formato Markdown.
    Si se proporciona title, lo agrega como encabezado H1.
    """
    path, filename = _build_path(filename, "md")
    try:
        with open(path, "w", encoding="utf-8") as f:
            if title:
                f.write(f"# {title}\n\n")
            # Fecha de creación como metadata
            f.write(f"> Creado: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            f.write(content)
        return f"Archivo Markdown '{filename}' creado correctamente."
    except Exception as e:
        return f"Error creando '{filename}': {str(e)}"


def append_md(filename: str, content: str, section_title: str = None) -> str:
    """
    Agrega contenido a un .md existente.
    Si se proporciona section_title, lo agrega como encabezado H2.
    """
    path, filename = _build_path(filename, "md")
    if not os.path.exists(path):
        return f"No encontré '{filename}'. ¿Quieres crearlo primero?"
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n")
            if section_title:
                f.write(f"\n## {section_title}\n\n")
            f.write(content)
        return f"Sección agregada a '{filename}'."
    except Exception as e:
        return f"Error agregando a '{filename}': {str(e)}"


def read_txt(filename: str, max_chars: int = 3000) -> str:
    """Lee un archivo .txt o .md y regresa su contenido."""
    # Intenta con la extensión que venga, si no tiene agrega .txt
    path = os.path.join(DOCS_FOLDER, filename)
    if not os.path.exists(path):
        path = os.path.join(DOCS_FOLDER, filename + ".txt")
        filename = filename + ".txt"

    if not os.path.exists(path):
        return f"No encontré '{filename}'."

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        if len(text) > max_chars:
            text = text[:max_chars] + f"\n\n... [truncado, {len(text) - max_chars} caracteres restantes]"

        return f"Contenido de '{filename}':\n\n{text}"
    except Exception as e:
        return f"Error leyendo '{filename}': {str(e)}"