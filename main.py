import pyttsx3
import speech_recognition as sr
from tts import speak_piper
from memory.context import ConversationContext
from tools.chat import detect_intent, ask_llm, extract_params
from tools.weather import get_weather
from tools.files import (
    create_txt, create_md, create_docx,
    read_file, list_files,
    move_file, rename_file, delete_file
)

# ─────────────────────────────────────────
#  VOZ
# ─────────────────────────────────────────

def speak(text: str):
    """Convierte texto a voz con Piper TTS."""
    print(f"Aria: {text}")
    speak_piper(text)

# -- TODO NO FUNCIONA EL MICROFONO
def listen() -> str:
    """Escucha el micrófono y regresa el texto reconocido."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language="es-MX")
            print(f"👤 Tú: {text}")
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("No pude conectarme al reconocimiento de voz.")
            return ""


# ─────────────────────────────────────────
#  EJECUTAR HERRAMIENTAS
# ─────────────────────────────────────────

def execute_tool(intent: str, user_input: str) -> str:
    from tools.files import (
        create_txt, create_md, create_docx, create_docx_with_sections,
        append_txt, append_md, append_docx, replace_in_docx,
        create_xlsx, create_xlsx_from_dict, append_rows_xlsx, add_sheet_xlsx,
        read_file, read_txt, read_docx, read_xlsx,
        list_files, search_files, file_info,
        move_file, rename_file, copy_file, delete_file,
        create_folder, delete_folder, list_folder,
        rename_folder, move_folder, copy_folder, folder_info
    )

    params = extract_params(user_input, intent)

    if "error" in params:
        return f"No pude entender bien la solicitud: {params['error']}"

    # ── Clima ──
    if intent == "weather":
        return get_weather(params.get("city", "Monterrey"))

    # ── Texto ──
    elif intent == "create_txt":
        return create_txt(params["filename"], params.get("content", ""))
    elif intent == "create_md":
        return create_md(params["filename"], params.get("content", ""), params.get("title"))
    elif intent == "append_file":
        return append_txt(params["filename"], params.get("content", ""))

    # ── Word ──
    elif intent == "create_docx":
        return create_docx(params["filename"], params.get("content", ""), params.get("title"))
    elif intent == "append_docx":
        return append_docx(params["filename"], params.get("content", ""), params.get("section_title"))
    elif intent == "replace_in_docx":
        return replace_in_docx(params["filename"], params.get("old_text", ""), params.get("new_text", ""))

    # ── Excel ──
    elif intent == "create_xlsx":
        return create_xlsx(params["filename"], params.get("headers", []), params.get("rows", []))
    elif intent == "append_xlsx":
        return append_rows_xlsx(params["filename"], params.get("rows", []))
    elif intent == "add_sheet":
        return add_sheet_xlsx(params["filename"], params.get("sheet", "Hoja"), params.get("headers", []))

    # ── Leer ──
    elif intent == "read_file":
        return read_file(params.get("filename", ""))

    # ── Utilidades ──
    elif intent == "list_files":
        return list_files()
    elif intent == "search_files":
        return search_files(params.get("filename", ""))
    elif intent == "file_info":
        return file_info(params.get("filename", ""))
    elif intent == "move_file":
        return move_file(params["filename"], params.get("destination", ""))
    elif intent == "rename_file":
        return rename_file(params["filename"], params.get("new_name", ""))
    elif intent == "copy_file":
        return copy_file(params["filename"], params.get("copy_name", ""))
    elif intent == "delete_file":
        return delete_file(params.get("filename", ""))

    # ── Carpetas ──
    elif intent == "create_folder":
        return create_folder(params.get("folder", ""))
    elif intent == "delete_folder":
        return delete_folder(params.get("folder", ""))
    elif intent == "list_folder":
        return list_folder(params.get("folder"))
    elif intent == "rename_folder":
        return rename_folder(params["folder"], params.get("new_name", ""))
    elif intent == "move_folder":
        return move_folder(params["folder"], params.get("destination", ""))
    elif intent == "copy_folder":
        return copy_folder(params["folder"], params.get("copy_name", ""))
    elif intent == "folder_info":
        return folder_info(params.get("folder", ""))

    return "No supe cómo manejar esa solicitud."


# ─────────────────────────────────────────
#  LOOP PRINCIPAL
# ─────────────────────────────────────────

def main():
    context = ConversationContext()
    speak("Hola, soy Aria. ¿En qué te puedo ayudar?")
    print("\nEscribe tu mensaje o presiona Enter para hablar.")
    print("Comandos especiales: 'salir', 'limpiar memoria', 'historial'\n")

    while True:
        # ── Input: texto o voz ──
        user_input = input("👤 Tú (Enter para voz): ").strip()

        if user_input == "":
            user_input = listen()

        if not user_input:
            continue

        # ── Comandos especiales ──
        if user_input.lower() in ["salir", "exit", "adiós", "adios"]:
            speak("Hasta luego.")
            break

        if user_input.lower() in ["limpiar memoria", "olvida todo"]:
            context.clear()
            speak("Memoria limpiada.")
            continue

        if user_input.lower() in ["historial", "ver historial"]:
            context.show_history()
            continue

        # ── Detectar intención ──
        intent = detect_intent(user_input)
        context.add_user_message(user_input)

        # ── Ejecutar herramienta o chatear ──
        if intent == "chat":
            response = ask_llm(context.get_messages())
        else:
            tool_result = execute_tool(intent, user_input)
            # Le pasamos el resultado al LLM para que responda naturalmente
            context.add_user_message(
                f"[Resultado de la herramienta '{intent}']: {tool_result}"
            )
            response = ask_llm(context.get_messages())

        context.add_assistant_message(response)
        speak(response)


if __name__ == "__main__":
    main()