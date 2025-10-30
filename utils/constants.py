import tkinter as tk

# ウィンドウ設定
DEFAULT_WINDOW_GEOMETRY = (100, 100, 800, 600)
DEFAULT_FONT_SIZE = 12
DEFAULT_FONT_FAMILY = 'MS Gothic'
DEFAULT_APP_TITLE = 'VisionOCR'

# スクリーンキャプチャ設定
DEFAULT_TRANSPARENCY = 0.3
DEFAULT_OUTLINE_WIDTH = 3
MIN_SCREENSHOT_SIZE = 5


class UIColors:
    """UI配色定数
    
    アプリケーションで使用する色を定義します。
    """
    HIGHLIGHT_PRIMARY = '#007bff'
    HIGHLIGHT_HOVER = '#0056b3'
    HIGHLIGHT_TEXT = 'white'
    SELECTION_OUTLINE = 'red'


class UILayout:
    """UIレイアウト定数
    
    ボタンやフレームのレイアウトに関する定数を定義します。
    """
    BUTTON_PADDING = 2
    FRAME_PADDING = 5
    HIGHLIGHT_FONT = ('Helvetica', 10, 'bold')
    HIGHLIGHT_BORDER_WIDTH = 3


class TextPosition:
    """テキストウィジェットの位置定数
    
    tkinterのテキストウィジェットで使用する位置指定文字列を定義します。
    """
    START = '1.0'
    END = tk.END


# ファイル設定
DEFAULT_FILE_EXTENSION = '.txt'
DEFAULT_FILE_PREFIX = 'OCR_result_'
DATETIME_FORMAT = '%Y%m%d_%H%M%S'

# エンコーディング設定
DEFAULT_ENCODING = 'utf-8'
FALLBACK_ENCODING = 'cp932'

# ログ設定
DEFAULT_LOG_DIRECTORY = 'logs'
DEFAULT_LOG_RETENTION_DAYS = 7
