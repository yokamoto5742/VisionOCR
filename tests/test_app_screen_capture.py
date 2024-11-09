from typing import Generator
import pytest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk
from PIL import Image
from app_screen_capture import ScreenCapture


@pytest.fixture
def mock_config_manager():
    with patch('app_screen_capture.ConfigManager') as mock_config:
        config_instance = mock_config.return_value
        config_instance.get_screen_capture_settings.return_value = (0.3, 2)  # 透明度とアウトライン幅
        yield config_instance


@pytest.fixture
def mock_tk():
    with patch('tkinter.Tk') as mock_tk:
        root = mock_tk.return_value
        root.winfo_screenwidth.return_value = 1920
        root.winfo_screenheight.return_value = 1080
        yield root


@pytest.fixture
def mock_canvas():
    with patch('tkinter.Canvas') as mock_canvas:
        canvas_instance = MagicMock()
        mock_canvas.return_value = canvas_instance
        yield canvas_instance


@pytest.fixture
def screen_capture(mock_config_manager, mock_tk, mock_canvas):
    with patch('app_screen_capture.perform_ocr') as mock_ocr:
        screen_capture = ScreenCapture()
        screen_capture.canvas = mock_canvas
        yield screen_capture


def test_initialization(screen_capture):
    """初期化が正しく行われることを確認するテスト"""
    assert screen_capture.outline_width == 2
    assert screen_capture.screen_width == 1920
    assert screen_capture.screen_height == 1080
    assert screen_capture.start_x is None
    assert screen_capture.start_y is None
    assert screen_capture.end_x is None
    assert screen_capture.end_y is None
    assert screen_capture.selection_rect is None


def test_setup_window_error(mock_config_manager):
    """設定読み込みエラー時の処理をテストする"""
    mock_config_manager.get_screen_capture_settings.side_effect = Exception("設定エラー")

    with patch('tkinter.messagebox.showerror') as mock_error:
        with pytest.raises(Exception):
            ScreenCapture()

        mock_error.assert_called_once()
        assert "設定の読み込み中にエラー" in mock_error.call_args[0][1]


def test_mouse_press_event(screen_capture):
    """マウスクリックイベントの処理をテストする"""
    mock_event = Mock(x=100, y=200)
    screen_capture.selection_rect = "existing_rect"

    screen_capture._on_press(mock_event)

    assert screen_capture.start_x == 100
    assert screen_capture.start_y == 200
    screen_capture.canvas.delete.assert_called_once_with("existing_rect")


def test_mouse_drag_event(screen_capture):
    """マウスドラッグイベントの処理をテストする"""
    screen_capture.start_x = 50
    screen_capture.start_y = 50
    screen_capture.selection_rect = "old_rect"
    mock_event = Mock(x=200, y=150)

    screen_capture._on_drag(mock_event)

    screen_capture.canvas.delete.assert_called_once_with("old_rect")
    screen_capture.canvas.create_rectangle.assert_called_once_with(
        50, 50, 200, 150,
        outline='red',
        width=2
    )


def test_mouse_release_event(screen_capture):
    """マウスリリースイベントの処理をテストする"""
    mock_event = Mock(x=300, y=400)

    screen_capture._on_release(mock_event)

    assert screen_capture.end_x == 300
    assert screen_capture.end_y == 400
    screen_capture.root.withdraw.assert_called_once()
    screen_capture.root.quit.assert_called_once()


def test_escape_key_event(screen_capture):
    """ESCキーイベントの処理をテストする"""
    mock_event = Mock()

    screen_capture._cancel(mock_event)

    screen_capture.root.quit.assert_called_once()


def test_screenshot_bounds_calculation(screen_capture):
    """スクリーンショット範囲の計算をテストする"""
    screen_capture.start_x = 100
    screen_capture.start_y = 200
    screen_capture.end_x = 300
    screen_capture.end_y = 400

    bounds = screen_capture._get_screenshot_bounds()

    assert bounds == (100, 200, 300, 400)


def test_invalid_screenshot_bounds(screen_capture):
    """無効なスクリーンショット範囲の処理をテストする"""
    screen_capture.start_x = None
    screen_capture.start_y = 200
    screen_capture.end_x = 300
    screen_capture.end_y = 400

    with pytest.raises(ValueError) as exc_info:
        screen_capture._get_screenshot_bounds()

    assert "スクリーンショットの座標が正しく設定されていません" in str(exc_info.value)


@patch('pyautogui.screenshot')
def test_successful_screenshot_process(mock_screenshot, screen_capture):
    """スクリーンショット処理の成功パターンをテストする"""
    screen_capture.start_x = 100
    screen_capture.start_y = 200
    screen_capture.end_x = 300
    screen_capture.end_y = 400

    mock_image = MagicMock(spec=Image.Image)
    mock_screenshot.return_value = mock_image

    with patch('app_screen_capture.perform_ocr') as mock_ocr:
        mock_ocr.return_value = "テスト結果テキスト"
        screen_capture._process_screenshot()

        mock_screenshot.assert_called_once_with(region=(100, 200, 200, 200))
        mock_ocr.assert_called_once_with(mock_image)
        screen_capture.root.clipboard_append.assert_called_once_with("テスト結果テキスト")


@patch('tkinter.messagebox.showwarning')
@patch('pyautogui.screenshot')
def test_empty_ocr_result(mock_screenshot, mock_warning, screen_capture):
    """OCR結果が空の場合の処理をテストする"""
    screen_capture.start_x = 100
    screen_capture.start_y = 200
    screen_capture.end_x = 300
    screen_capture.end_y = 400

    mock_image = MagicMock(spec=Image.Image)
    mock_screenshot.return_value = mock_image

    with patch('app_screen_capture.perform_ocr') as mock_ocr:
        mock_ocr.return_value = ""
        screen_capture._process_screenshot()

        mock_warning.assert_called_once_with('OCR結果', 'テキストを検出できませんでした。')
