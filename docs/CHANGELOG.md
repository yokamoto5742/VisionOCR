# 変更履歴

このプロジェクトの注目すべき変更はすべてこのファイルに記録されています。

このフォーマットは [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に基づいており、
このプロジェクトは [Semantic Versioning](https://semver.org/lang/ja/) に準拠しています。

## [Unreleased]

## [1.1.1] - 2025-11-01

### 変更
- docs/README.mdを大幅に更新・充実化
  - プロジェクト概要と主な機能を追加
  - 必要要件を明記
  - インストール方法を詳細化（.env設定手順を含む）
  - 使用方法とワークフローを説明
  - プロジェクト構成を詳細化
  - アーキテクチャセクションを新規追加（レイヤード設計、コンポーネント構成、データフロー）
  - 開発コマンドを充実化
  - トラブルシューティングセクションを追加
  - 開発環境セットアップガイドを追加

## [1.1.0] - 2025-10-31

### 追加
- ウィジェットファクトリ機能：ボタンリストからウィジェットを作成・配置

### 変更
- config_manager.pyをリファクタリング：コメントを整理してエラー表示を追加
- env_loader.pyの不要なコメント削除と認証情報検証部分を整理
- utils/constants.pyのコメント簡潔化と不要な改行を削除
- サービスレイヤーの日本語コメントを簡潔に修正
- メインUIの説明を明確化

[Unreleased]: https://github.com/yourusername/VisionOCR/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/yourusername/VisionOCR/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/yourusername/VisionOCR/releases/tag/v1.1.0
