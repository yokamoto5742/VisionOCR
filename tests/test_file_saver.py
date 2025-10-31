import os
import re
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from service import file_saver


@pytest.fixture
def mock_downloads_path():
    with patch('pathlib.Path.home') as mock_home:
        mock_home.return_value = Path('/mock/home')
        yield mock_home


def test_get_save_file_path_with_downloads(mock_downloads_path):
    """Downloadsフォルダが存在する場合のファイルパス取得"""
    expected_path = '/path/to/save/file.txt'

    with patch('pathlib.Path.exists') as mock_exists, \
            patch('tkinter.filedialog.asksaveasfilename') as mock_dialog:
        mock_exists.return_value = True
        mock_dialog.return_value = expected_path

        result = file_saver.get_save_file_path()

        mock_dialog.assert_called_once()
        call_args = mock_dialog.call_args[1]

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
    """Downloadsフォルダが存在しない場合のファイルパス取得"""
    with patch('pathlib.Path.exists') as mock_exists, \
            patch('pathlib.Path.cwd') as mock_cwd, \
            patch('tkinter.filedialog.asksaveasfilename') as mock_dialog:
        mock_exists.return_value = False
        mock_cwd.return_value = Path('/current/work/dir')
        mock_dialog.return_value = '/path/to/save/file.txt'

        result = file_saver.get_save_file_path()

        mock_dialog.assert_called_once()
        assert mock_dialog.call_args[1]['initialdir'] == str(Path('/current/work/dir'))


def test_write_text_to_file(tmp_path):
    """ファイルへのテキスト書き込み"""
    test_file_path = tmp_path / "test.txt"
    test_text = "テストテキスト\n複数行"

    file_saver.write_text_to_file(str(test_file_path), test_text)

    with open(test_file_path, 'r', encoding='utf-8') as f:
        saved_text = f.read()
    assert saved_text == test_text


def test_show_success_message():
    """成功メッセージの表示"""
    with patch('tkinter.messagebox.showinfo') as mock_info:
        file_saver.show_success_message()
        mock_info.assert_called_once_with('完了', 'テキストファイルを保存しました。')


def test_open_saved_directory():
    """保存先ディレクトリを開く"""
    test_path = '/path/to/file.txt'
    with patch('os.startfile') as mock_startfile:
        file_saver.open_saved_directory(test_path)
        mock_startfile.assert_called_once_with('/path/to')


def test_save_text_to_file_success(tmp_path):
    """テキストファイル保存の成功"""
    test_text = "テストテキスト"
    test_file_path = str(tmp_path / "test.txt")

    with patch('tkinter.filedialog.asksaveasfilename') as mock_dialog, \
            patch('tkinter.messagebox.showinfo') as mock_info, \
            patch('os.startfile') as mock_startfile:
        mock_dialog.return_value = test_file_path

        result = file_saver.save_text_to_file(test_text)

        assert result is True
        with open(test_file_path, 'r', encoding='utf-8') as f:
            saved_text = f.read()
        assert saved_text == test_text

        mock_info.assert_called_once_with('完了', 'テキストファイルを保存しました。')
        mock_startfile.assert_called_once_with(str(tmp_path))


def test_save_text_to_file_cancel():
    """ファイル保存のキャンセル"""
    with patch('tkinter.filedialog.asksaveasfilename') as mock_dialog, \
            patch('tkinter.messagebox.showinfo') as mock_info, \
            patch('os.startfile') as mock_startfile:
        mock_dialog.return_value = ''

        result = file_saver.save_text_to_file("テストテキスト")

        assert result is False
        mock_info.assert_not_called()
        mock_startfile.assert_not_called()


def test_save_text_to_file_permission_error():
    """ファイル保存時の権限エラー"""
    test_text = "テストテキスト"

    with patch('tkinter.filedialog.asksaveasfilename') as mock_dialog, \
            patch('builtins.open') as mock_open, \
            patch('tkinter.messagebox.showerror') as mock_error:
        mock_dialog.return_value = '/invalid/path/test.txt'
        mock_open.side_effect = PermissionError("アクセス拒否")

        result = file_saver.save_text_to_file(test_text)

        assert result is False
        mock_error.assert_called_once_with(
            'エラー',
            'ファイルへのアクセス権限がありません。'
        )


def test_save_text_to_file_os_error():
    """ファイル保存時のOSエラー"""
    test_text = "テストテキスト"

    with patch('tkinter.filedialog.asksaveasfilename') as mock_dialog, \
            patch('builtins.open') as mock_open, \
            patch('tkinter.messagebox.showerror') as mock_error:
        mock_dialog.return_value = '/invalid/path/test.txt'
        mock_open.side_effect = OSError("IOエラー")

        result = file_saver.save_text_to_file(test_text)

        assert result is False
        mock_error.assert_called_once_with(
            'エラー',
            'ファイル操作エラー: IOエラー'
        )


def test_save_text_to_file_unexpected_error():
    """ファイル保存時の予期せぬエラー"""
    test_text = "テストテキスト"

    with patch('tkinter.filedialog.asksaveasfilename') as mock_dialog, \
            patch('builtins.open') as mock_open, \
            patch('tkinter.messagebox.showerror') as mock_error:
        mock_dialog.return_value = '/invalid/path/test.txt'
        mock_open.side_effect = Exception("予期せぬエラー")

        result = file_saver.save_text_to_file(test_text)

        assert result is False
        mock_error.assert_called_once_with(
            'エラー',
            '予期せぬエラーが発生しました: 予期せぬエラー'
        )
