import pytest
from unittest.mock import Mock, patch

from app import __version__ as VERSION, __date__ as LAST_UPDATED


def test_version_format():
    """VERSIONが正しい形式であることを確認するテスト"""
    # バージョン番号が x.x.x の形式になっているか確認
    version_parts = VERSION.split('.')
    assert len(version_parts) == 3
    assert all(part.isdigit() for part in version_parts)


def test_last_updated_format():
    """LAST_UPDATEDが正しい日付形式であることを確認するテスト"""
    # 日付が YYYY-MM-DD の形式になっているか確認
    date_parts = LAST_UPDATED.split('-')
    assert len(date_parts) == 3
    assert len(date_parts[0]) == 4  # 年は4桁
    assert len(date_parts[1]) == 2  # 月は2桁
    assert len(date_parts[2]) == 2  # 日は2桁
    assert all(part.isdigit() for part in date_parts)


@patch('main.OCRApplication')
def test_main_creates_application(mock_ocr_app):
    """mainメソッドがアプリケーションを正しく作成・起動することを確認するテスト"""
    # モックの設定
    mock_instance = Mock()
    mock_ocr_app.return_value = mock_instance
    mock_instance.root = Mock()

    # main関数をインポートして実行
    from main import main
    main()

    # アサーション
    mock_ocr_app.assert_called_once()  # OCRApplicationが1回作成されたことを確認
    mock_instance.root.mainloop.assert_called_once()  # mainloopが1回呼ばれたことを確認


@patch('main.OCRApplication')
def test_main_handles_errors(mock_ocr_app):
    """mainメソッドがエラーを適切に処理することを確認するテスト"""
    # モックでエラーを発生させる
    mock_ocr_app.side_effect = Exception("テスト用エラー")

    # main関数をインポートして実行
    from main import main

    # エラーが発生することを確認
    with pytest.raises(Exception) as exc_info:
        main()
    assert str(exc_info.value) == "テスト用エラー"


# conftest.pyに移動することを推奨
@pytest.fixture
def mock_ocr_application():
    """OCRApplicationのモックを提供するフィクスチャ"""
    with patch('main.OCRApplication') as mock:
        instance = Mock()
        mock.return_value = instance
        instance.root = Mock()
        yield instance
