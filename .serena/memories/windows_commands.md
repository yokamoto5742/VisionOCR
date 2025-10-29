# Windows コマンドリファレンス

## ファイル・ディレクトリ操作

### 一覧表示
```bash
dir                    # カレントディレクトリの一覧
dir /s                 # サブディレクトリも含めて一覧
dir /b                 # ファイル名のみ表示
```

### 移動・コピー・削除
```bash
cd path                # ディレクトリ移動
mkdir dirname          # ディレクトリ作成
rmdir dirname          # 空のディレクトリ削除
rmdir /s dirname       # ディレクトリとその内容を削除
move source dest       # ファイル・ディレクトリ移動
copy source dest       # ファイルコピー
xcopy source dest /E   # ディレクトリを再帰的にコピー
del filename           # ファイル削除
```

### ファイル表示・検索
```bash
type filename          # ファイル内容表示
more filename          # ページングしてファイル内容表示
find "text" filename   # ファイル内のテキスト検索
findstr pattern files  # 正規表現でファイル検索
```

## プロセス管理
```bash
tasklist               # 実行中のプロセス一覧
taskkill /PID pid      # プロセスID指定で終了
taskkill /IM name      # プロセス名指定で終了
```

## システム情報
```bash
systeminfo             # システム情報表示
hostname               # ホスト名表示
ipconfig               # ネットワーク設定表示
set                    # 環境変数一覧
echo %VAR%             # 環境変数の値表示
```

## PowerShell
より強力な機能が必要な場合はPowerShellを使用:
```bash
powershell -Command "Get-ChildItem"  # PowerShellコマンド実行
```

### よく使うPowerShellコマンド
```powershell
Get-ChildItem          # ファイル・ディレクトリ一覧（dir相当）
Get-Content file       # ファイル内容表示（type相当）
Select-String pattern  # grep相当
Measure-Object         # 行数カウントなど
```

## 注意点
- パスの区切り文字はバックスラッシュ（`\`）
- スペースを含むパスは引用符で囲む: `"C:\Program Files\..."`
- Unix系コマンド（grep, find, sedなど）は標準では使えない
- Git Bashや WSL を使うとUnix系コマンドが使える
