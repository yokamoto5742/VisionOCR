from pathlib import Path
from typing import Optional

from pdf2image import convert_from_path

from external_service.vision_ocr_service import VisionOCRService

_PAGE_HEADER = "--- {file_name} / ページ{page_num} ---"
_OCR_FAILED = "[テキストを検出できませんでした]"


def process_pdf_files(
    pdf_paths: list[str],
    ocr_service: VisionOCRService,
    poppler_path: Optional[str] = None,
) -> str:
    """複数PDFファイルの全ページをOCR処理してテキストを返す"""
    poppler = poppler_path if poppler_path else None
    all_parts: list[str] = []

    for pdf_path in pdf_paths:
        file_name = Path(pdf_path).name
        images = convert_from_path(pdf_path, poppler_path=poppler)

        for page_num, image in enumerate(images, 1):
            header = _PAGE_HEADER.format(file_name=file_name, page_num=page_num)
            try:
                text = ocr_service.perform_ocr(image)
            except Exception:
                text = _OCR_FAILED
            all_parts.append(f"{header}\n{text}")

    return "\n\n".join(all_parts)
