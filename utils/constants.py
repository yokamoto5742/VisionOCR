import tkinter as tk

# ウィンドウ設定
DEFAULT_WINDOW_GEOMETRY = (100, 100, 800, 600)
DEFAULT_FONT_SIZE = 12
DEFAULT_FONT_FAMILY = "MS Gothic"
DEFAULT_APP_TITLE = "VisionOCR"

# スクリーンキャプチャ設定
DEFAULT_TRANSPARENCY = 0.3
DEFAULT_OUTLINE_WIDTH = 3
MIN_SCREENSHOT_SIZE = 5


class UIColors:
    """UI配色定数"""

    HIGHLIGHT_PRIMARY = "#007bff"
    HIGHLIGHT_HOVER = "#0056b3"
    HIGHLIGHT_TEXT = "white"
    SELECTION_OUTLINE = "red"


class UILayout:
    """UIレイアウト定数"""

    BUTTON_PADDING = 2
    FRAME_PADDING = 5
    HIGHLIGHT_FONT = ("Helvetica", 10, "bold")
    HIGHLIGHT_BORDER_WIDTH = 3


class TextPosition:
    """テキストウィジェットの位置定数"""

    START = "1.0"
    END = tk.END


class UILabels:
    """ボタン・ダイアログタイトル等のラベル定数"""

    # ボタン
    BTN_CAPTURE = "範囲選択"
    BTN_SELECT_FILE = "ファイル選択"
    BTN_COPY_ALL = "全文コピー"
    BTN_SAVE_FILE = "ファイル出力"
    BTN_CLEAR = "画面クリア"
    BTN_CLOSE = "閉じる"
    BTN_REMOVE_COMMA = "読点除去"
    BTN_REMOVE_PERIOD = "句点除去"
    BTN_REMOVE_LINEBREAK = "改行除去"
    BTN_REMOVE_SPACE = "スペース除去"
    BTN_REMOVE_SEPARATOR = "区切り削除"
    MODE_APPEND = "追記"
    MODE_OVERWRITE = "上書き"

    # ダイアログタイトル
    TITLE_ERROR = "エラー"
    TITLE_WARNING = "警告"
    TITLE_INFO = "完了"
    TITLE_OCR_RESULT = "OCR結果"
    TITLE_OCR_ERROR = "OCRエラー"
    TITLE_CAPTURE_ERROR = "キャプチャエラー"
    TITLE_CONFIG_ERROR = "設定エラー"

    # ファイル選択
    PDF_DIALOG_TITLE = "PDFファイルを選択"
    PDF_FILETYPE_LABEL = "PDFファイル"
    TEXT_FILETYPE_LABEL = "テキストファイル"
    ALL_FILETYPE_LABEL = "すべてのファイル"


class UIMessages:
    """ユーザー向けメッセージ定数（必要に応じて {} プレースホルダを含む）"""

    # 情報
    INFO_COPY_DONE = "テキストをクリップボードにコピーしました。"
    INFO_SAVE_DONE = "テキストファイルを保存しました。"

    # 警告
    WARN_NO_COPY_TEXT = "コピーするテキストがありません。"
    WARN_SCREENSHOT_TOO_SMALL = "スクリーンショットの範囲が小さすぎます。"
    WARN_NO_TEXT_DETECTED = "テキストを検出できませんでした。"

    # エラー（テンプレート）
    ERR_WINDOW_CONFIG_LOAD = "ウィンドウ設定の読み込みに失敗: {error}"
    ERR_TEXT_AREA_CREATE = "テキストエリアの作成に失敗: {error}"
    ERR_UNEXPECTED = "予期せぬエラーが発生: {error}"
    ERR_UNEXPECTED_DETAIL = "予期せぬエラーが発生しました: {error}"
    ERR_CLIPBOARD_TCL = "Tclエラー: クリップボードへのアクセスに失敗しました。\n{error}"
    ERR_CLIPBOARD_COPY = "クリップボードへのコピーに失敗: {error}"
    ERR_FILE_SAVE = "ファイルの保存に失敗: {error}"
    ERR_PDF_PROCESS = "PDF処理中にエラーが発生しました: {error}"
    ERR_CLEAR_SCREEN = "画面のクリアに失敗: {error}"
    ERR_CONFIG_LOAD = "設定の読み込み中にエラーが発生しました: {error}"
    ERR_OCR_DETECT = "テキスト認識中にエラーが発生しました: {error}"
    ERR_CAPTURE_PROCESS = "スクリーンショット処理中にエラーが発生しました: {error}"
    ERR_FILE_PERMISSION = "ファイルへのアクセス権限がありません。"
    ERR_FILE_OS = "ファイル操作エラー: {error}"

    # PDF処理
    PDF_PAGE_FOOTER = "--- {page_num}ページ目 ---"
    PDF_OCR_FAILED = "[テキストを検出できませんでした]"

    # 座標エラー（プログラム内部用、ユーザー表示ではない）
    COORD_INVALID = "スクリーンショットの座標が正しく設定されていません"

    # Vision OCR サービス（RuntimeError/ValueError として送出される）
    ERR_VISION_CLIENT_INIT = "Vision APIクライアントの初期化に失敗しました: {error}"
    ERR_VISION_API = "Vision API エラー: {error}"
    ERR_OCR_NO_TEXT = "テキストを検出できませんでした"
    ERR_OCR_NO_EXTRACT = "テキストを抽出できませんでした"
    ERR_OCR_PROCESS = "OCR処理中にエラーが発生しました: {error}"


# ファイル設定
DEFAULT_FILE_EXTENSION = ".txt"
DEFAULT_FILE_PREFIX = "OCR_result_"
DATETIME_FORMAT = "%Y%m%d_%H%M%S"

# エンコーディング設定
DEFAULT_ENCODING = "utf-8"
FALLBACK_ENCODING = "cp932"
