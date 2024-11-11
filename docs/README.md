# VisionOCR

## 概要
VisionOCRは、Google Cloud Vision APIを使用して画面上の任意の領域からテキストを抽出するデスクトップアプリケーションです。キャプチャした画像から文字を認識し、編集可能なテキストとして取り込むことができます。日本語の手書き文字や半角カナ文字の読み取りにも対応しています。

## 機能
- 画面の任意の領域を選択してOCR処理
- 認識したテキストの編集機能
- テキストの追記/上書きモード切替
- テキスト編集機能：
  - 読点（、）の除去
  - 句点（。）の除去
  - 改行の除去
  - スペースの除去
- クリップボードへのコピー機能
- テキストのファイル出力機能

## 必要要件
- Python 3.10以上
- Google Cloud Vision API のアクセス権限
- 以下のPythonパッケージ:
  - tkinter
  - pyautogui
  - Pillow (PIL)
  - google-cloud-vision

## インストール方法
1. リポジトリをクローン
```bash
git clone [repository-url]
cd visionocr
```

2. 必要なパッケージをインストール
```bash
pip install -r requirements.txt
```

3. Google Cloud Vision API の認証情報を設定
- Google Cloud Consoleで認証情報を取得
- 環境変数 `GOOGLE_APPLICATION_CREDENTIALS` に認証情報のパスを設定

## 使い方
1. アプリケーションの起動
```bash
python main.py
```

2. OCR処理の手順
   1. 「OCR範囲選択」ボタンをクリック
   2. マウスでキャプチャしたい領域をドラッグして選択
   3. 選択完了後、自動的にOCR処理が実行され、結果がテキストエリアに表示

3. テキスト編集
   - 各種編集ボタンを使用してテキストを整形
   - 必要に応じて手動でテキストを編集
   - 「追記モード」「上書きモード」を切り替えて新しいOCR結果の挿入方法を制御

4. テキストの出力
   - 「全文コピー」でクリップボードにコピー
   - 「ファイル出力」で任意のファイルに保存

## 主なファイル構成
- `main.py`: アプリケーションのエントリーポイント
- `app_window.py`: メインウィンドウのGUI実装
- `app_screen_capture.py`: 画面キャプチャ機能の実装
- `vision_ocr_service.py`: Google Cloud Vision APIとの連携
- `service_text.py`: テキスト処理機能の実装
- `service_file.py`: ファイル保存機能の実装
- `config_manager.py`: アプリケーション設定の管理

## エラー処理
- OCR処理失敗時のエラーメッセージ表示
- 設定ファイル読み込みエラーの処理
- テキスト処理時のエラーハンドリング

## 注意事項
- Google Cloud Vision APIの利用料金が発生する可能性があります
- 大量の文字を含む画像の処理には時間がかかる場合があります
- 画像の品質や文字の状態によってOCRの精度が変わる可能性があります
