import fitz  # PyMuPDF
from PIL import Image

from external_service.vision_ocr_service import VisionOCRService

_PAGE_HEADER = "--- ページ{page_num} ---"
_OCR_FAILED = "[テキストを検出できませんでした]"


def process_pdf_files(
    pdf_paths: list[str],
    ocr_service: VisionOCRService,
) -> str:
    """複数PDFファイルの全ページをOCR処理してテキストを返す"""
    all_parts: list[str] = []

    for pdf_path in pdf_paths:
        doc = fitz.open(pdf_path)

        for page_num, page in enumerate(doc, 1):
            header = _PAGE_HEADER.format(page_num=page_num)
            try:
                pixmap = page.get_pixmap()
                image = Image.frombytes(
                    "RGB", [pixmap.width, pixmap.height], pixmap.samples
                )
                text = ocr_service.perform_ocr(image)
            except Exception:
                text = _OCR_FAILED
            all_parts.append(f"{header}\n{text}")

        doc.close()

    return "\n\n".join(all_parts)
