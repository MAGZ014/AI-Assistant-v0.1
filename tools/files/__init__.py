# tools/files/__init__.py

# ── Texto plano ──
from .text_files import (
    create_txt,
    create_md,
    append_txt,
    append_md,
    read_txt
)

# ── Word ──
from .word_files import (
    create_docx,
    create_docx_with_sections,
    read_docx,
    append_docx,
    replace_in_docx
)

# ── Excel ──
from .excel_files import (
    create_xlsx,
    create_xlsx_from_dict,
    create_xlsx_multi_sheet,
    read_xlsx,
    list_sheets,
    append_rows_xlsx,
    add_sheet_xlsx
)

# ── Carpetas ──
from .folders import (
    create_folder,
    delete_folder,
    list_folder,
    rename_folder,
    move_folder,
      copy_folder,
    folder_info
)

# ── Utilidades ──
from .utils import (
    read_file,
    list_files,
    move_file,
    rename_file,
    copy_file,
    delete_file,
    search_files,
    file_info,
    append_to_file
)