from typing import Any

import pytest
import tkinter as tk
from unittest.mock import Mock

from service import text_widget_utils


@pytest.fixture
def mock_text_widget() -> Mock:
    widget = Mock()
    widget._text = ""

    def mock_get(start: str, end: str) -> str:
        return widget._text

    def mock_delete(start: str, end: str) -> None:
        widget._text = ""

    def mock_insert(position: Any, text: str) -> None:
        widget._text = widget._text + text

    widget.get = mock_get
    widget.delete = mock_delete
    widget.insert = mock_insert

    return widget


def test_remove_punctuation_japanese_comma(mock_text_widget: Mock) -> None:
    initial_text = "これは、テストです、よろしく"
    expected_text = "これはテストですよろしく"
    mock_text_widget._text = initial_text

    text_widget_utils.remove_punctuation(mock_text_widget, "、")
    result = mock_text_widget._text

    assert result == expected_text


def test_remove_punctuation_japanese_period(mock_text_widget: Mock) -> None:
    initial_text = "これは。テストです。よろしく"
    expected_text = "これはテストですよろしく"
    mock_text_widget._text = initial_text

    text_widget_utils.remove_punctuation(mock_text_widget, "。")
    result = mock_text_widget._text

    assert result == expected_text


def test_remove_spaces(mock_text_widget: Mock) -> None:
    initial_text = "This is  a   test   string"
    expected_text = "Thisisateststring"
    mock_text_widget._text = initial_text

    text_widget_utils.remove_spaces(mock_text_widget)
    result = mock_text_widget._text

    assert result == expected_text


def test_remove_spaces_with_japanese(mock_text_widget: Mock) -> None:
    initial_text = "これは　テスト　です"
    expected_text = "これはテストです"
    mock_text_widget._text = initial_text

    text_widget_utils.remove_spaces(mock_text_widget)
    result = mock_text_widget._text

    assert result == expected_text


def test_remove_linebreaks(mock_text_widget: Mock) -> None:
    initial_text = "これは\nテスト\nです"
    expected_text = "これは テスト です"
    mock_text_widget._text = initial_text

    text_widget_utils.remove_linebreaks(mock_text_widget)
    result = mock_text_widget._text

    assert result == expected_text


def test_get_text_content(mock_text_widget: Mock) -> None:
    expected_text = "テストテキスト"
    mock_text_widget._text = expected_text

    result = text_widget_utils.get_text_content(mock_text_widget)

    assert result == expected_text


def test_set_text_content_replace(mock_text_widget: Mock) -> None:
    initial_text = "初期テキスト"
    new_text = "新しいテキスト"
    mock_text_widget._text = initial_text

    text_widget_utils.set_text_content(mock_text_widget, new_text, append=False)
    result = mock_text_widget._text

    assert result == new_text


def test_set_text_content_append(mock_text_widget: Mock) -> None:
    initial_text = "初期テキスト"
    additional_text = "追加テキスト"
    expected_text = "初期テキスト\n追加テキスト"
    mock_text_widget._text = initial_text

    text_widget_utils.set_text_content(mock_text_widget, additional_text, append=True)
    result = mock_text_widget._text

    assert result == expected_text


def test_set_text_content_append_empty(mock_text_widget: Mock) -> None:
    new_text = "新しいテキスト"
    mock_text_widget._text = ""

    text_widget_utils.set_text_content(mock_text_widget, new_text, append=True)
    result = mock_text_widget._text

    assert result == new_text


@pytest.fixture
def error_mock_widget() -> Mock:
    widget = Mock()
    widget.get.side_effect = tk.TclError("テストエラー")
    widget.delete.side_effect = tk.TclError("テストエラー")
    widget.insert.side_effect = tk.TclError("テストエラー")
    return widget


def test_remove_punctuation_error(error_mock_widget: Mock) -> None:
    with pytest.raises(ValueError) as exc_info:
        text_widget_utils.remove_punctuation(error_mock_widget, "、")
    assert "テキストウィジェットの操作に失敗しました" in str(exc_info.value)


def test_remove_spaces_error(error_mock_widget: Mock) -> None:
    with pytest.raises(ValueError) as exc_info:
        text_widget_utils.remove_spaces(error_mock_widget)
    assert "テキストウィジェットの操作に失敗しました" in str(exc_info.value)


def test_remove_linebreaks_error(error_mock_widget: Mock) -> None:
    with pytest.raises(ValueError) as exc_info:
        text_widget_utils.remove_linebreaks(error_mock_widget)
    assert "テキストウィジェットの操作に失敗しました" in str(exc_info.value)


def test_get_text_content_error(error_mock_widget: Mock) -> None:
    with pytest.raises(ValueError) as exc_info:
        text_widget_utils.get_text_content(error_mock_widget)
    assert "テキストウィジェットの読み取りに失敗しました" in str(exc_info.value)


def test_set_text_content_error(error_mock_widget: Mock) -> None:
    with pytest.raises(ValueError) as exc_info:
        text_widget_utils.set_text_content(error_mock_widget, "テスト")
    assert "テキストウィジェットの書き込みに失敗しました" in str(exc_info.value)
