# VisionOCR

## プロジェクト概要

VisionOCRは、Google Cloud Vision APIを使用して画面上の任意の領域からテキストを抽出するデスクトップアプリケーションです。マウスドラッグで領域を選択するだけで、高精度のOCR処理を実行できます。日本語の手書き文字や半角カタカナの認識にも対応しています。

## 主な機能

- 画面の任意の領域をマウスドラッグで選択してOCR実行
- Google Cloud Vision APIによる高精度なテキスト認識
- 日本語手書き文字と半角カタカナのサポート
- 追記/上書きモードの切り替え（OCR結果の挿入方法を制御）
- テキスト編集機能（読点・句点・改行・空白の除去）
- OCR結果のクリップボードコピー機能
- OCR結果のファイル保存機能（ダイアログ選択）

## 必要要件

### 開発環境
- Python 3.13以上
- Google Cloud Vision API のサービスアカウント認証情報

### 実行環境
- Windows OS
- Google Cloud Vision API のアクセス権限
- インターネット接続

### Pythonパッケージ依存関係
主要な依存関係（詳細は`pyproject.toml`参照）:
- `google-cloud-vision==3.11.0` - OCR処理エンジン
- `PyAutoGUI==0.9.54` - スクリーンキャプチャ
- `pyperclip==1.11.0` - クリップボード操作
- `python-dotenv==1.2.1` - 環境変数ロード

## インストール方法

### 1. リポジトリをクローン
```bash
git clone https://github.com/yokamoto5742/VisionOCR
cd VisionOCR
```

### 2. 仮想環境の作成と依存パッケージのインストール

