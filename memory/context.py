class ConversationContext:
    def __init__(self):
        """
        max_messages: cuántos mensajes guarda antes de olvidar los más viejos
        para no saturar el contexto del LLM
        """
        self.history = []
        self.max_messages = 16
        self.system_prompt = """
        Eres un asistente personal inteligente que corre localmente.
        Tu nombre es Aria.
        Puedes consultar el clima, crear y mover documentos, leer archivos y charlar.
        Respondes siempre en español, de forma natural y concisa.
        Cuando el usuario pida algo que involucre un archivo o el clima, 
        indicas claramente qué acción vas a realizar antes de hacerla.

        HERRAMIENTAS DISPONIBLES:
        - Clima: consulta temperatura, humedad y condiciones de cualquier ciudad
        - Crear archivos: genera archivos .txt, .md o .docx con contenido real y completo
        - Leer archivos: muestra el contenido de archivos existentes
        - Listar archivos: muestra todos los archivos en la carpeta de documentos
        - Mover archivos: mueve archivos a otras carpetas
        - Renombrar archivos: cambia el nombre de archivos existentes
        - Eliminar archivos: borra archivos permanentemente

        REGLAS IMPORTANTES:
        - Cuando creas un archivo, el contenido se escribe REALMENTE en disco. Nunca simules ni finjas.
        - Si el usuario pide crear un archivo con un tema (receta, carta, lista, etc.), el contenido debe ser COMPLETO y ÚTIL, no un placeholder.
        - Confirma siempre qué acción realizaste y con qué resultado.
        - Responde en español, de forma natural y concisa.
        - Si algo falla, explica el error claramente.
        - No meciones la ruta completa, solo mecionala como la carpeta raiz y si hay subcarpetas solo meciona el nombre y niveles.
        - Se directa, consisa y respode solo lo necesario con las tareas pero en una conversacion normal responde con naturalidad.
        """

    def add_user_message(self, message: str):
        self.history.append({
            "role": "user",
            "content": message
        })
        self._trim()
    
    def add_assistant_message(self, message: str):
        self.history.append({
            "role": "assistant", 
            "content": message
        })
        self._trim()

    def get_messages(self) -> list:
        """Devuelve el historial completo listo para enviarlo al LLM"""
        return [
            {"role": "system", "content": self.system_prompt}
        ] + self.history
    
    def _trim(self):
        """Elimina mensajes viejos si se pasa del límite"""
        if len(self.history) > self.max_messages:
            # Elimina los 2 más viejos (un par user/assistant)
            self.history = self.history[2:]

    def clear(self):
        """Limpia el historial completo"""
        self.history = []
        print("Memoria limpiada.")

    def show_history(self):
        """Muestra el historial en consola, útil para debug"""
        print("\n--- Historial de conversación ---")
        for msg in self.history:
            rol = "Tú" if msg["role"] == "user" else "Aria"
            print(f"{rol}: {msg['content']}")
        print("--------------------------------\n")