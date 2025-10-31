"""テキストウィジェット操作ユーティリティ

このモジュールは、tkinterのTextウィジェットに対する
共通操作を提供します。すべての関数は適切なエラーハンドリングを行います。
"""

# 標準ライブラリ
import tkinter as tk
from functools import wraps
from typing import Any, Callable, TypeVar

# 型変数の定義
F = TypeVar('F', bound=Callable[..., Any])


def safe_text_operation(func: F) -> F:
    """テキストウィジェット操作の安全なラッパー

    TclErrorとその他の例外を適切に処理するデコレータです。
    すべてのテキストウィジェット操作関数に適用されます。

    Args:
        func: ラップする関数

    Returns:
        F: ラップされた関数

    Raises:
        ValueError: TclError が発生した場合
        RuntimeError: その他の予期しないエラーが発生した場合
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except tk.TclError as e:
            raise ValueError(f"テキストウィジェットの操作に失敗しました: {e}")
        except Exception as e:
            raise RuntimeError(f"予期せぬエラーが発生しました: {e}")
    return wrapper  # type: ignore[return-value]


@safe_text_operation
def remove_punctuation(text_widget: tk.Text, punct: str) -> None:
    """指定した句読点をテキストから削除
    
    Args:
        text_widget: 対象のテキストウィジェット
        punct: 削除する句読点（例: '、', '。'）
        
    Raises:
        ValueError: テキストウィジェットの操作に失敗した場合
        RuntimeError: 予期しないエラーが発生した場合
    """
    text = text_widget.get('1.0', tk.END)
    modified_text = text.replace(punct, '')
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, modified_text)


@safe_text_operation
def remove_spaces(text_widget: tk.Text) -> None:
    """すべての空白文字（スペース、タブ、改行）を削除
    
    Args:
        text_widget: 対象のテキストウィジェット
        
    Raises:
        ValueError: テキストウィジェットの操作に失敗した場合
        RuntimeError: 予期しないエラーが発生した場合
    """
    text = text_widget.get('1.0', tk.END)
    modified_text = ''.join(text.split())
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, modified_text)


@safe_text_operation
def remove_linebreaks(text_widget: tk.Text) -> None:
    """改行を空白に置換
    
    複数行のテキストを1行にまとめます。
    各行の間には空白が挿入されます。
    
    Args:
        text_widget: 対象のテキストウィジェット
        
    Raises:
        ValueError: テキストウィジェットの操作に失敗した場合
        RuntimeError: 予期しないエラーが発生した場合
    """
    text = text_widget.get('1.0', tk.END).strip()
    modified_text = ' '.join(text.splitlines())
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, modified_text)


@safe_text_operation
def get_text_content(text_widget: tk.Text) -> str:
    """テキストウィジェットの内容を取得
    
    Args:
        text_widget: 対象のテキストウィジェット
        
    Returns:
        str: テキストの内容（末尾の空白を除去）
        
    Raises:
        ValueError: テキストウィジェットの読み取りに失敗した場合
        RuntimeError: 予期しないエラーが発生した場合
    """
    return text_widget.get('1.0', tk.END).strip()


@safe_text_operation
def set_text_content(
    text_widget: tk.Text,
    text: str,
    append: bool = False
) -> None:
    """テキストウィジェットに内容を設定
    
    Args:
        text_widget: 対象のテキストウィジェット
        text: 設定するテキスト
        append: True の場合は追記、False の場合は上書き
        
    Raises:
        ValueError: テキストウィジェットの書き込みに失敗した場合
        RuntimeError: 予期しないエラーが発生した場合
    """
    if not append:
        text_widget.delete('1.0', tk.END)
    if append and text_widget.get('1.0', tk.END).strip():
        text_widget.insert(tk.END, "\n")
    text_widget.insert(tk.END, text)


@safe_text_operation
def clear_text(text_widget: tk.Text) -> None:
    """テキストウィジェットの内容をクリア
    
    Args:
        text_widget: 対象のテキストウィジェット
        
    Raises:
        ValueError: テキストウィジェットの操作に失敗した場合
        RuntimeError: 予期しないエラーが発生した場合
    """
    text_widget.delete('1.0', tk.END)


@safe_text_operation
def insert_text(text_widget: tk.Text, text: str, position: str = tk.END) -> None:
    """指定位置にテキストを挿入
    
    Args:
        text_widget: 対象のテキストウィジェット
        text: 挿入するテキスト
        position: 挿入位置（デフォルト: 末尾）
        
    Raises:
        ValueError: テキストウィジェットの操作に失敗した場合
        RuntimeError: 予期しないエラーが発生した場合
    """
    text_widget.insert(position, text)
