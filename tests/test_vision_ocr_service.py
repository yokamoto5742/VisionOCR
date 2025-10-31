import io

import pytest
from unittest.mock import Mock, patch

from google.cloud import vision
from PIL import Image

from service.vision_ocr_service import VisionOCRService


@pytest.fixture
def mock_vision_client():
    with patch('service.vision_ocr_service.vision.ImageAnnotatorClient') as mock_client:
        yield mock_client


@pytest.fixture
def vision_service(mock_vision_client):
    # from_service_account_infoの戻り値を設定
    mock_instance = Mock()
    mock_vision_client.from_service_account_info.return_value = mock_instance
    return VisionOCRService()


@pytest.fixture
def sample_image():
    # テスト用の空のPIL Imageを作成
    return Image.new('RGB', (100, 100), color='white')


def test_successful_ocr(vision_service, mock_vision_client, sample_image):
    # モックレスポンスの設定
    mock_response = Mock()
    # errorオブジェクトのmessageを空文字列に設定（Falsy）
    mock_error = Mock()
    mock_error.message = ""
    mock_response.error = mock_error

    mock_annotation = Mock()
    mock_annotation.description = "テストテキスト"
    mock_response.text_annotations = [mock_annotation]

    # クライアントのtext_detectionメソッドの戻り値を設定
    instance = mock_vision_client.from_service_account_info.return_value
    instance.text_detection.return_value = mock_response

    # OCR実行
    result = vision_service.perform_ocr(sample_image)

    # アサーション
    assert result == "テストテキスト"
    assert instance.text_detection.called


def test_api_error(vision_service, mock_vision_client, sample_image):
    # エラーレスポンスの設定
    mock_response = Mock()
    mock_error = Mock()
    mock_error.message = "API エラー"
    mock_response.error = mock_error

    instance = mock_vision_client.from_service_account_info.return_value
    instance.text_detection.return_value = mock_response

    # エラーが発生することを確認
    with pytest.raises(RuntimeError) as exc_info:
        vision_service.perform_ocr(sample_image)

    assert "Vision API エラー" in str(exc_info.value)


def test_no_text_detected(vision_service, mock_vision_client, sample_image):
    # テキストが検出されないケース
    mock_response = Mock()
    # errorオブジェクトのmessageを空文字列に設定（Falsy）
    mock_error = Mock()
    mock_error.message = ""
    mock_response.error = mock_error
    mock_response.text_annotations = []

    instance = mock_vision_client.from_service_account_info.return_value
    instance.text_detection.return_value = mock_response

    with pytest.raises(RuntimeError) as exc_info:
        vision_service.perform_ocr(sample_image)

    assert "OCR処理中にエラーが発生しました: テキストを検出できませんでした" in str(exc_info.value)


def test_empty_text_detected(vision_service, mock_vision_client, sample_image):
    # 空のテキストが検出されるケース
    mock_response = Mock()
    # errorオブジェクトのmessageを空文字列に設定（Falsy）
    mock_error = Mock()
    mock_error.message = ""
    mock_response.error = mock_error

    mock_annotation = Mock()
    mock_annotation.description = "   "  # 空白文字のみ
    mock_response.text_annotations = [mock_annotation]

    instance = mock_vision_client.from_service_account_info.return_value
    instance.text_detection.return_value = mock_response

    with pytest.raises(RuntimeError) as exc_info:
        vision_service.perform_ocr(sample_image)

    assert "OCR処理中にエラーが発生しました: テキストを抽出できませんでした" in str(exc_info.value)


def test_client_initialization_error():
    # クライアント初期化エラーのテスト
    with patch('service.vision_ocr_service.vision.ImageAnnotatorClient.from_service_account_info', side_effect=Exception("初期化エラー")):
        with pytest.raises(RuntimeError) as exc_info:
            VisionOCRService()

        assert "Vision APIクライアントの初期化に失敗しました" in str(exc_info.value)
