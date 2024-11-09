import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
import pytesseract
from service_ocr import perform_ocr, initialize_tesseract, get_tesseract_path
from config_manager import ConfigManager


@pytest.fixture
def mock_config():
    with patch('service_ocr.ConfigManager') as mock:
        config_instance = MagicMock()
        config_instance.get_tesseract_path.return_value = '/mock/tesseract/path'
        mock.return_value = config_instance
        yield mock


@pytest.fixture
def mock_image():
    # テスト用の空のPIL Imageを作成
    return Image.new('RGB', (100, 100), color='white')


def test_get_tesseract_path(mock_config):
    """Tesseractのパス取得機能のテスト"""
    # 期待されるパスを取得できることを確認
    path = get_tesseract_path()
    assert path == '/mock/tesseract/path'
    mock_config.return_value.get_tesseract_path.assert_called_once()


def test_initialize_tesseract(mock_config):
    """Tesseractの初期化機能のテスト"""
    initialize_tesseract()
    # pytesseractのパスが正しく設定されていることを確認
    assert pytesseract.pytesseract.tesseract_cmd == '/mock/tesseract/path'


def test_perform_ocr_success(mock_image):
    """OCR処理の成功ケースのテスト"""
    expected_text = "テストテキスト"

    with patch('pytesseract.image_to_string') as mock_ocr:
        mock_ocr.return_value = expected_text
        result = perform_ocr(mock_image)

        assert result == expected_text
        mock_ocr.assert_called_once_with(mock_image, lang='jpn+eng')


def test_perform_ocr_empty_result(mock_image):
    """OCR処理で空のテキストが返された場合のテスト"""
    with patch('pytesseract.image_to_string') as mock_ocr:
        mock_ocr.return_value = "   "  # 空白文字のみ

        with pytest.raises(RuntimeError) as exc_info:
            perform_ocr(mock_image)

        assert "テキストを抽出できませんでした" in str(exc_info.value)


def test_perform_ocr_initialization_error():
    """Tesseract初期化エラー時のテスト"""
    with patch('service_ocr.initialize_tesseract') as mock_init:
        mock_init.side_effect = FileNotFoundError("Tesseract not found")

        with pytest.raises(RuntimeError) as exc_info:
            perform_ocr(Image.new('RGB', (100, 100)))

        assert "Tesseractの初期化に失敗しました" in str(exc_info.value)


def test_perform_ocr_unexpected_error(mock_image):
    """予期せぬエラー発生時のテスト"""
    with patch('pytesseract.image_to_string') as mock_ocr:
        mock_ocr.side_effect = Exception("Unexpected error")

        with pytest.raises(RuntimeError) as exc_info:
            perform_ocr(mock_image)

        assert "予期せぬエラーが発生しました" in str(exc_info.value)
