import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_MB", "80")) * 1024 * 1024
    SERVICE_MODE = os.getenv("SERVICE_MODE", "all")

    BASE_DIR = Path(__file__).resolve().parent.parent
    UPLOAD_FOLDER = BASE_DIR / "instance" / "uploads"
    OUTPUT_FOLDER = BASE_DIR / "instance" / "outputs"

    @classmethod
    def init_app(cls, app):
        cls.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
