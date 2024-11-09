from typing import Optional
import tkinter as tk


def remove_punctuation(text_widget: tk.Text, punct: str) -> None:
    try:
        text = text_widget.get('1.0', tk.END)
        modified_text = text.replace(punct, '')
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, modified_text)
    except tk.TclError as e:
        raise ValueError(f"テキストウィジェットの操作に失敗しました: {e}")
    except Exception as e:
        raise RuntimeError(f"予期せぬエラーが発生しました: {e}")


def remove_spaces(text_widget: tk.Text) -> None:
    try:
        text = text_widget.get('1.0', tk.END)
        modified_text = ''.join(text.split())
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, modified_text)
    except tk.TclError as e:
        raise ValueError(f"テキストウィジェットの操作に失敗しました: {e}")
    except Exception as e:
        raise RuntimeError(f"予期せぬエラーが発生しました: {e}")


def remove_linebreaks(text_widget: tk.Text) -> None:
    try:
        text = text_widget.get('1.0', tk.END).strip()
        modified_text = ' '.join(text.splitlines())
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, modified_text)
    except tk.TclError as e:
        raise ValueError(f"テキストウィジェットの操作に失敗しました: {e}")
    except Exception as e:
        raise RuntimeError(f"予期せぬエラーが発生しました: {e}")


def get_text_content(text_widget: tk.Text) -> str:
    try:
        return text_widget.get('1.0', tk.END).strip()
    except tk.TclError as e:
        raise ValueError(f"テキストウィジェットの読み取りに失敗しました: {e}")
    except Exception as e:
        raise RuntimeError(f"予期せぬエラーが発生しました: {e}")


def set_text_content(
    text_widget: tk.Text,
    text: str,
    append: bool = False
) -> None:
    try:
        if not append:
            text_widget.delete('1.0', tk.END)
        if append and text_widget.get('1.0', tk.END).strip():
            text_widget.insert(tk.END, "\n")
        text_widget.insert(tk.END, text)
    except tk.TclError as e:
        raise ValueError(f"テキストウィジェットの書き込みに失敗しました: {e}")
    except Exception as e:
        raise RuntimeError(f"予期せぬエラーが発生しました: {e}")
