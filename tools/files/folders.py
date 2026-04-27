# tools/files/folders.py
import os
import shutil
from datetime import datetime
from config import DOCS_FOLDER


def _build_path(folder_name: str) -> str:
    """Si la ruta no es absoluta, la construye dentro de DOCS_FOLDER."""
    if os.path.isabs(folder_name):
        return folder_name
    return os.path.join(DOCS_FOLDER, folder_name)


# ─────────────────────────────────────────
#  CREAR
# ─────────────────────────────────────────

def create_folder(folder_name: str) -> str:
    """
    Crea una carpeta dentro de DOCS_FOLDER.
    Soporta rutas anidadas: "proyectos/2024/enero"
    """
    path = _build_path(folder_name)
    try:
        if os.path.exists(path):
            return f"La carpeta '{folder_name}' ya existe."
        os.makedirs(path, exist_ok=True)
        return f"Carpeta '{folder_name}' creada en {DOCS_FOLDER}."
    except Exception as e:
        return f"Error creando carpeta '{folder_name}': {str(e)}"


# ─────────────────────────────────────────
#  ELIMINAR
# ─────────────────────────────────────────

def delete_folder(folder_name: str, force: bool = False) -> str:
    """
    Elimina una carpeta.
    force=False: solo elimina si está vacía.
    force=True: elimina aunque tenga contenido.
    """
    path = _build_path(folder_name)

    if not os.path.exists(path):
        return f"No encontré la carpeta '{folder_name}'."

    if not os.path.isdir(path):
        return f"'{folder_name}' no es una carpeta."

    try:
        if force:
            shutil.rmtree(path)
            return f"Carpeta '{folder_name}' y todo su contenido eliminados."
        else:
            contents = os.listdir(path)
            if contents:
                return (
                    f"La carpeta '{folder_name}' no está vacía "
                    f"({len(contents)} elemento(s)). "
                    f"¿Confirmas que quieres eliminarla con todo su contenido?"
                )
            os.rmdir(path)
            return f"Carpeta '{folder_name}' eliminada."
    except Exception as e:
        return f"Error eliminando carpeta '{folder_name}': {str(e)}"


# ─────────────────────────────────────────
#  LISTAR
# ─────────────────────────────────────────

def list_folder(folder_name: str = None) -> str:
    """
    Lista el contenido de una carpeta específica.
    Si no se especifica, lista DOCS_FOLDER.
    Muestra archivos y subcarpetas con tamaño y fecha.
    """
    path = _build_path(folder_name) if folder_name else DOCS_FOLDER

    if not os.path.exists(path):
        return f"No encontré la carpeta '{folder_name}'."

    try:
        entries = sorted(os.listdir(path))

        if not entries:
            return f"La carpeta '{path}' está vacía."

        folders = []
        files   = []

        for entry in entries:
            full = os.path.join(path, entry)
            mtime = datetime.fromtimestamp(os.path.getmtime(full)).strftime("%d/%m/%Y %H:%M")

            if os.path.isdir(full):
                num_items = len(os.listdir(full))
                folders.append(f" {entry}/  [{num_items} elemento(s)  {mtime}]")
            else:
                size = os.path.getsize(full)
                size_str = f"{size}B" if size < 1024 else f"{size // 1024}KB"
                files.append(f" {entry}  [{size_str}  {mtime}]")

        lines = [f"Contenido de '{path}':"]
        if folders:
            lines.append("Carpetas:")
            lines.extend(folders)
        if files:
            lines.append("Archivos:")
            lines.extend(files)
        lines.append(f"\nTotal: {len(folders)} carpeta(s), {len(files)} archivo(s)")

        return "\n".join(lines)

    except Exception as e:
        return f"Error listando '{folder_name}': {str(e)}"


# ─────────────────────────────────────────
#  MOVER Y RENOMBRAR
# ─────────────────────────────────────────

def rename_folder(folder_name: str, new_name: str) -> str:
    """Renombra una carpeta dentro de DOCS_FOLDER."""
    old_path = _build_path(folder_name)
    new_path = _build_path(new_name)

    if not os.path.exists(old_path):
        return f"No encontré la carpeta '{folder_name}'."

    if os.path.exists(new_path):
        return f"Ya existe una carpeta llamada '{new_name}'."

    try:
        os.rename(old_path, new_path)
        return f"Carpeta '{folder_name}' renombrada a '{new_name}'."
    except Exception as e:
        return f"Error renombrando carpeta: {str(e)}"


def move_folder(folder_name: str, destination: str) -> str:
    """
    Mueve una carpeta a otro destino dentro de DOCS_FOLDER.
    Ejemplo: move_folder("fotos", "archivo/2024")
    """
    source = _build_path(folder_name)
    dest   = _build_path(destination)

    if not os.path.exists(source):
        return f"No encontré la carpeta '{folder_name}'."

    try:
        os.makedirs(dest, exist_ok=True)
        shutil.move(source, os.path.join(dest, folder_name))
        return f"Carpeta '{folder_name}' movida a '{destination}'."
    except Exception as e:
        return f"Error moviendo carpeta: {str(e)}"


# ─────────────────────────────────────────
#  COPIAR
# ─────────────────────────────────────────

def copy_folder(folder_name: str, new_name: str) -> str:
    """Copia una carpeta completa con otro nombre dentro de DOCS_FOLDER."""
    source = _build_path(folder_name)
    dest   = _build_path(new_name)

    if not os.path.exists(source):
        return f"No encontré la carpeta '{folder_name}'."

    if os.path.exists(dest):
        return f"Ya existe una carpeta llamada '{new_name}'."

    try:
        shutil.copytree(source, dest)
        return f"Carpeta '{folder_name}' copiada como '{new_name}'."
    except Exception as e:
        return f"Error copiando carpeta: {str(e)}"


# ─────────────────────────────────────────
#  INFO
# ─────────────────────────────────────────

def folder_info(folder_name: str) -> str:
    """Muestra información detallada de una carpeta."""
    path = _build_path(folder_name)

    if not os.path.exists(path):
        return f"No encontré la carpeta '{folder_name}'."

    try:
        total_files   = 0
        total_folders = 0
        total_size    = 0

        for root, dirs, files in os.walk(path):
            total_folders += len(dirs)
            total_files   += len(files)
            for f in files:
                total_size += os.path.getsize(os.path.join(root, f))

        size_str = (
            f"{total_size}B" if total_size < 1024
            else f"{total_size // 1024}KB" if total_size < 1024 ** 2
            else f"{total_size // (1024 ** 2)}MB"
        )

        mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%d/%m/%Y %H:%M")
        ctime = datetime.fromtimestamp(os.path.getctime(path)).strftime("%d/%m/%Y %H:%M")

        return (
            f"Carpeta: {folder_name}\n"
            f"Ruta: {path}\n"
            f"Archivos: {total_files}\n"
            f"Subcarpetas: {total_folders}\n"
            f"Tamaño total: {size_str}\n"
            f"Creada: {ctime}\n"
            f"Modificada: {mtime}"
        )
    except Exception as e:
        return f"Error obteniendo info: {str(e)}"