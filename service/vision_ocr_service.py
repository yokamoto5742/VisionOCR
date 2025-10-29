import io
from pathlib import Path
from typing import Optional

from google.cloud import vision
from PIL import Image

from utils.config_manager import ConfigManager

class VisionOCRService:
    def __init__(self):
        try:
            self.client = vision.ImageAnnotatorClient()
        except Exception as e:
            raise RuntimeError(f"Vision APIクライアントの初期化に失敗しました: {e}")

    def perform_ocr(self, image: Image.Image) -> str:
        try:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format or 'PNG')
            content = img_byte_arr.getvalue()

            vision_image = vision.Image(content=content)

            response = self.client.text_detection(image=vision_image)

            if response.error.message:
                raise RuntimeError(
                    f"Vision API エラー: {response.error.message}"
                )

            if not response.text_annotations:
                raise ValueError("テキストを検出できませんでした")

            extracted_text = response.text_annotations[0].description
            
            if not extracted_text.strip():
                raise ValueError("テキストを抽出できませんでした")
                
            return extracted_text

        except Exception as e:
            raise RuntimeError(f"OCR処理中にエラーが発生しました: {e}")
