import configparser
import os
import sys
from pathlib import Path
from typing import Final, List, Tuple, Optional


def get_config_path() -> Path:
    """設定ファイルのパスを取得する"""
    base_path: Path = Path(sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__))
    return base_path / 'config.ini'


CONFIG_PATH: Final[Path] = get_config_path()


class ConfigManager:
    def __init__(self, config_file: Path | str = CONFIG_PATH) -> None:
        self.config_file: Path = Path(config_file)
        self.config: configparser.ConfigParser = configparser.ConfigParser()
        self.load_config()

    def load_config(self) -> None:
        """設定ファイルを読み込む"""
        if not self.config_file.exists():
            return

        try:
            self.config.read(self.config_file, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                # UTF-8以外のエンコーディングで試行
                content: str = self.config_file.read_bytes().decode('cp932')
                self.config.read_string(content)
            except (UnicodeDecodeError, OSError) as e:
                raise ConfigError(f"Failed to load config: {e}") from e

    def save_config(self) -> None:
        """設定ファイルを保存する"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as configfile:
                self.config.write(configfile)
        except (IOError, OSError) as e:
            raise ConfigError(f"Failed to save config: {e}") from e

    def get_window_geometry(self) -> List[int]:
        """ウィンドウの位置とサイズを取得する"""
        try:
            geometry: str = self.config.get('WindowSettings', 'geometry', fallback='100,100,800,600')
            return [int(val) for val in geometry.split(',')]
        except ValueError as e:
            raise ConfigError(f"Invalid window geometry format: {e}") from e

    def get_font_size(self) -> int:
        """フォントサイズを取得する"""
        return self.config.getint('WindowSettings', 'font_size', fallback=12)

    def get_screen_capture_settings(self) -> Tuple[float, int]:
        """画面キャプチャの設定を取得する"""
        try:
            transparency: float = self.config.getfloat('ScreenCapture', 'transparency', fallback=0.2)
            outline_width: int = self.config.getint('ScreenCapture', 'selection_outline_width', fallback=2)
            return transparency, outline_width
        except ValueError as e:
            raise ConfigError(f"Invalid screen capture settings: {e}") from e

    def get_tesseract_path(self) -> str:
        """Tesseractの実行ファイルパスを取得する"""
        return self.config.get('Paths', 'tesseract_path', 
                             fallback=r'C:\Program Files\Tesseract-OCR\tesseract.exe')

    def get_input_mode(self) -> bool:
        """入力モード（追記/上書き）の設定を取得する"""
        return self.config.getboolean('WindowSettings', 'append_mode', fallback=True)

    def set_window_geometry(self, x: int, y: int, width: int, height: int) -> None:
        """ウィンドウの位置とサイズを設定する"""
        self._ensure_section('WindowSettings')
        self.config['WindowSettings']['geometry'] = f"{x},{y},{width},{height}"
        self.save_config()

    def set_font_size(self, size: int) -> None:
        """フォントサイズを設定する"""
        if size <= 0:
            raise ValueError("Font size must be positive")
        self._ensure_section('WindowSettings')
        self.config['WindowSettings']['font_size'] = str(size)
        self.save_config()

    def set_screen_capture_settings(self, transparency: float, outline_width: int) -> None:
        """画面キャプチャの設定を保存する"""
        if not 0 <= transparency <= 1:
            raise ValueError("Transparency must be between 0 and 1")
        if outline_width <= 0:
            raise ValueError("Outline width must be positive")

        self._ensure_section('ScreenCapture')
        self.config['ScreenCapture']['transparency'] = str(transparency)
        self.config['ScreenCapture']['selection_outline_width'] = str(outline_width)
        self.save_config()

    def set_tesseract_path(self, path: str | Path) -> None:
        """Tesseractの実行ファイルパスを設定する"""
        path_obj: Path = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Tesseract executable not found at: {path}")

        self._ensure_section('Paths')
        self.config['Paths']['tesseract_path'] = str(path_obj)
        self.save_config()

    def set_input_mode(self, is_append: bool) -> None:
        """入力モード（追記/上書き）の設定を保存する"""
        self._ensure_section('WindowSettings')
        self.config['WindowSettings']['append_mode'] = str(is_append)
        self.save_config()

    def _ensure_section(self, section: str) -> None:
        """設定セクションが存在することを確認し、必要に応じて作成する"""
        if section not in self.config:
            self.config[section] = {}
