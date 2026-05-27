import tkinter as tk
from tkinter import TclError, filedialog, messagebox, scrolledtext
from typing import List

from app.app_screen_capture import ScreenCapture
from external_service.vision_ocr_service import VisionOCRService
from service import text_widget_utils
from service.file_saver import save_text_to_file
from service.pdf_processor import process_pdf_files
from utils.config_manager import ConfigManager
from utils.constants import (
    DEFAULT_APP_TITLE,
    DEFAULT_FONT_FAMILY,
    UILabels,
    UILayout,
    UIMessages,
)
from widgets.button_factory import ButtonConfig, create_buttons

# 表示ラベルとAPIパラメータのマッピング
_DETECTION_LABEL_TO_TYPE = {
    UILabels.DETECTION_TEXT: "text_detection",
    UILabels.DETECTION_DOCUMENT: "document_text_detection",
}
_DETECTION_TYPE_TO_LABEL = {v: k for k, v in _DETECTION_LABEL_TO_TYPE.items()}


class OCRApplication:
    """Google Cloud Vision APIを使用したOCRアプリケーションのメインUI"""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.config_manager = ConfigManager()
        self.root.title(
            self.config_manager.config.get(
                "WindowSettings", "app_title", fallback=DEFAULT_APP_TITLE
            )
        )
        self.is_append_mode = self.config_manager.get_input_mode()
        self._detection_type = self.config_manager.get_detection_type()
        self._initialize_application()

    def _initialize_application(self) -> None:
        self._setup_window_geometry()
        self._create_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def _setup_window_geometry(self) -> None:
        try:
            geometry = self.config_manager.get_window_geometry()
            width = geometry[2] - geometry[0]
            height = geometry[3] - geometry[1]
            position_x = geometry[0]
            position_y = geometry[1]
            self.root.geometry(f"{width}x{height}+{position_x}+{position_y}")
        except (AttributeError, IndexError) as e:
            messagebox.showerror(
                UILabels.TITLE_ERROR,
                UIMessages.ERR_WINDOW_CONFIG_LOAD.format(error=str(e)),
            )
            self.root.geometry("800x600+100+100")

    def _create_gui(self) -> None:
        self._create_top_buttons()
        self._create_text_area()
        self._create_bottom_buttons()

    def _on_mode_change(self, value: str) -> None:
        """プルダウンでモードが変更されたときの処理"""
        self.is_append_mode = value == UILabels.MODE_APPEND
        self.config_manager.set_input_mode(self.is_append_mode)

    def _on_detection_type_change(self, value: str) -> None:
        """検出タイプのプルダウンが変更されたときの処理"""
        self._detection_type = _DETECTION_LABEL_TO_TYPE[value]
        self.config_manager.set_detection_type(self._detection_type)

    def _create_top_buttons(self) -> None:
        button_frame = tk.Frame(self.root)
        button_frame.pack(
            fill=tk.X, padx=UILayout.FRAME_PADDING, pady=UILayout.FRAME_PADDING
        )

        top_buttons: List[ButtonConfig] = [
            ButtonConfig(UILabels.BTN_CAPTURE, self.capture_screen, is_highlight=True),
            ButtonConfig(UILabels.BTN_SELECT_FILE, self.select_pdf_files),
            ButtonConfig(UILabels.BTN_COPY_ALL, self.copy_to_clipboard),
            ButtonConfig(UILabels.BTN_SAVE_FILE, self.save_to_file),
            ButtonConfig(UILabels.BTN_CLEAR, self.clear_screen),
        ]

        create_buttons(button_frame, top_buttons)

        initial_detection_label = _DETECTION_TYPE_TO_LABEL.get(
            self._detection_type, UILabels.DETECTION_TEXT
        )
        self.detection_var = tk.StringVar(
            master=self.root, value=initial_detection_label
        )
        self.detection_menu = tk.OptionMenu(
            button_frame,
            self.detection_var,
            UILabels.DETECTION_TEXT,
            UILabels.DETECTION_DOCUMENT,
            command=self._on_detection_type_change,
        )
        self.detection_menu.pack(side=tk.LEFT, padx=UILayout.BUTTON_PADDING)

        initial_mode = (
            UILabels.MODE_APPEND if self.is_append_mode else UILabels.MODE_OVERWRITE
        )
        self.mode_var = tk.StringVar(master=self.root, value=initial_mode)
        self.mode_menu = tk.OptionMenu(
            button_frame,
            self.mode_var,
            UILabels.MODE_APPEND,
            UILabels.MODE_OVERWRITE,
            command=self._on_mode_change,
        )
        self.mode_menu.pack(side=tk.LEFT, padx=UILayout.BUTTON_PADDING)

    def _create_text_area(self) -> None:
        try:
            font_family = self.config_manager.config.get(
                "WindowSettings", "font_family", fallback=DEFAULT_FONT_FAMILY
            )
            font_size = self.config_manager.get_font_size()

            self.text_area = scrolledtext.ScrolledText(
                self.root, wrap=tk.WORD, font=(font_family, font_size)
            )
            self.text_area.pack(
                expand=True,
                fill="both",
                padx=UILayout.FRAME_PADDING,
                pady=UILayout.FRAME_PADDING,
            )
        except Exception as e:
            messagebox.showerror(
                UILabels.TITLE_ERROR,
                UIMessages.ERR_TEXT_AREA_CREATE.format(error=str(e)),
            )
            raise

    def _create_bottom_buttons(self) -> None:
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(
            fill=tk.X, padx=UILayout.FRAME_PADDING, pady=UILayout.FRAME_PADDING
        )

        bottom_buttons: List[ButtonConfig] = [
            ButtonConfig(
                UILabels.BTN_REMOVE_COMMA,
                lambda: text_widget_utils.remove_punctuation(self.text_area, "、"),
            ),
            ButtonConfig(
                UILabels.BTN_REMOVE_PERIOD,
                lambda: text_widget_utils.remove_punctuation(self.text_area, "。"),
            ),
            ButtonConfig(
                UILabels.BTN_REMOVE_LINEBREAK,
                lambda: text_widget_utils.remove_linebreaks(self.text_area),
            ),
            ButtonConfig(
                UILabels.BTN_REMOVE_SPACE,
                lambda: text_widget_utils.remove_spaces(self.text_area),
            ),
            ButtonConfig(
                UILabels.BTN_REMOVE_SEPARATOR,
                lambda: text_widget_utils.remove_page_separators(self.text_area),
            ),
            ButtonConfig(UILabels.BTN_CLOSE, self.root.destroy),
        ]

        create_buttons(bottom_frame, bottom_buttons)

    def capture_screen(self) -> None:
        """画面の一部をキャプチャしてOCR処理を実行"""
        try:
            self.root.iconify()
            screen_capture = ScreenCapture()
            screen_capture.root.mainloop()
            self.root.deiconify()

            if screen_capture.result_text:
                text_widget_utils.set_text_content(
                    self.text_area,
                    screen_capture.result_text,
                    append=self.is_append_mode,
                )

        except Exception as e:
            messagebox.showerror(
                UILabels.TITLE_ERROR,
                UIMessages.ERR_UNEXPECTED.format(error=str(e)),
            )

    def copy_to_clipboard(self) -> None:
        try:
            text = text_widget_utils.get_text_content(self.text_area)
            if not text:
                messagebox.showwarning(
                    UILabels.TITLE_WARNING, UIMessages.WARN_NO_COPY_TEXT
                )
                return

            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()

            messagebox.showinfo(UILabels.TITLE_INFO, UIMessages.INFO_COPY_DONE)

        except TclError as e:
            messagebox.showerror(
                UILabels.TITLE_ERROR,
                UIMessages.ERR_CLIPBOARD_TCL.format(error=str(e)),
            )
        except Exception as e:
            messagebox.showerror(
                UILabels.TITLE_ERROR,
                UIMessages.ERR_CLIPBOARD_COPY.format(error=str(e)),
            )

    def save_to_file(self) -> None:
        try:
            text = text_widget_utils.get_text_content(self.text_area)
            if text:
                save_text_to_file(text)
        except Exception as e:
            messagebox.showerror(
                UILabels.TITLE_ERROR,
                UIMessages.ERR_FILE_SAVE.format(error=str(e)),
            )

    def select_pdf_files(self) -> None:
        """PDFファイルを選択してOCR処理を実行"""
        pdf_paths = filedialog.askopenfilenames(
            title=UILabels.PDF_DIALOG_TITLE,
            filetypes=[(UILabels.PDF_FILETYPE_LABEL, "*.pdf")],
        )
        if not pdf_paths:
            return

        try:
            ocr_service = VisionOCRService()
            max_pages = self.config_manager.get_pdf_max_pages()
            text = process_pdf_files(list(pdf_paths), ocr_service, max_pages)
            text_widget_utils.set_text_content(
                self.text_area, text, append=self.is_append_mode
            )
        except Exception as e:
            messagebox.showerror(
                UILabels.TITLE_ERROR,
                UIMessages.ERR_PDF_PROCESS.format(error=str(e)),
            )

    def clear_screen(self) -> None:
        try:
            text_widget_utils.clear_text(self.text_area)
        except TclError as e:
            messagebox.showerror(
                UILabels.TITLE_ERROR,
                UIMessages.ERR_CLEAR_SCREEN.format(error=str(e)),
            )
