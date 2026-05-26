from typing import cast

import fitz  # PyMuPDF
from PIL import Image

from external_service.vision_ocr_service import VisionOCRService
from utils.constants import UIMessages


def _render_page_to_image(page: fitz.Page) -> Image.Image:
    """PDFページをPIL Imageへ変換"""
    pixmap = page.get_pixmap()
    return Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)


def _ocr_page(page: fitz.Page, ocr_service: VisionOCRService) -> str:
    """単一ページをOCR処理（失敗時はフェイルバック文言を返す）"""
    try:
        image = _render_page_to_image(page)
        return ocr_service.perform_ocr(image)
    except Exception:
        return UIMessages.PDF_OCR_FAILED


def process_pdf_files(
    pdf_paths: list[str],
    ocr_service: VisionOCRService,
) -> str:
    """複数PDFファイルの全ページをOCR処理してテキストを返す"""
    all_parts: list[str] = []

    for pdf_path in pdf_paths:
        with fitz.open(pdf_path) as doc:
            for page_num, page in enumerate(cast(list[fitz.Page], doc), 1):
                footer = UIMessages.PDF_PAGE_FOOTER.format(page_num=page_num)
                text = _ocr_page(page, ocr_service)
                all_parts.append(f"{text}\n{footer}")

    return "\n\n".join(all_parts)
