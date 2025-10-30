# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## House Rules:
- 文章ではなくパッチの差分を返す。
- コードの変更範囲は最小限に抑える。
- コードの修正は直接適用する。
- Pythonのコーディング規約はPEP8に従います。
- KISSの原則に従い、できるだけシンプルなコードにします。
- 可読性を優先します。一度読んだだけで理解できるコードが最高のコードです。
- Pythonのコードのimport文は以下の適切な順序に並べ替えてください。
標準ライブラリ
サードパーティライブラリ
カスタムモジュール 
それぞれアルファベット順に並べます。importが先でfromは後です。

## CHANGELOG
このプロジェクトにおけるすべての重要な変更は日本語でdcos/CHANGELOG.mdに記録します。
フォーマットは[Keep a Changelog](https://keepachangelog.com/ja/1.1.0/)に基づきます。

## Automatic Notifications (Hooks)
自動通知は`.claude/settings.local.json` で設定済：
- **Stop Hook**: ユーザーがClaude Codeを停止した時に「作業が完了しました」と通知
- **SessionEnd Hook**: セッション終了時に「セッションが終了しました」と通知

## クリーンコードガイドライン
- 関数のサイズ：関数は50行以下に抑えることを目標にしてください。関数の処理が多すぎる場合は、より小さなヘルパー関数に分割してください。
- 単一責任：各関数とモジュールには明確な目的が1つあるようにします。無関係なロジックをまとめないでください。
- 命名：説明的な名前を使用してください。`tmp` 、`data`、`handleStuff`のような一般的な名前は避けてください。例えば、`doCalc`よりも`calculateInvoiceTotal` の方が適しています。
- DRY原則：コードを重複させないでください。類似のロジックが2箇所に存在する場合は、共有関数にリファクタリングしてください。それぞれに独自の実装が必要な場合はその理由を明確にしてください。
- コメント:分かりにくいロジックについては説明を加えます。説明不要のコードには過剰なコメントはつけないでください。
- コメントとdocstringは必要最小限に日本語で記述し、文末に"。"や"."をつけないでください。

## Project Overview
VisionOCR is a desktop application that uses Google Cloud Vision API to extract text from screen regions via OCR. It's a Tkinter-based GUI application that supports Japanese handwriting and half-width katakana recognition.

## Architecture

### Core Components
- **app/app_window.py**: Main GUI (`OCRApplication` class) - manages the Tkinter window, text display area, and all user interactions. Uses append/overwrite mode toggle for OCR results.
- **app/app_screen_capture.py**: Screen capture functionality (`ScreenCapture` class) - handles region selection via mouse drag
- **service/vision_ocr_service.py**: Google Cloud Vision API integration (`VisionOCRService` class) - performs actual OCR processing
- **service/service_text.py**: Text manipulation utilities - removes punctuation, line breaks, and spaces
- **service/service_file.py**: File I/O operations for saving OCR results
- **utils/config_manager.py**: Configuration management - reads from config.ini (uses resource_path for PyInstaller compatibility)

### Entry Point
`main.py` imports from `app_window` and launches `OCRApplication().root.mainloop()`

### Authentication
Google Cloud Vision API credentials are stored in `.env` file at project root. The app uses service account authentication loaded via `env_loader.py`.

## Development Commands

### Running the Application
```bash
python main.py
```

### Running Tests
```bash
pytest                          # Run all tests
pytest tests/test_main.py       # Run specific test file
pytest -v                       # Verbose output
```

### Building Executable
```bash
python build.py
```
This script:
1. Auto-increments version in `app/__init__.py` (patch version)
2. Updates `docs/README.md` with new version and date
3. Runs PyInstaller with:
   - `--windowed` flag (no console window)
   - Icon from `assets/VisionOCR.ico`
   - Bundles `config.ini`
   - Output name: `VisionOCR`

### Version Management
Version is stored in `app/__init__.py` as `__version__` and `__date__`. The `scripts/version_manager.py` module handles automatic version incrementing during builds. Current version: 1.1.0

## Key Design Patterns

### Configuration System
Uses `ConfigManager` class which provides `resource_path()` to locate config.ini in both development and PyInstaller environments. Configuration includes window geometry, transparency settings, and outline width.

### Service Layer
Services are separated by concern:
- `VisionOCRService`: External API integration
- `service_text`: Pure text transformations
- `service_file`: File system operations

### GUI State Management
`OCRApplication` maintains `is_append_mode` boolean to toggle between append/overwrite modes for OCR results. Mode button updates its text dynamically.

## Testing Notes
- Test files mirror the structure of source files (e.g., `test_app_window.py` tests `app_window.py`)
- Tests use pytest framework
- All test files are in the `tests/` directory

## Important Implementation Details
- The screen capture minimizes the main window during capture to avoid capturing the app itself
- Text area uses monospace font and includes scrollbars
- Error handling uses custom exceptions from `utils/exceptions.py`
- Logging uses rotation via `utils/log_rotation.py`
