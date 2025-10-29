import tkinter as tk
from tkinter import messagebox

import pyautogui
from PIL import Image
from typing import Optional, Tuple

from utils.config_manager import ConfigManager
from service.vision_ocr_service import VisionOCRService


class ScreenCapture:
    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.root.clipboard_clear()
        self.ocr_service = VisionOCRService()
        self._setup_window()
        self._setup_canvas()
        self._bind_events()

    def _setup_window(self) -> None:
        try:
            self.config_manager = ConfigManager()
            transparency, outline_width = self.config_manager.get_screen_capture_settings()
        except Exception as e:
            messagebox.showerror('設定エラー', f'設定の読み込み中にエラーが発生しました: {str(e)}')
            raise

        self.root.attributes('-alpha', transparency)
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)

        self.outline_width: int = outline_width
        self.screen_width: int = self.root.winfo_screenwidth()
        self.screen_height: int = self.root.winfo_screenheight()

    def _setup_canvas(self) -> None:
        self.canvas = tk.Canvas(
            self.root,
            width=self.screen_width,
            height=self.screen_height,
            highlightthickness=0
        )
        self.canvas.pack()

        self.start_x: Optional[int] = None
        self.start_y: Optional[int] = None
        self.end_x: Optional[int] = None
        self.end_y: Optional[int] = None
        self.selection_rect: Optional[int] = None

    def _bind_events(self) -> None:
        self.canvas.bind('<Button-1>', self._on_press)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)
        self.root.bind('<Escape>', self._cancel)

    def _on_press(self, event: tk.Event) -> None:
        self.start_x = event.x
        self.start_y = event.y
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)

    def _on_drag(self, event: tk.Event) -> None:
        curr_x = event.x
        curr_y = event.y

        if self.selection_rect:
            self.canvas.delete(self.selection_rect)

        self.selection_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            curr_x, curr_y,
            outline='red',
            width=self.outline_width
        )

    def _on_release(self, event: tk.Event) -> None:
        self.end_x = event.x
        self.end_y = event.y
        self.root.withdraw()
        self._process_screenshot()
        self.root.quit()

    def _cancel(self, event: tk.Event) -> None:
        self.root.quit()

    def _get_screenshot_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        if any(coord is None for coord in [self.start_x, self.start_y, self.end_x, self.end_y]):
            raise ValueError("スクリーンショットの座標が正しく設定されていません")

        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        right = max(self.start_x, self.end_x)
        bottom = max(self.start_y, self.end_y)

        if right - left < 5 or bottom - top < 5:
            return None

        return left, top, right, bottom

    def _process_screenshot(self) -> None:
        try:
            bounds = self._get_screenshot_bounds()
            if bounds is None:
                messagebox.showwarning('OCR結果', 'スクリーンショットの範囲が小さすぎます。')
                self.root.quit()
                return

            left, top, right, bottom = bounds
            screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

            try:
                text = self.ocr_service.perform_ocr(screenshot)
                if not text.strip():
                    messagebox.showwarning('OCR結果', 'テキストを検出できませんでした。')
                    return

                self.root.clipboard_clear()
                self.root.clipboard_append(text)

            except Exception as ocr_error:
                messagebox.showerror('OCRエラー', f'テキスト認識中にエラーが発生しました: {str(ocr_error)}')

        except Exception as e:
            messagebox.showerror('キャプチャエラー', f'スクリーンショット処理中にエラーが発生しました: {str(e)}')
