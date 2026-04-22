"""POST /translate — 멀티파트로 사진+페르소나 받고 SSE로 스트리밍.

SSE 이벤트 포맷:
  event: token     data: {"text": "<chunk>"}     # 토큰 단위 부분 응답
  event: done      data: {}                       # 정상 종료
  event: error     data: {"message": "..."}       # 에러 시

프론트엔드는 EventSource가 POST를 지원하지 않으므로
fetch + ReadableStream으로 수신/파싱하는 것을 상정한다.
"""
from __future__ import annotations

import json
from typing import AsyncIterator

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.config import DEFAULT_PERSONA
from app.core.generator import translate_stream
from app.core.image_processor import preprocess_image
from app.models.schemas import PersonaKey

router = APIRouter(tags=["translate"])

_VALID_PERSONAS = {p.value for p in PersonaKey}


def _sse_event(event: str, data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {payload}\n\n"


@router.post("/translate")
async def translate(
    image: UploadFile = File(..., description="강아지 사진 (JPG/PNG/HEIC)"),
    persona: str = Form(DEFAULT_PERSONA, description="페르소나 키"),
) -> StreamingResponse:
    if persona not in _VALID_PERSONAS:
        raise HTTPException(
            status_code=400,
            detail=f"unknown persona '{persona}'. valid: {sorted(_VALID_PERSONAS)}",
        )

    raw = await image.read()
    if not raw:
        raise HTTPException(status_code=400, detail="empty image upload")

    processed = preprocess_image(raw)

    async def event_stream() -> AsyncIterator[str]:
        try:
            async for token in translate_stream(processed, persona):
                yield _sse_event("token", {"text": token})
            yield _sse_event("done", {})
        except Exception as exc:
            yield _sse_event("error", {"message": str(exc)})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
