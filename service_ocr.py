from typing import Optional
from pathlib import Path
from PIL import Image
import pytesseract
from config_manager import ConfigManager


def get_tesseract_path() -> str:
    config = ConfigManager()
    return config.get_tesseract_path()

def initialize_tesseract() -> None:
    pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

def perform_ocr(image: Image.Image) -> str:
    try:
        initialize_tesseract()
    except (FileNotFoundError, PermissionError) as e:
        raise RuntimeError(f"Tesseractの初期化に失敗しました: {e}")

    try:
        text = pytesseract.image_to_string(image, lang='jpn+eng')
        if not text.strip():
            raise ValueError("テキストを抽出できませんでした")
        return text
    except Exception as e:
        raise RuntimeError(f"予期せぬエラーが発生しました: {e}")
