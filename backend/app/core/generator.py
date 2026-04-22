"""비전 RAG 통역 파이프라인.

단계:
  1. caption_observation — 사진에서 관찰 가능한 특징만 짧게 뽑아낸다 (해석 금지)
  2. retrieve_knowledge — caption 을 쿼리로 바디랭귀지 지식 top-k 검색
  3. translate_stream   — 페르소나 + 지식 + 사진을 함께 넣고 한국어 독백을 스트리밍

Phase 2 에서는 (1) 이후 CLIP 감정 매칭이 추가되고, 그 결과도 프롬프트에 주입된다.
"""
from __future__ import annotations

import base64
from typing import AsyncIterator

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.config import VISION_MODEL
from app.core.retriever import format_knowledge_block, retrieve_knowledge
from app.prompts import build_system_prompt

_CAPTION_INSTRUCTION = (
    "Observe the dog's physical features only — no interpretation. "
    "List 3 to 5 short Korean bullet points covering: 귀 위치/방향, 꼬리 높이·움직임, "
    "눈매, 입/혀 상태, 전반적 자세·몸의 긴장도. 20단어 이내로 각 bullet 을 간결하게."
)

_USER_INSTRUCTION = (
    "이 강아지의 표정·자세·바디랭귀지를 살펴보고, 강아지 본인의 속마음을 "
    "그대로 말해줘. 짧고 생생하게."
)


def _data_url(image_bytes: bytes, mime: str = "image/jpeg") -> str:
    b64 = base64.b64encode(image_bytes).decode()
    return f"data:{mime};base64,{b64}"


async def _caption_observation(image_bytes: bytes) -> str:
    """사진에서 관찰 가능한 피처만 bullet 로 뽑아낸다. RAG 쿼리용."""
    llm = ChatOpenAI(model=VISION_MODEL, temperature=0)
    result = await llm.ainvoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": _CAPTION_INSTRUCTION},
                    {"type": "image_url", "image_url": {"url": _data_url(image_bytes)}},
                ]
            )
        ]
    )
    content = result.content
    return content if isinstance(content, str) else str(content)


def _build_system(persona_key: str, knowledge_block: str) -> str:
    base = build_system_prompt(persona_key)
    if not knowledge_block:
        return base
    return (
        f"{base}\n\n"
        "다음은 강아지 바디랭귀지에 대한 참고 지식이다. 이 지식을 바탕으로 "
        "사진 속 강아지의 상태를 해석한 뒤, 페르소나 말투로 속마음을 전달하라. "
        "지식을 그대로 나열하지 말고 감정·행동으로 녹여서 표현하라.\n"
        f"---\n{knowledge_block}\n---"
    )


async def translate_stream(
    image_bytes: bytes,
    persona_key: str,
    *,
    temperature: float = 0.85,
) -> AsyncIterator[dict]:
    """Yield 이벤트 dict.

      {"kind": "meta", "caption": "...", "knowledge": [{"title","meaning"}, ...]}
      {"kind": "token", "text": "..."}
    """
    caption = await _caption_observation(image_bytes)
    docs = retrieve_knowledge(caption)
    knowledge_block = format_knowledge_block(docs)

    yield {
        "kind": "meta",
        "caption": caption,
        "knowledge": [
            {
                "title": d.metadata.get("title", ""),
                "meaning": d.metadata.get("meaning", ""),
            }
            for d in docs
        ],
    }

    llm = ChatOpenAI(
        model=VISION_MODEL,
        streaming=True,
        temperature=temperature,
    )
    messages = [
        SystemMessage(content=_build_system(persona_key, knowledge_block)),
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
            yield {"kind": "token", "text": content}
