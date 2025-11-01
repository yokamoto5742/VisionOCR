# VisionOCR

バージョン: 1.1.1 (2025-11-01)

## プロジェクト概要

VisionOCRは、Google Cloud Vision APIを使用して画面上の任意の領域からテキストを抽出するデスクトップアプリケーションです。マウスドラッグで領域を選択するだけで、高精度のOCR処理を実行できます。日本語の手書き文字や半角カタカナの認識にも対応しています。

## 主な機能

- 画面の任意の領域をマウスドラッグで選択してOCR実行
- Google Cloud Vision APIによる高精度なテキスト認識
- 日本語手書き文字とハーフ幅カタカナのサポート
- 追記/上書きモードの切り替え（OCR結果の挿入方法を制御）
- テキスト編集機能（読点・句点・改行・空白の除去）
- OCR結果のクリップボードコピー機能
- OCR結果のファイル保存機能（ダイアログ選択）

## 必要要件

### 開発環境
- Python 3.10以上
- pip（Pythonパッケージマネージャー）
- Google Cloud Vision API のサービスアカウント認証情報

### 実行環境
- Windows OS
- Google Cloud Vision API のアクセス権限
- インターネット接続

### Pythonパッケージ依存関係
主要な依存関係（詳細は`requirements.txt`参照）:
- `google-cloud-vision==3.11.0` - OCR処理エンジン
- `pillow==12.0.0` - 画像処理
- `PyAutoGUI==0.9.54` - スクリーンキャプチャ
- `pyperclip==1.11.0` - クリップボード操作
- `python-dotenv==1.2.1` - 環境変数ロード

## インストール方法

### 1. リポジトリをクローン
```bash
git clone [repository-url]
cd VisionOCR
```

### 2. 仮想環境の構築（推奨）
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 4. Google Cloud Vision API認証情報の設定

プロジェクトルートに`.env`ファイルを作成し、Google Cloud Consoleから取得したサービスアカウント認証情報を配置してください：

```
TYPE=service_account
PROJECT_ID=your-project-id
PRIVATE_KEY_ID=your-private-key-id
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
CLIENT_ID=your-client-id
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/...
UNIVERSE_DOMAIN=googleapis.com
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
   - メインウィンドウが一時的に非表示になります
   - マウスをドラッグして、OCRしたい領域を選択

2. **OCR処理**
   - 領域選択後、自動的にスクリーンショットが取得されます
   - Google Cloud Vision APIに送信され、テキストが認識されます
   - 認識結果がテキストエリアに表示されます

3. **テキスト編集**
   - 「読点除去」「句点除去」「改行除去」「スペース除去」ボタンで自動整形
   - テキストエリアで直接編集することも可能

4. **テキスト出力**
   - 「全文コピー」: 認識されたテキストをクリップボードにコピー
   - 「ファイル出力」: テキストを任意のファイルに保存（ダイアログで場所を選択）

5. **モード切り替え**
   - 「追記モード」「上書きモード」ボタンで、次のOCR結果の挿入方法を制御

### 使用例

日本語文書のスクリーンショットからテキストを抽出する場合:

1. 抽出したい日本語文字の領域を選択
2. OCR処理待機（通常1〜3秒）
3. 認識されたテキストで「読点除去」「改行除去」等を実行
4. 結果をクリップボードコピーまたはファイル保存

## プロジェクト構成

```
VisionOCR/
├── app/                          # アプリケーションコア
│   ├── app_window.py            # メインGUIウィンドウ (OCRApplication)
│   ├── app_screen_capture.py    # 画面キャプチャ機能 (ScreenCapture)
│   └── __init__.py              # バージョン定義
├── service/                      # ビジネスロジック層
│   ├── vision_ocr_service.py    # Google Vision API統合 (VisionOCRService)
│   ├── service_text.py          # テキスト処理ユーティリティ
│   ├── service_file.py          # ファイルI/O操作
│   ├── text_widget_utils.py     # Tkinterテキストウィジェット操作
│   └── file_saver.py            # ファイル保存ダイアログ
├── utils/                        # ユーティリティ層
│   ├── config_manager.py        # 設定ファイル管理 (ConfigManager)
│   ├── env_loader.py            # 環境変数ロード
│   ├── constants.py             # 定数定義
│   ├── exceptions.py            # カスタム例外
│   ├── log_rotation.py          # ログローテーション
│   └── config.ini               # アプリケーション設定ファイル
├── tests/                        # テストスイート
│   ├── test_app_window.py
│   ├── test_app_screen_capture.py
│   ├── test_vision_ocr_service.py
│   ├── test_service_text.py
│   └── test_service_file.py
├── scripts/                      # ユーティリティスクリプト
│   ├── version_manager.py       # バージョン管理自動化
│   └── project_structure.py     # プロジェクト構造生成
├── assets/                       # リソース
│   ├── VisionOCR.ico            # アプリケーションアイコン
│   └── VisionOCR.png            # ロゴ画像
├── docs/                         # ドキュメント
│   ├── README.md                # このファイル
│   ├── CHANGELOG.md             # 変更ログ
│   └── LICENSE                  # ライセンス
├── main.py                       # アプリケーション起動エントリーポイント
├── build.py                      # 実行ファイルビルドスクリプト
├── requirements.txt              # Python依存パッケージ
├── .env                          # 環境変数（認証情報）※リポジトリ外で管理
└── CLAUDE.md                     # Claude Code用プロジェクト指示
```

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

- **テキスト処理** (`service_text.py`): 純粋なテキスト変換
  - 読点・句点・改行・空白の除去

- **ファイル操作** (`service_file.py`, `file_saver.py`): ファイルI/O
  - テキスト保存とダイアログ管理

- **ウィジェット操作** (`text_widget_utils.py`): Tkinter操作
  - テキストウィジェットへの追記/上書き処理

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

### データフロー

```
ユーザーが領域選択
    ↓
