import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from tkinter import filedialog, messagebox


def get_save_file_path() -> Optional[str]:
    downloads_path = Path.home() / "Downloads"
    initial_dir = str(downloads_path if downloads_path.exists() else Path.cwd())
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    default_filename = f'OCR_result_{current_time}.txt'

    return filedialog.asksaveasfilename(
        initialfile=default_filename,
        initialdir=initial_dir,
        defaultextension='.txt',
        filetypes=[('テキストファイル', '*.txt'), ('すべてのファイル', '*.*')]
    )


def write_text_to_file(file_path: str, text: str) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)


def show_success_message() -> None:
    messagebox.showinfo('完了', 'テキストファイルを保存しました。')


def open_saved_directory(file_path: str) -> None:
    saved_dir = os.path.dirname(file_path)
    os.startfile(saved_dir)


def save_text_to_file(text: str) -> bool:
    file_path = get_save_file_path()
    if not file_path:
        return False

    try:
        write_text_to_file(file_path, text)
        show_success_message()
        open_saved_directory(file_path)
        return True

    except PermissionError:
        messagebox.showerror('エラー', 'ファイルへのアクセス権限がありません。')
        return False
    except OSError as e:
        messagebox.showerror('エラー', f'ファイル操作エラー: {e}')
        return False
    except Exception as e:
        messagebox.showerror('エラー', f'予期せぬエラーが発生しました: {e}')
        return False
