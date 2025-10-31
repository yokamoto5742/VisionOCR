import tkinter as tk
from tkinter import TclError, messagebox, scrolledtext
from typing import List

from app.app_screen_capture import ScreenCapture
from service import text_widget_utils
from service.file_saver import save_text_to_file
from utils.config_manager import ConfigManager
from utils.constants import TextPosition, UILayout
from widgets.button_factory import ButtonConfig, create_buttons


class OCRApplication:
    """Google Cloud Vision APIを使用したOCRアプリケーションのメインGUI"""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.config_manager = ConfigManager()
        self.root.title(self.config_manager.config.get('WindowSettings', 'app_title', fallback='VisionOCR'))
        self.is_append_mode = self.config_manager.get_input_mode()
        self._initialize_application()

    def _initialize_application(self) -> None:
        self._setup_window_geometry()
        self._create_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

    def _setup_window_geometry(self) -> None:
        try:
            geometry = self.config_manager.get_window_geometry()
            width = geometry[2] - geometry[0]
            height = geometry[3] - geometry[1]
            position_x = geometry[0]
            position_y = geometry[1]
            self.root.geometry(f"{width}x{height}+{position_x}+{position_y}")
        except (AttributeError, IndexError) as e:
            messagebox.showerror("エラー", f"ウィンドウ設定の読み込みに失敗: {str(e)}")
            self.root.geometry("800x600+100+100")  # デフォルト値

    def _create_gui(self) -> None:
        self._create_top_buttons()
        self._create_text_area()
        self._create_bottom_buttons()

    def toggle_input_mode(self) -> None:
        """OCR結果の入力モードを追記と上書きで切り替え"""
        self.is_append_mode = not self.is_append_mode
        self.config_manager.set_input_mode(self.is_append_mode)  # 設定を保存
        mode_text = "追記" if self.is_append_mode else "上書き"
        self.mode_button.config(text=f"{mode_text}モード")

    def _create_top_buttons(self) -> None:
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=UILayout.FRAME_PADDING, pady=UILayout.FRAME_PADDING)

        top_buttons: List[ButtonConfig] = [
            ButtonConfig("OCR範囲選択", self.capture_screen, is_highlight=True),
            ButtonConfig("全文コピー", self.copy_to_clipboard),
            ButtonConfig("ファイル出力", self.save_to_file),
            ButtonConfig("テキストクリア", self.clear_screen),
        ]

        create_buttons(button_frame, top_buttons)

        mode_text = "追記" if self.is_append_mode else "上書き"
        self.mode_button = tk.Button(
            button_frame,
            text=f"{mode_text}モード",
            command=self.toggle_input_mode
        )
        self.mode_button.pack(side=tk.LEFT, padx=UILayout.BUTTON_PADDING)

    def _create_text_area(self) -> None:
        try:
            font_family = self.config_manager.config.get(
                'WindowSettings',
                'font_family',
                fallback='MS Gothic'
            )
            font_size = self.config_manager.get_font_size()

            self.text_area = scrolledtext.ScrolledText(
                self.root,
                wrap=tk.WORD,
                font=(font_family, font_size)
            )
            self.text_area.pack(expand=True, fill='both', padx=UILayout.FRAME_PADDING, pady=UILayout.FRAME_PADDING)
        except Exception as e:
            messagebox.showerror("エラー", f"テキストエリアの作成に失敗: {str(e)}")
            raise

    def _create_bottom_buttons(self) -> None:
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=UILayout.FRAME_PADDING, pady=UILayout.FRAME_PADDING)

        bottom_buttons: List[ButtonConfig] = [
            ButtonConfig("読点除去", lambda: text_widget_utils.remove_punctuation(self.text_area, '、')),
            ButtonConfig("句点除去", lambda: text_widget_utils.remove_punctuation(self.text_area, '。')),
            ButtonConfig("改行除去", lambda: text_widget_utils.remove_linebreaks(self.text_area)),
            ButtonConfig("スペース除去", lambda: text_widget_utils.remove_spaces(self.text_area)),
            ButtonConfig("閉じる", self.root.quit)
        ]

        create_buttons(bottom_frame, bottom_buttons)

    def capture_screen(self) -> None:
        """画面の一部をキャプチャしてOCR処理を実行"""
        try:
            self.root.iconify()
            screen_capture = ScreenCapture()
            screen_capture.root.mainloop()
            self.root.deiconify()

            try:
                text = self.root.clipboard_get()
                if text:
                    if not self.is_append_mode:
                        self.text_area.delete(TextPosition.START, TextPosition.END)
                    elif self.text_area.get(TextPosition.START, TextPosition.END).strip():
                        self.text_area.insert(TextPosition.END, "\n")
                    self.text_area.insert(TextPosition.END, text)
            except tk.TclError:
                pass # _process_screenshot でエラー処理済み

        except Exception as e:
            messagebox.showerror("エラー", f"予期せぬエラーが発生: {str(e)}")

    def copy_to_clipboard(self) -> None:
        try:
            text = self.text_area.get(TextPosition.START, TextPosition.END).strip()
            if not text:
                messagebox.showwarning("警告", "コピーするテキストがありません。")
                return

            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()

            messagebox.showinfo("完了", "テキストをクリップボードにコピーしました。")

        except TclError as e:
            messagebox.showerror("エラー", f"Tclエラー: クリップボードへのアクセスに失敗しました。\n{str(e)}")
        except Exception as e:
            messagebox.showerror("エラー", f"クリップボードへのコピーに失敗: {str(e)}")


    def save_to_file(self) -> None:
        try:
            text = self.text_area.get(TextPosition.START, TextPosition.END).strip()
            if text:
                save_text_to_file(text)
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルの保存に失敗: {str(e)}")

    def clear_screen(self) -> None:
        try:
            self.text_area.delete(TextPosition.START, TextPosition.END)
        except TclError as e:
            messagebox.showerror("エラー", f"画面のクリアに失敗: {str(e)}")
