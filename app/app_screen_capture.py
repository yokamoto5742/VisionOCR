import tkinter as tk
from tkinter import messagebox
from typing import Any, Optional, Tuple

import pyautogui

from service.vision_ocr_service import VisionOCRService
from utils.config_manager import ConfigManager
from utils.constants import MIN_SCREENSHOT_SIZE, UIColors


class ScreenCapture:
    """画面の矩形領域を選択してOCR処理を行うキャプチャUI"""

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

        if self.start_x is not None and self.start_y is not None:
            self.selection_rect = self.canvas.create_rectangle(
                self.start_x, self.start_y,
                curr_x, curr_y,
                outline=UIColors.SELECTION_OUTLINE,
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
        """ユーザーが選択した矩形領域の座標を計算"""
        if any(coord is None for coord in [self.start_x, self.start_y, self.end_x, self.end_y]):
            raise ValueError("スクリーンショットの座標が正しく設定されていません")

        assert self.start_x is not None and self.end_x is not None
        assert self.start_y is not None and self.end_y is not None

        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        right = max(self.start_x, self.end_x)
        bottom = max(self.start_y, self.end_y)

        if right - left < MIN_SCREENSHOT_SIZE or bottom - top < MIN_SCREENSHOT_SIZE:
            return None

        return left, top, right, bottom

    def _validate_screenshot_bounds(self, bounds: Optional[Tuple[int, int, int, int]]) -> bool:
        """スクリーンショット境界を検証

        Args:
            bounds: スクリーンショット境界 (left, top, right, bottom)

        Returns:
            bool: 境界が有効な場合True、そうでない場合False
        """
        if bounds is None:
            messagebox.showwarning('OCR結果', 'スクリーンショットの範囲が小さすぎます。')
            return False
        return True

    def _capture_screenshot(self, bounds: Tuple[int, int, int, int]) -> Any:
        """スクリーンショットをキャプチャ

        Args:
            bounds: スクリーンショット境界 (left, top, right, bottom)

        Returns:
            キャプチャされたスクリーンショット画像
        """
        left, top, right, bottom = bounds
        return pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    def _extract_text_from_screenshot(self, screenshot: Any) -> Optional[str]:
        """スクリーンショットからテキストを抽出

        Args:
            screenshot: スクリーンショット画像

        Returns:
            Optional[str]: 抽出されたテキスト、失敗時はNone
        """
        try:
            text = self.ocr_service.perform_ocr(screenshot)
            if not text.strip():
                messagebox.showwarning('OCR結果', 'テキストを検出できませんでした。')
                return None
            return text
        except Exception as ocr_error:
            messagebox.showerror('OCRエラー', f'テキスト認識中にエラーが発生しました: {str(ocr_error)}')
            return None

    def _copy_text_to_clipboard(self, text: str) -> None:
        """テキストをクリップボードにコピー

        Args:
            text: コピーするテキスト
        """
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def _process_screenshot(self) -> None:
        """スクリーンショットを処理してテキストを抽出"""
        try:
            bounds = self._get_screenshot_bounds()

            if not self._validate_screenshot_bounds(bounds):
                self.root.quit()
                return

            if bounds is not None:
                screenshot = self._capture_screenshot(bounds)
                text = self._extract_text_from_screenshot(screenshot)

                if text is not None:
                    self._copy_text_to_clipboard(text)

        except Exception as e:
            messagebox.showerror('キャプチャエラー', f'スクリーンショット処理中にエラーが発生しました: {str(e)}')
