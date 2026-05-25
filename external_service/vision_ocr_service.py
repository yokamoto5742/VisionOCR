import io

from google.cloud import vision
from PIL import Image

from utils.config_manager import ConfigManager
from utils.constants import UIMessages
from utils.env_loader import get_google_credentials


class VisionOCRService:
    """Google Cloud Vision APIを使用したOCR処理"""

    def __init__(self) -> None:
        try:
            credentials = get_google_credentials()
            self.client = vision.ImageAnnotatorClient.from_service_account_info(
                credentials
            )
        except Exception as e:
            raise RuntimeError(UIMessages.ERR_VISION_CLIENT_INIT.format(error=e))
        config = ConfigManager()
        self._detection_type = config.get_detection_type()

    def perform_ocr(self, image: Image.Image) -> str:
        """画像からテキストを抽出"""
        try:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format or "PNG")
            content = img_byte_arr.getvalue()

            vision_image = vision.Image(content=content)

            detect = getattr(self.client, self._detection_type)
            response = detect(image=vision_image)  # type: ignore[attr-defined]

            if response.error.message:
                raise RuntimeError(
                    UIMessages.ERR_VISION_API.format(error=response.error.message)
                )

            if not response.text_annotations:
                raise ValueError(UIMessages.ERR_OCR_NO_TEXT)

            extracted_text = response.text_annotations[0].description

            if not extracted_text.strip():
                raise ValueError(UIMessages.ERR_OCR_NO_EXTRACT)

            return extracted_text

        except Exception as e:
            raise RuntimeError(UIMessages.ERR_OCR_PROCESS.format(error=e))
