# tools/chat.py
from groq import Groq
from openai import OpenAI
from config import (
    GROQ_API_KEY, GROQ_MODEL,
    LM_STUDIO_BASE_URL, LM_STUDIO_MODEL,
    DEFAULT_LLM
)

# ─────────────────────────────────────────
#  CLIENTES
# ─────────────────────────────────────────

groq_client = Groq(api_key=GROQ_API_KEY)

local_client = OpenAI(
    base_url=LM_STUDIO_BASE_URL,
    api_key="lm-studio"
)


# ─────────────────────────────────────────
#  DETECTAR INTENCIÓN
# ─────────────────────────────────────────

def detect_intent(user_input: str) -> str:
    text = user_input.lower()

    # Clima
    if any(w in text for w in ["clima", "temperatura", "tiempo en", "weather", "lluvia", "calor", "frío", "pronóstico"]):
        return "weather"

    # Carpetas
    if any(w in text for w in ["crea la carpeta", "crear carpeta", "nueva carpeta"]):
        return "create_folder"
    if any(w in text for w in ["elimina la carpeta", "eliminar carpeta", "borra la carpeta"]):
        return "delete_folder"
    if any(w in text for w in ["renombra la carpeta", "renombrar carpeta"]):
        return "rename_folder"
    if any(w in text for w in ["mueve la carpeta", "mover carpeta"]):
        return "move_folder"
    if any(w in text for w in ["copia la carpeta", "copiar carpeta"]):
        return "copy_folder"
    if any(w in text for w in ["info de la carpeta", "información de la carpeta"]):
        return "folder_info"

    # Archivos - crear
    if any(w in text for w in ["crea", "crear", "nuevo archivo", "genera un archivo", "escribe un archivo"]):
        if "excel" in text or "xlsx" in text or "hoja de cálculo" in text or "tabla" in text:
            return "create_xlsx"
        if "word" in text or "docx" in text or "documento" in text:
            return "create_docx"
        if "markdown" in text or ".md" in text:
            return "create_md"
        return "create_txt"

    # Archivos - modificar
    if any(w in text for w in ["agrega", "agregar", "añade", "añadir", "append"]):
        if "excel" in text or "xlsx" in text:
            return "append_xlsx"
        if "word" in text or "docx" in text:
            return "append_docx"
        return "append_file"

    if any(w in text for w in ["reemplaza", "reemplazar", "cambia el texto", "sustituye"]):
        return "replace_in_docx"

    if any(w in text for w in ["nueva hoja", "agregar hoja", "añadir hoja"]):
        return "add_sheet"

    # Archivos - leer
    if any(w in text for w in ["lee", "leer", "muestra", "mostrar", "abre", "abrir", "contenido de", "qué dice"]):
        return "read_file"

    # Archivos - listar
    if any(w in text for w in ["lista", "listar", "qué archivos", "que archivos", "mis archivos", "archivos tengo"]):
        return "list_files"

    # Archivos - buscar
    if any(w in text for w in ["busca", "buscar", "encuentra", "encontrar", "dónde está"]):
        return "search_files"

    # Archivos - info
    if any(w in text for w in ["info del archivo", "información del archivo", "detalles del archivo", "tamaño del archivo"]):
        return "file_info"

    # Archivos - mover / renombrar / copiar / eliminar
    if any(w in text for w in ["mueve", "mover el archivo"]):
        return "move_file"
    if any(w in text for w in ["renombra", "renombrar el archivo", "cambia el nombre"]):
        return "rename_file"
    if any(w in text for w in ["copia el archivo", "copiar el archivo"]):
        return "copy_file"
    if any(w in text for w in ["elimina", "eliminar", "borra", "borrar"]):
        return "delete_file"

    return "chat"


# ─────────────────────────────────────────
#  LLAMADAS AL LLM
# ─────────────────────────────────────────

def ask_groq(messages: list, temperature: float = 0.7) -> str:
    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error con Groq: {str(e)}"


