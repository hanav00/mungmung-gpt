"""바디랭귀지 지식 retriever — Chroma + OpenAI 임베딩.

사용 측(generator)에서 caption 텍스트로 호출하면 유사한 지식 top-k 를 반환한다.
컬렉션이 비어 있으면 경고만 찍고 빈 리스트를 반환해 파이프라인을 끊지 않는다.
"""
from __future__ import annotations

from functools import lru_cache

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from app.config import (
    CHROMA_DIR,
    EMBEDDING_MODEL,
    KNOWLEDGE_COLLECTION,
    RETRIEVE_TOP_K,
)


@lru_cache(maxsize=1)
def _get_store() -> Chroma:
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return Chroma(
        collection_name=KNOWLEDGE_COLLECTION,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )


def retrieve_knowledge(query: str, k: int = RETRIEVE_TOP_K) -> list[Document]:
    store = _get_store()
    try:
        if not store.get().get("ids"):
            print(
                f"[retriever] collection '{KNOWLEDGE_COLLECTION}' is empty. "
                f"seed it with: uv run python -m scripts.seed_knowledge"
            )
            return []
    except Exception as exc:
        print(f"[retriever] warm-up failed: {exc}")
        return []

    return store.similarity_search(query, k=k)


def format_knowledge_block(docs: list[Document]) -> str:
    """검색된 지식을 LLM 프롬프트에 주입하기 좋은 형태로 포맷."""
    if not docs:
        return ""
    lines = []
    for i, d in enumerate(docs, 1):
        title = d.metadata.get("title", "")
        meaning = d.metadata.get("meaning", "")
        detail = d.page_content.split("상세: ", 1)[-1]
        lines.append(f"{i}. {title} → {meaning}\n   {detail}")
    return "\n".join(lines)
