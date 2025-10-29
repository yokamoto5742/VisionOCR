# コードベース構造

## ディレクトリ構成

```
VisionOCR/
├── app/                        # アプリケーションのメインコード
│   ├── app_window.py          # OCRApplicationクラス - メインGUI
│   ├── app_screen_capture.py  # ScreenCaptureクラス - 画面キャプチャ
│   └── __init__.py            # バージョン情報
├── service/                    # サービスレイヤー
│   ├── vision_ocr_service.py  # VisionOCRServiceクラス - OCR処理
│   ├── service_text.py        # テキスト処理ユーティリティ
│   └── service_file.py        # ファイルI/O操作
├── utils/                      # ユーティリティ
│   ├── config_manager.py      # ConfigManagerクラス - 設定管理
│   ├── config.ini             # 設定ファイル
│   ├── env_loader.py          # 環境変数ローダー
│   ├── exceptions.py          # カスタム例外
│   ├── log_rotation.py        # ログローテーション
│   └── constants.py           # 定数定義
├── tests/                      # テストコード
│   ├── test_app_window.py
│   ├── test_app_screen_capture.py
│   ├── test_vision_ocr_service.py
│   ├── test_service_text.py
│   └── test_service_file.py
├── scripts/                    # スクリプト
│   ├── version_manager.py     # バージョン管理
│   └── project_structure.py   # プロジェクト構造生成
├── widgets/                    # ウィジェット（現在は未使用）
├── assets/                     # アセット（アイコン、画像）
│   ├── VisionOCR.ico
│   └── VisionOCR.png
├── docs/                       # ドキュメント
│   ├── README.md
│   ├── CHANGELOG.md           # 変更ログ（Keep a Changelog形式）
│   └── LICENSE
├── .claude/                    # Claude Code設定
│   ├── agents/                # カスタムエージェント
│   ├── hooks/                 # フック
│   └── settings.local.json
├── main.py                     # エントリーポイント
├── build.py                    # ビルドスクリプト
├── requirements.txt            # 依存関係
└── CLAUDE.md                  # Claude Code用のプロジェクト指示
```

## 主要クラス

### OCRApplication (app/app_window.py)
- メインGUIウィンドウの管理
- ボタン、テキストエリア、ユーザーインタラクションの処理
- 追記/上書きモード切り替え機能
- 主要メソッド:
  - `capture_screen()`: 画面キャプチャとOCR実行
  - `toggle_input_mode()`: モード切り替え
  - `copy_to_clipboard()`: クリップボードコピー
  - `save_to_file()`: ファイル保存
  - `clear_screen()`: テキストクリア

### ScreenCapture (app/app_screen_capture.py)
- マウスドラッグによる領域選択
- 選択領域のスクリーンショット取得

### VisionOCRService (service/vision_ocr_service.py)
- Google Cloud Vision APIとの統合
- OCR処理の実行

### ConfigManager (utils/config_manager.py)
- config.iniからの設定読み込み
- PyInstaller環境対応のresource_path()提供
- ウィンドウジオメトリ、透明度、アウトライン幅などの設定管理

## エントリーポイント
`main.py` が `OCRApplication().root.mainloop()` を呼び出してアプリケーションを起動