事前に [uv](https://docs.astral.sh/uv/getting-started/installation/) のインストールが必要です。

```bash
# 仮想環境の作成とパッケージのインストールを一度に行う
uv sync
```

仮想環境を有効化する：

```bash
# Windows (Command Prompt)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Mac / Linux
source .venv/bin/activate
```

### 3. Google Cloud API キーを設定

`.env` の`GOOGLE_CREDENTIALS_JSON` の値には、Google Cloud Console からダウンロードしたサービスアカウントキーの JSON を**1 行に変換した文字列**が必要です。

#### 3-1. サービスアカウントキーを 1 行に変換

Google Cloud Console からダウンロードした JSON ファイルには改行が含まれているため、`scripts/json_minifier.py` を使って 1 行に変換します。

```bash
python scripts/json_minifier.py
```

実行するとファイル選択ダイアログが開きます。Google Cloud のサービスアカウントキー JSON ファイルを選択してください。

スクリプトは変換後の 1 行 JSON をタイムスタンプ付きで出力ファイル（例: `credentials_20240430_123456.json`）に保存します。出力ファイル内の JSON 文字列をコピーしてください。

#### 3-2. .env ファイルを作成

```
GOOGLE_PROJECT_ID=my-awesome-app-123456
GOOGLE_LOCATION=asia-northeast1
GOOGLE_CREDENTIALS_JSON={"type":"service_account","project_id":"my-awesome-app-123456","private_key_id":...}
```

**セキュリティ上の注意**: `.env`ファイルは絶対に公開リポジトリにコミットしないでください。`.gitignore`に`.env`が含まれていることを確認してください。

## 使用方法

### アプリケーションの起動
```bash
python main.py
```

### 基本的な使用フロー

1. **OCR範囲選択**
   - アプリケーション内の「OCR範囲選択」ボタンをクリック
   - マウスをドラッグして、OCRしたい領域を選択

2. **OCR処理**
   - 領域選択後、自動的にスクリーンショットが取得されます
   - スクリーンショットがGoogle Cloud Vision APIに送信され、テキストが認識されます
   - 認識結果がテキストエリアに表示されます

3. **テキスト編集**
   - 「読点除去」「句点除去」「改行除去」「スペース除去」ボタンで整形
   - テキストエリアで直接編集することも可能

4. **テキスト出力**
   - 「全文コピー」: テキストエリアのテキスト全文をクリップボードにコピー
   - 「ファイル出力」: テキストを任意のファイルに保存（ダイアログで保存場所を選択）

5. **モード切り替え**
   - 「追記モード」「上書きモード」ボタンで、次のOCR結果の挿入方法を制御

### 使用例

日本語文書のスクリーンショットからテキストを抽出する場合:

1. 抽出したい日本語文字の領域を選択
2. OCR処理待機（通常1〜3秒）
3. 認識されたテキストで「読点除去」「改行除去」等を実行
4. 結果をクリップボードコピーまたはファイル保存

## アーキテクチャ

### アーキテクチャパターン

VisionOCRはレイヤード設計に基づいており、関心事を明確に分離しています：

#### 1. プレゼンテーション層 (app/)
- **OCRApplication** (`app_window.py`): メインGUIウィンドウ
  - ユーザーインタラクション処理
  - UI状態管理（追記/上書きモード切り替え）
  - ウィジェットレイアウト管理

- **ScreenCapture** (`app_screen_capture.py`): 画面キャプチャ
  - マウスドラッグによる領域選択
  - スクリーンショット取得

#### 2. ビジネスロジック層 (service/)
- **VisionOCRService** (`vision_ocr_service.py`): OCR処理エンジン
  - Google Cloud Vision APIとの統合
  - 画像→テキスト変換

- **ファイル操作** (`file_saver.py`): ファイルI/O
  - テキスト保存とダイアログ管理

- **テキスト処理** (`text_widget_utils.py`): Tkinter操作とテキスト変換
  - テキストウィジェットへの追記/上書き処理
  - 読点・句点・改行・空白の除去

#### 3. ユーティリティ層 (utils/)
- **ConfigManager** (`config_manager.py`): 設定管理
  - config.iniから設定読み込み
  - PyInstaller互換のリソース取得（`resource_path()`）

- **環境変数管理** (`env_loader.py`): 認証情報ロード
  - `.env`ファイル解析
  - サービスアカウント認証情報初期化

#### 4. テスト層 (tests/)
- pytest ベースのユニットテスト
- ソースファイル構造と対応

### 認証フロー

1. アプリケーション起動時に`env_loader.py`が`.env`ファイルを読み込む
2. Google Cloud Vision API用サービスアカウント認証情報をメモリに格納
3. VisionOCRServiceが認証情報を使用してAPIリクエスト実行

## 開発コマンド

### アプリケーション実行
```bash
python main.py
```

### テスト実行
```bash
# 全テスト実行
pytest

# 詳細出力
pytest -v

# カバレッジレポート付き実行
pytest --cov=app --cov=service --cov=utils

# 特定のテストファイル実行
pytest tests/test_app_window.py
```

## トラブルシューティング

### Google Cloud Vision APIエラー
**症状**: 「authentication error」や「permission denied」エラーが表示される

**解決方法**:
1. `.env`ファイルが正しくプロジェクトルートに配置されているか確認
2. `.env`のPRIVATE_KEY形式を確認（改行記号が`\n`である必要があります）
3. Google Cloud Consoleでサービスアカウントが有効か確認
4. APIクォータと請求情報が正常か確認

### 画面キャプチャがうまくいかない
**症状**: 領域選択後にスクリーンショットが取得されない

**解決方法**:
1. PyAutoGUIの権限確認（Windowsの権限設定を確認）
2. マルチモニター環境の場合、プライマリモニターを使用していることを確認

### テキスト認識精度が低い
**症状**: 日本語が正しく認識されない、文字が欠落する

**解決方法**:
1. スクリーンショット領域をより大きく選択してみてください（最小推奨: 200x200ピクセル）
2. 画像のコントラストと明度が充分であることを確認してください
3. フォントサイズが小さすぎないことを確認してください（推奨: 12pt以上）

### VisionOCRService初期化エラー
**症状**: アプリケーション起動時に初期化エラーが表示される

**解決方法**:
1. Pythonバージョンが3.10以上であることを確認: `python --version`
2. 依存パッケージが正しくインストールされていることを確認: `pip list | grep google-cloud-vision`
3. 仮想環境が有効化されていることを確認: Windows環境では`.venv\Scripts\activate`を実行

## 注意事項

- Google Cloud Vision APIの利用には料金が発生する可能性があります。詳細は[Google Cloud Vision pricing](https://cloud.google.com/vision/pricing)を参照してください
- 大量の画像処理には時間がかかる場合があります。APIリクエストのレート制限に注意してください
- `.env`ファイルには秘密情報が含まれます。リポジトリにコミットしないでください
- 画像品質、文字の大きさ、コントラストによってOCR精度が変動します

## ライセンス

このプロジェクトのライセンス情報については、 [LICENSE](docs/LICENSE) を参照してください。

## 更新履歴

更新履歴は [CHANGELOG.md](docs/CHANGELOG.md) を参照してください。
