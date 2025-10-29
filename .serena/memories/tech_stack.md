# 技術スタック

## コア技術
- **Python**: メイン開発言語
- **Tkinter**: GUIフレームワーク
- **Google Cloud Vision API**: OCRエンジン

## 主要な依存関係
- `google-cloud-vision==3.11.0`: OCR処理
- `pillow==12.0.0`: 画像処理
- `PyAutoGUI==0.9.54`: スクリーンキャプチャ
- `pyperclip==1.11.0`: クリップボード操作
- `pytest==8.3.3`: テストフレームワーク
- `pyinstaller==6.11.0`: 実行ファイルのビルド

## 開発ツール
- pytest: ユニットテスト
- PyInstaller: 実行ファイルのパッケージング
- pip-review: パッケージの更新管理

## プラットフォーム
- Windows（プライマリターゲット）
- config.iniの読み込みにPyInstaller互換のresource_path()を使用
