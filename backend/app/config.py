"""Runtime 설정.

`.env` 또는 셸 환경변수에서 값을 읽는다. 프로젝트 전역 상수도 여기 모은다 —
모델명/경로 같은 값을 파일마다 흩어놓지 않기 위함이다.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR: Path = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
VISION_MODEL: str = os.getenv("VISION_MODEL", "gpt-4.1-mini")
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

MAX_IMAGE_SIDE: int = int(os.getenv("MAX_IMAGE_SIDE", "1024"))
JPEG_QUALITY: int = int(os.getenv("JPEG_QUALITY", "85"))

KNOWLEDGE_JSON_PATH: Path = BASE_DIR / "data" / "knowledge" / "body_language.json"
CHROMA_DIR: Path = DATA_DIR / "chroma"
KNOWLEDGE_COLLECTION: str = "dog_knowledge"
RETRIEVE_TOP_K: int = int(os.getenv("RETRIEVE_TOP_K", "5"))

CORS_ORIGINS: list[str] = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if o.strip()
]

DEFAULT_PERSONA: str = "happy"
