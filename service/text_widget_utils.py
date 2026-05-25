import re
import tkinter as tk

from utils.constants import TextPosition


def remove_punctuation(text_widget: tk.Text, punct: str) -> None:
    """指定した句読点をテキストから削除"""
    text = text_widget.get(TextPosition.START, TextPosition.END)
    modified_text = text.replace(punct, "")
    text_widget.delete(TextPosition.START, TextPosition.END)
    text_widget.insert(TextPosition.END, modified_text)


def remove_page_separators(text_widget: tk.Text) -> None:
    """「--- Nページ目 ---」形式の区切り行を削除"""
    text = text_widget.get(TextPosition.START, TextPosition.END)
    modified_text = re.sub(r"--- \d+ページ目 ---\n?", "", text)
    text_widget.delete(TextPosition.START, TextPosition.END)
    text_widget.insert(TextPosition.END, modified_text)


def remove_spaces(text_widget: tk.Text) -> None:
    """スペースとタブを削除"""
    text = text_widget.get(TextPosition.START, TextPosition.END)
    modified_text = re.sub(r"[ \t]", "", text)
    text_widget.delete(TextPosition.START, TextPosition.END)
    text_widget.insert(TextPosition.END, modified_text)


def remove_linebreaks(text_widget: tk.Text) -> None:
    """複数行のテキストを1行にまとめる"""
    text = text_widget.get(TextPosition.START, TextPosition.END).strip()
    modified_text = "".join(text.splitlines())
    text_widget.delete(TextPosition.START, TextPosition.END)
    text_widget.insert(TextPosition.END, modified_text)


def get_text_content(text_widget: tk.Text) -> str:
    """テキストウィジェットの内容を取得（末尾の空白を除去）"""
    return text_widget.get(TextPosition.START, TextPosition.END).strip()


def set_text_content(text_widget: tk.Text, text: str, append: bool = False) -> None:
    """テキストウィジェットに内容を設定（append=True で追記、False で上書き）"""
    if not append:
        text_widget.delete(TextPosition.START, TextPosition.END)
    if append and text_widget.get(TextPosition.START, TextPosition.END).strip():
        text_widget.insert(TextPosition.END, "\n")
    text_widget.insert(TextPosition.END, text)


def clear_text(text_widget: tk.Text) -> None:
    """テキストウィジェットの内容をクリア"""
    text_widget.delete(TextPosition.START, TextPosition.END)


def insert_text(
    text_widget: tk.Text, text: str, position: str = TextPosition.END
) -> None:
    """指定位置にテキストを挿入"""
    text_widget.insert(position, text)
