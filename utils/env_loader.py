import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv


def load_environment_variables():
    base_dir = Path(__file__).parent.parent
    env_path = os.path.join(base_dir, '.env')

    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(".envファイルを読み込みました")
    else:
        print("警告: .envファイルが見つかりません。")


def get_google_credentials() -> Dict[str, str]:
    """Google Cloud認証情報を.envから取得"""
    load_environment_variables()

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
        "universe_domain": os.getenv("UNIVERSE_DOMAIN")
    }

    if not credentials["project_id"]:
        raise ValueError(".envファイルにPROJECT_IDが設定されていません")

    return credentials
