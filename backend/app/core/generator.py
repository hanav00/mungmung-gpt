"""비전 LLM 호출 — 강아지 내면 독백을 토큰 단위로 스트리밍한다.

MVP 범위: 사진(bytes) + 페르소나 → GPT-4.1-mini vision → 한국어 스트리밍 텍스트.
RAG 검색 / CLIP 감정 태깅 / 일기장 저장은 LangGraph 노드로 이후 단계에서 덧붙인다.
"""
from __future__ import annotations

import base64
from typing import AsyncIterator

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.config import VISION_MODEL
from app.prompts import build_system_prompt

_USER_INSTRUCTION = (
    "이 강아지의 표정·자세·바디랭귀지를 살펴보고, 강아지 본인의 속마음을 "
    "그대로 말해줘. 짧고 생생하게."
)


def _data_url(image_bytes: bytes, mime: str = "image/jpeg") -> str:
    b64 = base64.b64encode(image_bytes).decode()
    return f"data:{mime};base64,{b64}"


async def translate_stream(
    image_bytes: bytes,
    persona_key: str,
    *,
    temperature: float = 0.85,
) -> AsyncIterator[str]:
    """페르소나에 맞춰 강아지 속마음을 한국어 스트리밍."""
    llm = ChatOpenAI(
        model=VISION_MODEL,
        streaming=True,
        temperature=temperature,
    )
    messages = [
        SystemMessage(content=build_system_prompt(persona_key)),
        HumanMessage(
            content=[
                {"type": "text", "text": _USER_INSTRUCTION},
                {"type": "image_url", "image_url": {"url": _data_url(image_bytes)}},
            ]
        ),
    ]

    async for chunk in llm.astream(messages):
        content = chunk.content
        if isinstance(content, str) and content:
            yield content
