import tkinter as tk
from tkinter import messagebox
from typing import Any, Optional, Tuple

import pyautogui

from external_service.vision_ocr_service import VisionOCRService
from utils.config_manager import ConfigManager
from utils.constants import MIN_SCREENSHOT_SIZE, UIColors, UILabels, UIMessages


class ScreenCapture:
    """画面の矩形領域を選択してOCR処理を行う"""

    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.ocr_service = VisionOCRService()
        self.result_text: Optional[str] = None
        self._setup_window()
        self._setup_canvas()
        self._bind_events()

    def _setup_window(self) -> None:
        try:
            self.config_manager = ConfigManager()
            transparency, outline_width = (
                self.config_manager.get_screen_capture_settings()
            )
        except Exception as e:
            messagebox.showerror(
                UILabels.TITLE_CONFIG_ERROR,
                UIMessages.ERR_CONFIG_LOAD.format(error=str(e)),
            )
            raise

        self.root.attributes("-alpha", transparency)
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)

        self.outline_width: int = outline_width
        self.screen_width: int = self.root.winfo_screenwidth()
        self.screen_height: int = self.root.winfo_screenheight()

    def _setup_canvas(self) -> None:
        self.canvas = tk.Canvas(
            self.root,
            width=self.screen_width,
            height=self.screen_height,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.start_x: Optional[int] = None
        self.start_y: Optional[int] = None
        self.end_x: Optional[int] = None
        self.end_y: Optional[int] = None
        self.selection_rect: Optional[int] = None

    def _bind_events(self) -> None:
        self.canvas.bind("<Button-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.root.bind("<Escape>", self._cancel)

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
                self.start_x,
                self.start_y,
                curr_x,
                curr_y,
                outline=UIColors.SELECTION_OUTLINE,
                width=self.outline_width,
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
        if any(c is None for c in [self.start_x, self.start_y, self.end_x, self.end_y]):
            raise ValueError(UIMessages.COORD_INVALID)

        start_x: int = self.start_x  # type: ignore[assignment]
        start_y: int = self.start_y  # type: ignore[assignment]
        end_x: int = self.end_x  # type: ignore[assignment]
        end_y: int = self.end_y  # type: ignore[assignment]

        left = min(start_x, end_x)
        top = min(start_y, end_y)
        right = max(start_x, end_x)
        bottom = max(start_y, end_y)

        if right - left < MIN_SCREENSHOT_SIZE or bottom - top < MIN_SCREENSHOT_SIZE:
            return None

        return left, top, right, bottom

    def _capture_screenshot(self, bounds: Tuple[int, int, int, int]) -> Any:
        left, top, right, bottom = bounds
        return pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    def _extract_text_from_screenshot(self, screenshot: Any) -> Optional[str]:
        """スクリーンショットからテキストを抽出、失敗時は None"""
        try:
            text = self.ocr_service.perform_ocr(screenshot)
            if not text.strip():
                messagebox.showwarning(
                    UILabels.TITLE_OCR_RESULT, UIMessages.WARN_NO_TEXT_DETECTED
                )
                return None
            return text
        except Exception as ocr_error:
            messagebox.showerror(
                UILabels.TITLE_OCR_ERROR,
                UIMessages.ERR_OCR_DETECT.format(error=str(ocr_error)),
            )
            return None

    def _process_screenshot(self) -> None:
        """スクリーンショットを処理してテキストを抽出し result_text に格納"""
        try:
            bounds = self._get_screenshot_bounds()
            if bounds is None:
                messagebox.showwarning(
                    UILabels.TITLE_OCR_RESULT, UIMessages.WARN_SCREENSHOT_TOO_SMALL
                )
                return

            screenshot = self._capture_screenshot(bounds)
            text = self._extract_text_from_screenshot(screenshot)
            if text is not None:
                self.result_text = text

        except Exception as e:
            messagebox.showerror(
                UILabels.TITLE_CAPTURE_ERROR,
                UIMessages.ERR_CAPTURE_PROCESS.format(error=str(e)),
            )