def ask_local(messages: list, temperature: float = 0.7) -> str:
    try:
        response = local_client.chat.completions.create(
            model=LM_STUDIO_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error con modelo local: {str(e)}"


def ask_llm(messages: list, force: str = None, temperature: float = 0.7) -> str:
    backend = force if force else DEFAULT_LLM
    if backend == "groq":
        return ask_groq(messages, temperature)
    elif backend == "local":
        return ask_local(messages, temperature)
    else:
        return "Backend no reconocido. Usa 'groq' o 'local'."


# ─────────────────────────────────────────
#  EXTRAER PARÁMETROS
# ─────────────────────────────────────────

def extract_params(user_input: str, intent: str) -> dict:
    prompts = {

        # ── Clima ──
        "weather": f"""El usuario dijo: "{user_input}"
Extrae el nombre de la ciudad. Si no menciona ninguna usa "Monterrey".
Responde SOLO con el nombre de la ciudad.""",

        # ── Archivos de texto ──
        "create_txt": f"""El usuario dijo: "{user_input}"
Extrae o GENERA:
1. nombre: nombre corto para el archivo (sin extensión, usa guiones_bajos)
2. contenido: si el usuario no lo dio, GENERA contenido completo y útil sobre el tema

Responde SOLO en este formato:
nombre|contenido""",

        "create_md": f"""El usuario dijo: "{user_input}"
Extrae o GENERA:
1. nombre: nombre corto (sin extensión, usa guiones_bajos)
2. titulo: título legible para el encabezado H1
3. contenido: contenido completo en formato Markdown con secciones ## si aplica

Responde SOLO en este formato:
nombre|titulo|contenido""",

        # ── Word ──
        "create_docx": f"""El usuario dijo: "{user_input}"
Extrae o GENERA:
1. nombre: nombre corto (sin extensión, usa guiones_bajos)
2. titulo: título legible para el documento
3. contenido: contenido completo. Usa ## para secciones, - para listas, 1. para listas numeradas

Responde SOLO en este formato:
nombre|titulo|contenido""",

        "append_docx": f"""El usuario dijo: "{user_input}"
Extrae:
1. nombre del archivo existente (con o sin .docx)
2. titulo de la nueva sección (opcional, deja vacío si no aplica)
3. contenido a agregar

Responde SOLO en este formato:
nombre|titulo_seccion|contenido""",

        "replace_in_docx": f"""El usuario dijo: "{user_input}"
Extrae:
1. nombre del archivo
2. texto a buscar
3. texto de reemplazo

Responde SOLO en este formato:
nombre|texto_viejo|texto_nuevo""",

        # ── Excel ──
        "create_xlsx": f"""El usuario dijo: "{user_input}"
Extrae o GENERA:
1. nombre: nombre corto (sin extensión, usa guiones_bajos)
2. encabezados: columnas separadas por coma
3. filas: cada fila separada por ; y sus valores separados por coma

Responde SOLO en este formato:
nombre|col1,col2,col3|val1,val2,val3;val1,val2,val3""",

        "append_xlsx": f"""El usuario dijo: "{user_input}"
Extrae:
1. nombre del archivo
2. filas a agregar: cada fila separada por ; y valores por coma

Responde SOLO en este formato:
nombre|val1,val2,val3;val1,val2,val3""",

        "add_sheet": f"""El usuario dijo: "{user_input}"
Extrae:
1. nombre del archivo Excel
2. nombre de la nueva hoja
3. encabezados separados por coma

Responde SOLO en este formato:
archivo|hoja|col1,col2,col3""",

        # ── Utilidades ──
        "read_file": f"""El usuario dijo: "{user_input}"
Extrae el nombre del archivo que quiere leer incluyendo extensión si la mencionó.
Responde SOLO con el nombre del archivo.""",

        "search_files": f"""El usuario dijo: "{user_input}"
Extrae el término de búsqueda (nombre parcial o extensión como .docx, .txt).
Responde SOLO con el término de búsqueda.""",

        "file_info": f"""El usuario dijo: "{user_input}"
Extrae el nombre del archivo del que quiere información.
Responde SOLO con el nombre del archivo.""",

        "move_file": f"""El usuario dijo: "{user_input}"
Extrae:
1. nombre del archivo
2. carpeta destino

Responde SOLO en este formato:
archivo|destino""",

        "rename_file": f"""El usuario dijo: "{user_input}"
Extrae:
1. nombre actual
2. nombre nuevo

Responde SOLO en este formato:
nombre_actual|nombre_nuevo""",

        "copy_file": f"""El usuario dijo: "{user_input}"
Extrae:
1. nombre del archivo original
2. nombre de la copia

Responde SOLO en este formato:
original|copia""",

        "delete_file": f"""El usuario dijo: "{user_input}"
Extrae el nombre del archivo a eliminar.
Responde SOLO con el nombre del archivo.""",

        # ── Carpetas ──
        "create_folder": f"""El usuario dijo: "{user_input}"
Extrae el nombre o ruta de la carpeta a crear.
Soporta rutas anidadas como proyectos/2024/enero.
Responde SOLO con el nombre/ruta de la carpeta.""",

        "delete_folder": f"""El usuario dijo: "{user_input}"
Extrae el nombre de la carpeta a eliminar.
Responde SOLO con el nombre de la carpeta.""",

        "rename_folder": f"""El usuario dijo: "{user_input}"
Extrae:
1. nombre actual de la carpeta
2. nombre nuevo

Responde SOLO en este formato:
nombre_actual|nombre_nuevo""",

        "move_folder": f"""El usuario dijo: "{user_input}"
Extrae:
1. nombre de la carpeta a mover
2. destino

Responde SOLO en este formato:
carpeta|destino""",

        "copy_folder": f"""El usuario dijo: "{user_input}"
Extrae:
1. nombre de la carpeta original
2. nombre de la copia

Responde SOLO en este formato:
original|copia""",

        "folder_info": f"""El usuario dijo: "{user_input}"
Extrae el nombre de la carpeta de la que quiere información.
Responde SOLO con el nombre de la carpeta.""",
    }

    if intent not in prompts:
        return {}

    messages = [{"role": "user", "content": prompts[intent]}]
    raw = ask_llm(messages, temperature=0.1).strip()

    try:
        if intent == "weather":
            return {"city": raw}

        elif intent == "create_txt":
            p = raw.split("|", 1)
            return {"filename": p[0].strip(), "content": p[1].strip() if len(p) > 1 else ""}

        elif intent == "create_md":
            p = raw.split("|", 2)
            return {
                "filename": p[0].strip(),
                "title":    p[1].strip() if len(p) > 1 else "",
                "content":  p[2].strip() if len(p) > 2 else ""
            }

        elif intent == "create_docx":
            p = raw.split("|", 2)
            return {
                "filename": p[0].strip(),
                "title":    p[1].strip() if len(p) > 1 else "",
                "content":  p[2].strip() if len(p) > 2 else ""
            }

        elif intent == "append_docx":
            p = raw.split("|", 2)
            return {
                "filename":      p[0].strip(),
                "section_title": p[1].strip() if len(p) > 1 else "",
                "content":       p[2].strip() if len(p) > 2 else ""
            }

        elif intent == "replace_in_docx":
            p = raw.split("|", 2)
            return {
                "filename": p[0].strip(),
                "old_text": p[1].strip() if len(p) > 1 else "",
                "new_text": p[2].strip() if len(p) > 2 else ""
            }

        elif intent == "create_xlsx":
            p = raw.split("|", 2)
            headers = [h.strip() for h in p[1].split(",")] if len(p) > 1 else []
            rows = []
            if len(p) > 2:
                for row_str in p[2].split(";"):
                    row = [v.strip() for v in row_str.split(",")]
                    if any(row):
                        rows.append(row)
            return {"filename": p[0].strip(), "headers": headers, "rows": rows}

        elif intent == "append_xlsx":
            p = raw.split("|", 1)
            rows = []
            if len(p) > 1:
                for row_str in p[1].split(";"):
                    row = [v.strip() for v in row_str.split(",")]
                    if any(row):
                        rows.append(row)
            return {"filename": p[0].strip(), "rows": rows}

        elif intent == "add_sheet":
            p = raw.split("|", 2)
            headers = [h.strip() for h in p[2].split(",")] if len(p) > 2 else []
            return {
                "filename": p[0].strip(),
                "sheet":    p[1].strip() if len(p) > 1 else "Nueva Hoja",
                "headers":  headers
            }

        elif intent in ["read_file", "search_files", "file_info", "delete_file"]:
            return {"filename": raw}

        elif intent in ["move_file", "rename_file", "copy_file"]:
            p = raw.split("|", 1)
            key2 = "destination" if intent == "move_file" else "new_name" if intent == "rename_file" else "copy_name"
            return {"filename": p[0].strip(), key2: p[1].strip() if len(p) > 1 else ""}

        elif intent in ["create_folder", "delete_folder", "folder_info"]:
            return {"folder": raw}

        elif intent in ["rename_folder", "move_folder", "copy_folder"]:
            p = raw.split("|", 1)
            key2 = "new_name" if intent == "rename_folder" else "destination" if intent == "move_folder" else "copy_name"
            return {"folder": p[0].strip(), key2: p[1].strip() if len(p) > 1 else ""}

    except Exception as e:
        return {"error": str(e)}

    return {}