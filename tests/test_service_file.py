import re
from datetime import datetime
from pathlib import Path

import pytest
from unittest.mock import patch, MagicMock

from service import service_file


@pytest.fixture
def mock_downloads_path():
    with patch('pathlib.Path.home') as mock_home:
        mock_home.return_value = Path('/mock/home')
        yield mock_home


def test_save_text_to_file_success(tmp_path):
    test_text = "テストテキスト"
    test_file_path = str(tmp_path / "test.txt")

    with patch('tkinter.filedialog.asksaveasfilename') as mock_dialog, \
            patch('tkinter.messagebox.showinfo') as mock_info, \
            patch('os.startfile') as mock_startfile:
        mock_dialog.return_value = test_file_path

        result = service_file.save_text_to_file(test_text)

        assert result is True
        with open(test_file_path, 'r', encoding='utf-8') as f:
            saved_text = f.read()
        assert saved_text == test_text

        mock_info.assert_called_once_with('完了', 'テキストファイルを保存しました。')
        mock_startfile.assert_called_once_with(str(tmp_path))


def test_save_text_to_file_cancel():
    with patch('tkinter.filedialog.asksaveasfilename') as mock_dialog, \
            patch('tkinter.messagebox.showinfo') as mock_info, \
            patch('os.startfile') as mock_startfile:
        mock_dialog.return_value = ''

        result = service_file.save_text_to_file("テストテキスト")

        assert result is False
        mock_info.assert_not_called()
        mock_startfile.assert_not_called()


def test_save_text_to_file_permission_error():
    test_text = "テストテキスト"

    with patch('tkinter.filedialog.asksaveasfilename') as mock_dialog, \
            patch('builtins.open') as mock_open, \
            patch('tkinter.messagebox.showerror') as mock_error:
        mock_dialog.return_value = '/invalid/path/test.txt'
        mock_open.side_effect = PermissionError("アクセス拒否")

        result = service_file.save_text_to_file(test_text)

        assert result is False
        mock_error.assert_called_once_with(
            'エラー',
            'ファイルへのアクセス権限がありません。'
        )


def test_save_text_to_file_os_error():
    test_text = "テストテキスト"

    with patch('tkinter.filedialog.asksaveasfilename') as mock_dialog, \
            patch('builtins.open') as mock_open, \
            patch('tkinter.messagebox.showerror') as mock_error:
        mock_dialog.return_value = '/invalid/path/test.txt'
        mock_open.side_effect = OSError("IOエラー")

        result = service_file.save_text_to_file(test_text)

        assert result is False
        mock_error.assert_called_once_with(
            'エラー',
            'ファイル操作エラー: IOエラー'
        )


def test_get_save_file_path_with_downloads(mock_downloads_path):
    expected_path = '/path/to/save/file.txt'

    with patch('pathlib.Path.exists') as mock_exists, \
            patch('tkinter.filedialog.asksaveasfilename') as mock_dialog:
        mock_exists.return_value = True
        mock_dialog.return_value = expected_path

        result = service_file.get_save_file_path()

        mock_dialog.assert_called_once()
        call_args = mock_dialog.call_args[1]

        # 現在時刻を使用したファイル名のフォーマット検証
        filename_pattern = r'OCR_result_\d{8}_\d{6}\.txt'
        assert re.match(filename_pattern, call_args['initialfile']), \
            f"ファイル名 '{call_args['initialfile']}' が期待される形式と一致しません"

        assert call_args['initialdir'] == str(Path('/mock/home/Downloads'))
        assert call_args['defaultextension'] == '.txt'
        assert call_args['filetypes'] == [
            ('テキストファイル', '*.txt'),
            ('すべてのファイル', '*.*')
        ]

        assert result == expected_path


def test_get_save_file_path_without_downloads(mock_downloads_path):
    with patch('pathlib.Path.exists') as mock_exists, \
            patch('pathlib.Path.cwd') as mock_cwd, \
            patch('tkinter.filedialog.asksaveasfilename') as mock_dialog:
        mock_exists.return_value = False
        mock_cwd.return_value = Path('/current/work/dir')
        mock_dialog.return_value = '/path/to/save/file.txt'

        result = service_file.get_save_file_path()

        mock_dialog.assert_called_once()
        assert mock_dialog.call_args[1]['initialdir'] == str(Path('/current/work/dir'))
