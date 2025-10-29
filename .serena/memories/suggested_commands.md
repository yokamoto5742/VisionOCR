# 推奨コマンド

## アプリケーション実行
```bash
python main.py
```

## テスト
```bash
# 全テスト実行
pytest

# 詳細出力
pytest -v

# 特定のテストファイル実行
pytest tests/test_app_window.py

# 警告を非表示
pytest --disable-warnings

# 短いトレースバック
pytest --tb=short
```

## ビルド（実行ファイル作成）
```bash
python build.py
```
このスクリプトは以下を実行:
1. app/__init__.pyのバージョン番号を自動インクリメント（パッチバージョン）
2. docs/README.mdのバージョンと日付を更新
3. PyInstallerで実行ファイルをビルド
   - --windowedフラグ（コンソールウィンドウなし）
   - assets/VisionOCR.icoをアイコンに設定
   - config.iniをバンドル
   - 出力名: VisionOCR

## パッケージ管理
```bash
# 依存関係のインストール
pip install -r requirements.txt

# パッケージの更新確認
pip-review

# パッケージの自動更新
pip-review --auto
```

## Windows特有のコマンド
```bash
# ディレクトリ一覧
dir

# ファイル移動
move source destination

# ディレクトリ作成
mkdir dirname

# ファイルコピー
copy source destination

# ファイル削除
del filename

# ディレクトリ削除
rmdir /s dirname

# PowerShellコマンド実行
powershell -Command "command"
```

## Git操作
```bash
# ステータス確認
git status

# 変更をステージング
git add .

# コミット
git commit -m "message"

# プッシュ
git push

# プル
git pull

# ブランチ一覧
git branch

# 差分確認
git diff
```
