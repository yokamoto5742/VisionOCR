import tkinter as tk
from dataclasses import dataclass
from typing import Callable, List


@dataclass
class ButtonConfig:
    text: str
    command: Callable[[], None]
    is_highlight: bool = False


def create_buttons(parent: tk.Frame, buttons: List[ButtonConfig]) -> None:
    """ボタンリストからボタンウィジェットを作成してparentに配置する"""
    for btn_config in buttons:
        button = tk.Button(
            parent,
            text=btn_config.text,
            command=btn_config.command
        )

        if btn_config.is_highlight:
            button.configure(
                background='#007bff',  # 青色の背景
                foreground='white',  # 白色のテキスト
                font=('Helvetica', 10, 'bold'),  # 太字フォント
                relief=tk.RAISED,  # 浮き出た表示
                borderwidth=3  # より太いボーダー
            )

            button.bind('<Enter>', lambda e, b=button: b.configure(background='#0056b3'))
            button.bind('<Leave>', lambda e, b=button: b.configure(background='#007bff'))

        button.pack(side=tk.LEFT, padx=2)
