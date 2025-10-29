import pytest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk
from tkinter import TclError

from app.app_window import OCRApplication, ButtonConfig


@pytest.fixture
def mock_config_manager():
    with patch('app.app_window.ConfigManager') as mock:
        instance = mock.return_value
        instance.get_input_mode.return_value = False
        instance.get_window_geometry.return_value = [100, 100, 900, 700]
        instance.get_font_size.return_value = 12
        instance.config.get.return_value = 'MS Gothic'
        yield instance


@pytest.fixture
def mock_text_widget():
    """ScrolledTextウィジェットのモック"""
    text_widget = MagicMock()
    # テキスト内容を保持する変数
    text_widget._content = ""

    # getメソッドのモック
    def mock_get(*args):
        return text_widget._content

    text_widget.get.side_effect = mock_get

    # insertメソッドのモック
    def mock_insert(index, text):
        text_widget._content = text_widget._content + str(text)

    text_widget.insert.side_effect = mock_insert

    # deleteメソッドのモック
    def mock_delete(*args):
        text_widget._content = ""

    text_widget.delete.side_effect = mock_delete

    return text_widget


@pytest.fixture
def app(mock_config_manager, mock_text_widget):
    with patch('tkinter.Tk') as mock_tk, \
            patch('tkinter.scrolledtext.ScrolledText', return_value=mock_text_widget), \
            patch('app.app_window.ScreenCapture') as mock_screen_capture:
        # Tkインスタンスの設定
        mock_tk_instance = mock_tk.return_value
        mock_tk_instance.clipboard_get = MagicMock()
        mock_tk_instance.iconify = MagicMock()
        mock_tk_instance.deiconify = MagicMock()

        app = OCRApplication()
        app.text_area = mock_text_widget
        yield app


def test_initialization(app, mock_config_manager):
    """アプリケーションの初期化テスト"""
    assert app.is_append_mode == False
    assert app.config_manager == mock_config_manager
    mock_config_manager.get_input_mode.assert_called_once()
    mock_config_manager.get_window_geometry.assert_called_once()


def test_toggle_input_mode(app):
    """入力モードの切り替えテスト"""
    initial_mode = app.is_append_mode
    app.toggle_input_mode()
    assert app.is_append_mode != initial_mode
    app.config_manager.set_input_mode.assert_called_once_with(app.is_append_mode)


@pytest.mark.parametrize("initial_text,new_text,expected_text", [
    ("", "新規テキスト", "新規テキスト"),
    ("既存テキスト", "新規テキスト", "既存テキスト\n新規テキスト"),
])
def test_append_mode(app, initial_text, new_text, expected_text):
    """追記モードのテスト"""
    app.is_append_mode = True
    app.text_area._content = initial_text

    # クリップボードの操作をモック
    with patch.object(app.root, 'clipboard_get', return_value=new_text):
        app.capture_screen()

    assert app.text_area._content == expected_text


def test_overwrite_mode(app):
    """上書きモードのテスト"""
    app.is_append_mode = False
    app.text_area._content = "既存テキスト"

    # クリップボードの操作をモック
    with patch.object(app.root, 'clipboard_get', return_value="新規テキスト"):
        app.capture_screen()

    assert app.text_area._content == "新規テキスト"


def test_clear_screen(app):
    """画面クリア機能のテスト"""
    app.text_area._content = "テストテキスト"
    app.clear_screen()
    assert app.text_area._content == ""


def test_save_to_file(app):
    """ファイル保存機能のテスト"""
    test_text = "保存するテキスト"
    app.text_area._content = test_text

    with patch('app.app_window.save_text_to_file') as mock_save:
        app.save_to_file()
        mock_save.assert_called_once_with(test_text)
