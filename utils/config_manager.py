"""設定ファイル管理モジュール

このモジュールは、config.iniファイルの読み書きを管理します。
設定の取得、保存、検証を行う機能を提供します。
"""

# 標準ライブラリ
import configparser
import os
import sys
from pathlib import Path
from typing import Final, List, Tuple


class ConfigError(Exception):
    """設定ファイル関連のエラー
    
    設定ファイルの読み込み、書き込み、検証時に発生するエラーを表します。
    """
    pass


def get_config_path() -> Path:
    """設定ファイルのパスを取得
    
    PyInstallerでビルドされた実行ファイルの場合は、
    一時ディレクトリ（sys._MEIPASS）から設定ファイルを読み込みます。
    それ以外の場合は、このファイルと同じディレクトリから読み込みます。
    
    Returns:
        Path: 設定ファイルのパス
    """
    base_path: Path = Path(
        sys._MEIPASS if getattr(sys, 'frozen', False) 
        else os.path.dirname(__file__)
    )
    return base_path / 'config.ini'


CONFIG_PATH: Final[Path] = get_config_path()


class ConfigManager:
    """設定管理クラス
    
    config.iniファイルの読み書きと設定値の管理を行います。
    
    Attributes:
        config_file (Path): 設定ファイルのパス
        config (ConfigParser): 設定パーサー
    """
    
    def __init__(self, config_file: Path | str = CONFIG_PATH) -> None:
        """ConfigManagerを初期化
        
        Args:
            config_file: 設定ファイルのパス（デフォルト: CONFIG_PATH）
        """
        self.config_file: Path = Path(config_file)
        self.config: configparser.ConfigParser = configparser.ConfigParser()
        self.load_config()

    def load_config(self) -> None:
        """設定ファイルを読み込む
        
        UTF-8エンコーディングで読み込みを試み、失敗した場合は
        CP932エンコーディングでリトライします。
        
        Raises:
            ConfigError: 設定ファイルの読み込みに失敗した場合
        """
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
        """設定をファイルに保存
        
        Raises:
            ConfigError: 設定ファイルの保存に失敗した場合
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as configfile:
                self.config.write(configfile)
        except (IOError, OSError) as e:
            raise ConfigError(f"Failed to save config: {e}") from e

    def get_window_geometry(self) -> List[int]:
        """ウィンドウのジオメトリ設定を取得
        
        Returns:
            List[int]: [x座標, y座標, 幅, 高さ]
            
        Raises:
            ConfigError: ジオメトリ設定の形式が無効な場合
        """
        try:
            geometry: str = self.config.get(
                'WindowSettings', 
                'geometry', 
                fallback='100,100,800,600'
            )
            return [int(val) for val in geometry.split(',')]
        except ValueError as e:
            raise ConfigError(f"Invalid window geometry format: {e}") from e

    def get_font_size(self) -> int:
        """フォントサイズを取得
        
        Returns:
            int: フォントサイズ（デフォルト: 12）
        """
        return self.config.getint('WindowSettings', 'font_size', fallback=12)

    def get_screen_capture_settings(self) -> Tuple[float, int]:
        """スクリーンキャプチャの設定を取得
        
        Returns:
            Tuple[float, int]: (透明度, 枠線の幅)
            
        Raises:
            ConfigError: 設定値が無効な場合
        """
        try:
            transparency: float = self.config.getfloat(
                'ScreenCapture', 
                'transparency', 
                fallback=0.2
            )
            outline_width: int = self.config.getint(
                'ScreenCapture', 
                'selection_outline_width', 
                fallback=2
            )
            return transparency, outline_width
        except ValueError as e:
            raise ConfigError(f"Invalid screen capture settings: {e}") from e

    def get_input_mode(self) -> bool:
        """入力モード（追記/上書き）を取得
        
        Returns:
            bool: True=追記モード, False=上書きモード
        """
        return self.config.getboolean('WindowSettings', 'append_mode', fallback=True)

    def set_window_geometry(self, x: int, y: int, width: int, height: int) -> None:
        """ウィンドウのジオメトリ設定を保存
        
        Args:
            x: X座標
            y: Y座標
            width: 幅
            height: 高さ
        """
        self._ensure_section('WindowSettings')
        self.config['WindowSettings']['geometry'] = f"{x},{y},{width},{height}"
        self.save_config()

    def set_font_size(self, size: int) -> None:
        """フォントサイズを保存
        
        Args:
            size: フォントサイズ
            
        Raises:
            ValueError: サイズが0以下の場合
        """
        if size <= 0:
            raise ValueError("Font size must be positive")
        self._ensure_section('WindowSettings')
        self.config['WindowSettings']['font_size'] = str(size)
        self.save_config()

    def set_screen_capture_settings(self, transparency: float, outline_width: int) -> None:
        """スクリーンキャプチャの設定を保存
        
        Args:
            transparency: 透明度（0.0～1.0）
            outline_width: 枠線の幅（ピクセル）
            
        Raises:
            ValueError: 設定値が範囲外の場合
        """
        if not 0 <= transparency <= 1:
            raise ValueError("Transparency must be between 0 and 1")
        if outline_width <= 0:
            raise ValueError("Outline width must be positive")

        self._ensure_section('ScreenCapture')
        self.config['ScreenCapture']['transparency'] = str(transparency)
        self.config['ScreenCapture']['selection_outline_width'] = str(outline_width)
        self.save_config()

    def set_input_mode(self, is_append: bool) -> None:
        """入力モードを保存
        
        Args:
            is_append: True=追記モード, False=上書きモード
        """
        self._ensure_section('WindowSettings')
        self.config['WindowSettings']['append_mode'] = str(is_append)
        self.save_config()

    def _ensure_section(self, section: str) -> None:
        """設定セクションが存在することを確認し、必要に応じて作成
        
        Args:
            section: セクション名
        """
        if section not in self.config:
            self.config[section] = {}
