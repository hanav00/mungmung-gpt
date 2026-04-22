"""FastAPI 엔트리포인트.

MVP 단계에서는 /health 만 노출한다. /translate 등 실제 기능 라우터는
이후 커밋에서 붙인다.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import translate as translate_api
from app.config import CORS_ORIGINS
from app.models.schemas import HealthResponse

app = FastAPI(
    title="강아지 표정 통역기",
    description="사진을 업로드하면 강아지 표정을 통역해주는 멀티모달 챗봇",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(translate_api.router)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=app.version)
