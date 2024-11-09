import pytest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk
from PIL import Image
import pyautogui
from app_screen_capture import ScreenCapture


@pytest.fixture
def mock_tk():
    with patch('tkinter.Tk') as mock:
        # Tkインスタンスのモック作成
        tk_instance = mock.return_value
        tk_instance.winfo_screenwidth.return_value = 1920
        tk_instance.winfo_screenheight.return_value = 1080

        # Canvasのモック作成
        canvas_mock = MagicMock()
        tk_instance.Canvas.return_value = canvas_mock

        yield tk_instance


@pytest.fixture
def mock_config_manager():
    with patch('app_screen_capture.ConfigManager') as mock:
        config_instance = mock.return_value
        config_instance.get_screen_capture_settings.return_value = (0.3, 2)
        yield config_instance


@pytest.fixture
def mock_vision_ocr():
    with patch('app_screen_capture.VisionOCRService') as mock:
        ocr_instance = mock.return_value
        ocr_instance.perform_ocr.return_value = "テスト文字列"
        yield ocr_instance


@pytest.fixture
def screen_capture(mock_tk, mock_config_manager, mock_vision_ocr):
    return ScreenCapture()


def test_initialization(screen_capture, mock_tk):
    """初期化が正しく行われることをテスト"""
    assert screen_capture.screen_width == 1920
    assert screen_capture.screen_height == 1080
    assert screen_capture.outline_width == 2

    # ウィンドウの属性が正しく設定されていることを確認
    mock_tk.attributes.assert_any_call('-alpha', 0.3)
    mock_tk.attributes.assert_any_call('-fullscreen', True)
    mock_tk.attributes.assert_any_call('-topmost', True)


def test_on_press(screen_capture):
    """マウスプレス時の処理をテスト"""
    event = Mock()
    event.x = 100
    event.y = 200

    screen_capture._on_press(event)

    assert screen_capture.start_x == 100
    assert screen_capture.start_y == 200


def test_on_drag(screen_capture):
    """ドラッグ時の処理をテスト"""
    # 初期位置の設定
    screen_capture.start_x = 100
    screen_capture.start_y = 200

    event = Mock()
    event.x = 300
    event.y = 400

    # 既存の選択矩形がある場合のための初期化を追加
    screen_capture.selection_rect = None  # この行を追加

    screen_capture._on_drag(event)

    # 矩形が正しく作成されたことを確認
    screen_capture.canvas.create_rectangle.assert_called_once_with(
        100, 200, 300, 400,
        outline='red',
        width=screen_capture.outline_width
    )


def test_process_screenshot_success(screen_capture, mock_vision_ocr):
    """スクリーンショット処理の成功ケースをテスト"""
    screen_capture.start_x = 100
    screen_capture.start_y = 200
    screen_capture.end_x = 300
    screen_capture.end_y = 400

    with patch('pyautogui.screenshot') as mock_screenshot:
        mock_image = Mock(spec=Image.Image)
        mock_screenshot.return_value = mock_image

        screen_capture._process_screenshot()

        # スクリーンショットが正しい範囲で撮影されたことを確認
        mock_screenshot.assert_called_once_with(region=(100, 200, 200, 200))

        # OCRが実行されたことを確認
        mock_vision_ocr.perform_ocr.assert_called_once_with(mock_image)

        # クリップボードにテキストが設定されたことを確認
        screen_capture.root.clipboard_append.assert_called_once_with("テスト文字列")


def test_process_screenshot_small_area(screen_capture):
    """小さすぎる範囲選択時のテスト"""
    screen_capture.start_x = 100
    screen_capture.start_y = 100
    screen_capture.end_x = 102  # 範囲が小さすぎる
    screen_capture.end_y = 102

    with patch('tkinter.messagebox.showwarning') as mock_warning:
        screen_capture._process_screenshot()
        mock_warning.assert_called_once_with('OCR結果', 'スクリーンショットの範囲が小さすぎます。')


def test_process_screenshot_ocr_error(screen_capture, mock_vision_ocr):
    """OCRエラー時のテスト"""
    screen_capture.start_x = 100
    screen_capture.start_y = 200
    screen_capture.end_x = 300
    screen_capture.end_y = 400

    # OCRサービスがエラーを発生させるように設定
    mock_vision_ocr.perform_ocr.side_effect = Exception("OCRエラー")

    with patch('tkinter.messagebox.showerror') as mock_error:
        screen_capture._process_screenshot()
        mock_error.assert_called_once_with('OCRエラー', 'テキスト認識中にエラーが発生しました: OCRエラー')
