import logging
import os
import re
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler

from utils.config_manager import ConfigManager

_SECTION = "LOGGING"


def _get_str(cm: ConfigManager, key: str, default: str) -> str:
    return cm.config.get(_SECTION, key, fallback=default)


def _get_int(cm: ConfigManager, key: str, default: int) -> int:
    return cm.config.getint(_SECTION, key, fallback=default)


def _get_bool(cm: ConfigManager, key: str, default: bool) -> bool:
    return cm.config.getboolean(_SECTION, key, fallback=default)


def _resolve_log_directory(log_directory: str) -> str:
    if not os.path.isabs(log_directory):
        project_root = os.path.dirname(os.path.dirname(__file__))
        log_directory = os.path.join(project_root, log_directory)
    return log_directory


def setup_logging(config_manager: ConfigManager | None = None) -> None:
    cm = config_manager or ConfigManager()

    try:
        log_directory = _resolve_log_directory(_get_str(cm, "log_directory", "logs"))
        log_retention_days = _get_int(cm, "log_retention_days", 7)
        project_name = _get_str(cm, "project_name", "VisionOCR")
        log_level = _get_str(cm, "log_level", "INFO")

        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        log_file = os.path.join(log_directory, f"{project_name}.log")

        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="midnight",
            backupCount=log_retention_days,
            encoding="utf-8",
        )
        file_handler.suffix = "%Y-%m-%d.log"

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        root_logger = logging.getLogger()

        try:
            level = getattr(logging, log_level.upper())
            root_logger.setLevel(level)
        except AttributeError:
            root_logger.setLevel(logging.INFO)
            logging.warning(
                f"無効なログレベル '{log_level}' が指定されました。INFOを使用します。"
            )

        root_logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.WARNING)
        root_logger.addHandler(console_handler)

        cleanup_old_logs(log_directory, log_retention_days, project_name)

        logging.info(f"ログシステムが初期化されました: {log_file}")

    except PermissionError as e:
        raise PermissionError(f"ログディレクトリの作成権限がありません: {e}")
    except Exception as e:
        raise Exception(f"ログ設定の初期化中にエラーが発生しました: {e}")


def cleanup_old_logs(
    log_directory: str, retention_days: int, project_name: str
) -> None:
    try:
        now = datetime.now()
        main_log_file = f"{project_name}.log"

        rotated_log_pattern = (
            rf"{re.escape(project_name)}\.log\.\d{{4}}-\d{{2}}-\d{{2}}\.log$"
        )

        deleted_count = 0
        for filename in os.listdir(log_directory):
            if filename.endswith(".log") and filename != main_log_file:
                if re.match(rotated_log_pattern, filename):
                    file_path = os.path.join(log_directory, filename)
                    try:
                        file_modification_time = datetime.fromtimestamp(
                            os.path.getmtime(file_path)
                        )
                        if now - file_modification_time >= timedelta(
                            days=retention_days
                        ):
                            os.remove(file_path)
                            logging.info(f"古いログファイルを削除しました: {filename}")
                            deleted_count += 1
                    except OSError as e:
                        logging.error(
                            f"ログファイルの削除中にエラーが発生しました {filename}: {str(e)}"
                        )

        if deleted_count > 0:
            logging.info(f"合計 {deleted_count} 個の古いログファイルを削除しました")

    except Exception as e:
        logging.error(f"ログクリーンアップ処理中にエラーが発生しました: {str(e)}")


def setup_debug_logging(
    config_manager: ConfigManager | None = None,
) -> logging.Logger | None:
    cm = config_manager or ConfigManager()

    try:
        if not _get_bool(cm, "debug_mode", False):
            return None

        log_directory = _resolve_log_directory(_get_str(cm, "log_directory", "logs"))

        debug_logger = logging.getLogger("debug")
        debug_logger.setLevel(logging.DEBUG)

        debug_log_path = os.path.join(log_directory, "debug.log")
        debug_handler = logging.FileHandler(debug_log_path, encoding="utf-8")
        debug_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )
        debug_handler.setFormatter(debug_formatter)
        debug_logger.addHandler(debug_handler)
        debug_logger.propagate = False

        logging.info(f"デバッグログが有効化されました: {debug_log_path}")
        return debug_logger

    except Exception as e:
        logging.error(f"デバッグログ設定中にエラーが発生しました: {str(e)}")
        return None


def get_log_info(
    config_manager: ConfigManager | None = None,
) -> dict[str, str | int | bool | None] | None:
    cm = config_manager or ConfigManager()

    try:
        log_directory = _resolve_log_directory(_get_str(cm, "log_directory", "logs"))
        project_name = _get_str(cm, "project_name", "VisionOCR")
        log_retention_days = _get_int(cm, "log_retention_days", 7)
        debug_mode = _get_bool(cm, "debug_mode", False)

        return {
            "log_directory": log_directory,
            "project_name": project_name,
            "log_retention_days": log_retention_days,
            "debug_mode": debug_mode,
            "main_log_file": os.path.join(log_directory, f"{project_name}.log"),
            "debug_log_file": os.path.join(log_directory, "debug.log")
            if debug_mode
            else None,
        }

    except Exception as e:
        logging.error(f"ログ情報取得中にエラーが発生しました: {str(e)}")
        return None