ScreenCapture が領域のスクリーンショットを取得
    ↓
VisionOCRService が Google Vision API に画像を送信
    ↓
APIが認識テキストを返却
    ↓
OCRApplication がテキストをウィジェットに表示
    ↓
ユーザーが編集/コピー/保存を実行
```

### 設定管理

ConfigManagerは`config.ini`から以下の設定を読み込みます：
- ウィンドウジオメトリ（サイズ、位置）
- 透明度設定
- アウトライン幅設定
- PyInstallerビルド時の互換性処理（`resource_path()`）

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

### 実行ファイルビルド
```bash
python build.py
```

ビルドスクリプトの処理：
1. `app/__init__.py`のバージョンを自動インクリメント（パッチバージョン）
2. 実行ファイル出力フォルダ: `dist/VisionOCR/VisionOCR.exe`
3. バンドル内容:
   - `config.ini` - アプリケーション設定
   - `.env` - Google API認証情報
4. アイコン: `assets/VisionOCR.ico`

### バージョン管理
- 現在のバージョン: 1.1.1
- バージョン定義ファイル: `app/__init__.py`
  - `__version__` - セマンティックバージョン
  - `__date__` - 最終更新日付
- バージョン管理スクリプト: `scripts/version_manager.py`（ビルド時に自動実行）

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
3. スクリーン解像度が極端に高い場合は、キャプチャ処理にやや時間がかかる場合があります

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

## 開発環境セットアップ

### IDE設定（PyCharm推奨）
1. インタープリタ設定: Python 3.10+（`.venv`から選択）
2. Runスクリプト: `main.py` をターゲット
3. テスト実行: pytest ランナー（デフォルト設定）

### コーディング規約
- **Python規約**: PEP8に準拠
- **命名規則**: スネークケース（`my_function`）
- **関数サイズ**: 50行以下を目標
- **コメント**: 日本語で記述、文末に句点を付けない
- **Import順序**: 標準ライブラリ → サードパーティ → カスタムモジュール（各グループ内でアルファベット順）

### 品質保証
```bash
# テストカバレッジ確認
pytest --cov=app --cov=service --cov=utils --cov-report=html

# Linting（pyright）
pyright

# 複数パッケージの最新版確認
pip-review
```

## ライセンス

このプロジェクトのライセンスについては、`docs/LICENSE`を参照してください。

## 関連ドキュメント

- `docs/CHANGELOG.md` - 変更履歴（Keep a Changelog形式）
- `CLAUDE.md` - Claude Code用プロジェクト指示
- `docs/LICENSE` - ライセンス情報

## 注意事項

- Google Cloud Vision APIの利用には料金が発生する可能性があります。詳細は[Google Cloud Vision pricing](https://cloud.google.com/vision/pricing)を参照してください
- 大量の画像処理には時間がかかる場合があります。APIリクエストのレート制限に注意してください
- `.env`ファイルには秘密情報が含まれます。リポジトリにコミットしないでください
- 画像品質、文字の大きさ、コントラストによってOCR精度が変動します
