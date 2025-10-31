import os
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional

from utils.constants import (
    DATETIME_FORMAT,
    DEFAULT_ENCODING,
    DEFAULT_FILE_EXTENSION,
    DEFAULT_FILE_PREFIX,
)


def get_save_file_path() -> Optional[str]:
    """ファイル保存ダイアログを表示してパスを取得"""
    downloads_path = Path.home() / "Downloads"
    initial_dir = str(downloads_path if downloads_path.exists() else Path.cwd())
    current_time = datetime.now().strftime(DATETIME_FORMAT)
    default_filename = f'{DEFAULT_FILE_PREFIX}{current_time}{DEFAULT_FILE_EXTENSION}'

    return filedialog.asksaveasfilename(
        initialfile=default_filename,
        initialdir=initial_dir,
        defaultextension=DEFAULT_FILE_EXTENSION,
        filetypes=[('テキストファイル', f'*{DEFAULT_FILE_EXTENSION}'), ('すべてのファイル', '*.*')]
    )


def write_text_to_file(file_path: str, text: str) -> None:
    """テキストをファイルに書き込み"""
    with open(file_path, 'w', encoding=DEFAULT_ENCODING) as f:
        f.write(text)


def show_success_message() -> None:
    messagebox.showinfo('完了', 'テキストファイルを保存しました。')


def open_saved_directory(file_path: str) -> None:
    saved_dir = os.path.dirname(file_path)
    os.startfile(saved_dir)


def save_text_to_file(text: str) -> bool:
    """テキストをファイルに保存し、保存先フォルダを開く"""
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
