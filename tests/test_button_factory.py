import tkinter as tk
import unittest.mock
from unittest.mock import MagicMock, call, patch

import pytest

from widgets.button_factory import ButtonConfig, create_buttons


@pytest.fixture
def mock_parent():
    """親フレームのモック"""
    parent = MagicMock(spec=tk.Frame)
    return parent


def test_button_config_creation():
    """ButtonConfigの作成"""
    command = lambda: None
    config = ButtonConfig(text="テストボタン", command=command)

    assert config.text == "テストボタン"
    assert config.command == command
    assert config.is_highlight is False


def test_button_config_with_highlight():
    """ハイライト付きButtonConfigの作成"""
    command = lambda: None
    config = ButtonConfig(text="ハイライトボタン", command=command, is_highlight=True)

    assert config.text == "ハイライトボタン"
    assert config.command == command
    assert config.is_highlight is True


def test_create_buttons_single_normal(mock_parent):
    """通常ボタン1つの作成"""
    command = MagicMock()
    buttons = [ButtonConfig(text="ボタン1", command=command)]

    with patch('tkinter.Button') as mock_button_class:
        mock_button = MagicMock()
        mock_button_class.return_value = mock_button

        create_buttons(mock_parent, buttons)

        mock_button_class.assert_called_once_with(
            mock_parent,
            text="ボタン1",
            command=command
        )
        mock_button.configure.assert_not_called()
        mock_button.pack.assert_called_once_with(side=tk.LEFT, padx=2)


def test_create_buttons_single_highlight(mock_parent):
    """ハイライトボタン1つの作成"""
    command = MagicMock()
    buttons = [ButtonConfig(text="ハイライト", command=command, is_highlight=True)]

    with patch('tkinter.Button') as mock_button_class:
        mock_button = MagicMock()
        mock_button_class.return_value = mock_button

        create_buttons(mock_parent, buttons)

        mock_button_class.assert_called_once()
        mock_button.configure.assert_called_once_with(
            background='#007bff',
            foreground='white',
            font=('Helvetica', 10, 'bold'),
            relief=tk.RAISED,
            borderwidth=3
        )
        mock_button.bind.assert_any_call('<Enter>', unittest.mock.ANY)
        mock_button.bind.assert_any_call('<Leave>', unittest.mock.ANY)
        assert mock_button.bind.call_count == 2
        mock_button.pack.assert_called_once_with(side=tk.LEFT, padx=2)


def test_create_buttons_multiple(mock_parent):
    """複数ボタンの作成"""
    command1 = MagicMock()
    command2 = MagicMock()
    command3 = MagicMock()
    buttons = [
        ButtonConfig(text="ボタン1", command=command1),
        ButtonConfig(text="ボタン2", command=command2, is_highlight=True),
        ButtonConfig(text="ボタン3", command=command3)
    ]

    with patch('tkinter.Button') as mock_button_class:
        mock_buttons = [MagicMock(), MagicMock(), MagicMock()]
        mock_button_class.side_effect = mock_buttons

        create_buttons(mock_parent, buttons)

        assert mock_button_class.call_count == 3

        # 最初のボタン（通常）
        mock_buttons[0].configure.assert_not_called()
        mock_buttons[0].pack.assert_called_once()

        # 2番目のボタン（ハイライト）
        mock_buttons[1].configure.assert_called_once()
        mock_buttons[1].bind.assert_any_call('<Enter>', unittest.mock.ANY)
        mock_buttons[1].bind.assert_any_call('<Leave>', unittest.mock.ANY)
        mock_buttons[1].pack.assert_called_once()

        # 3番目のボタン（通常）
        mock_buttons[2].configure.assert_not_called()
        mock_buttons[2].pack.assert_called_once()


def test_create_buttons_empty_list(mock_parent):
    """空のボタンリスト"""
    with patch('tkinter.Button') as mock_button_class:
        create_buttons(mock_parent, [])
        mock_button_class.assert_not_called()


def test_highlight_button_hover_callbacks(mock_parent):
    """ハイライトボタンのホバーコールバック"""
    command = MagicMock()
    buttons = [ButtonConfig(text="ハイライト", command=command, is_highlight=True)]

    with patch('tkinter.Button') as mock_button_class:
        mock_button = MagicMock()
        mock_button_class.return_value = mock_button

        create_buttons(mock_parent, buttons)

        # bindが2回呼ばれていることを確認
        assert mock_button.bind.call_count == 2

        # Enter/Leaveイベントが登録されていることを確認
        bind_calls = [call_obj[0] for call_obj in mock_button.bind.call_args_list]
        events = [call_obj[0] for call_obj in bind_calls]
        assert '<Enter>' in events
        assert '<Leave>' in events
