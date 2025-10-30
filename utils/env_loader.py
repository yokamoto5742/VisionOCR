import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv

REQUIRED_CREDENTIAL_FIELDS = [
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "auth_uri",
    "token_uri"
]

OPTIONAL_CREDENTIAL_FIELDS = {
    "auth_provider_x509_cert_url": None,
    "client_x509_cert_url": None,
    "universe_domain": "googleapis.com"
}

def load_environment_variables() -> None:
    """環境変数を.envファイルから読み込み"""
    base_dir = Path(__file__).parent.parent
    env_path = os.path.join(base_dir, '.env')

    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(".envファイルを読み込みました")
    else:
        print("警告: .envファイルが見つかりません。")


def get_google_credentials() -> Dict[str, str]:
    """Google Cloud認証情報を.envから取得して検証

    Returns:
        Dict[str, str]: 認証情報の辞書

    Raises:
        ValueError: 必須フィールドが不足している場合
    """
    load_environment_variables()

    # 認証情報を取得
    credentials = {
        "type": os.getenv("TYPE"),
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": os.getenv("PRIVATE_KEY"),
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("UNIVERSE_DOMAIN", "googleapis.com")
    }

    # 必須フィールドの検証
    missing_fields = [
        field for field in REQUIRED_CREDENTIAL_FIELDS
        if not credentials.get(field)
    ]

    if missing_fields:
        raise ValueError(
            f".envファイルに以下の必須フィールドが設定されていません: "
            f"{', '.join(missing_fields)}"
        )

    return credentials


def validate_credentials(credentials: Dict[str, str]) -> bool:
    """認証情報の妥当性を検証

    Args:
        credentials: 検証する認証情報

    Returns:
        bool: 妥当な場合True
    """
    # 基本的な検証
    if not credentials.get("project_id"):
        return False

    if not credentials.get("private_key"):
        return False

    if not "@" in credentials.get("client_email", ""):
        return False

    return True
