import tkinter as tk
from dataclasses import dataclass
from typing import Callable, List

from utils.constants import UIColors, UILayout


@dataclass
class ButtonConfig:
    """ボタンの設定を保持するデータクラス"""
    text: str
    command: Callable[[], None]
    is_highlight: bool = False


def create_buttons(parent: tk.Frame, buttons: List[ButtonConfig]) -> None:
    """ボタンリストからボタンウィジェットを作成して配置する"""
    for btn_config in buttons:
        button = tk.Button(
            parent,
            text=btn_config.text,
            command=btn_config.command
        )

        if btn_config.is_highlight:
            button.configure(
                background=UIColors.HIGHLIGHT_PRIMARY,
                foreground=UIColors.HIGHLIGHT_TEXT,
                font=UILayout.HIGHLIGHT_FONT,
                relief=tk.RAISED,
                borderwidth=UILayout.HIGHLIGHT_BORDER_WIDTH
            )

            button.bind('<Enter>', lambda e, b=button: b.configure(background=UIColors.HIGHLIGHT_HOVER))
            button.bind('<Leave>', lambda e, b=button: b.configure(background=UIColors.HIGHLIGHT_PRIMARY))

        button.pack(side=tk.LEFT, padx=UILayout.BUTTON_PADDING)
