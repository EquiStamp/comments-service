import os
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.environ.get("DB_USERNAME", "comments_admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "dont let me down")
DB_ENDPOINT = os.environ.get("DB_ENDPOINT", "0.0.0.0")
DB_PORT = os.environ.get("DB_PORT", 3306)
DB_NAME = os.environ.get("DB_NAME", "comments_db")
