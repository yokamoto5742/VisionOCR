# 変更履歴

このプロジェクトの注目すべき変更はすべてこのファイルに記録されています。

このフォーマットは [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に基づいており、
このプロジェクトは [Semantic Versioning](https://semver.org/lang/ja/) に準拠しています。

## [Unreleased]

## [1.0.1] - 2026-05-27

### 追加
- OCR検出タイプを選択可能に：テキスト検出（text_detection）とドキュメント検出（document_text_detection）を動的に切り替え可能
- PDF処理の最大ページ数を設定可能に：config.iniで処理するPDFの最大ページ数を制御可能
- PyInstallerビルドに対応したパス解決：単体実行ファイルでも正しく.envファイルと設定ファイルを読み込み可能に改善

### 変更
- PyInstallerビルド時に.envファイルのバンドルを削除：ユーザーディレクトリから.envを読み込むように変更

## [1.0.0] - 2026-05-25
VisionOCR 初版リリース
