"""지식 시드 JSON을 Chroma 컬렉션에 임베딩해서 저장한다.

실행:
    cd backend
    uv run python -m scripts.seed_knowledge

이미 존재하는 컬렉션은 삭제 후 재생성한다 (재실행 안전).
"""
from __future__ import annotations

import json

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from app.config import (
    CHROMA_DIR,
    EMBEDDING_MODEL,
    KNOWLEDGE_COLLECTION,
    KNOWLEDGE_JSON_PATH,
)


def _build_document(entry: dict) -> Document:
    """검색 대상 텍스트는 title + meaning + detail 을 합친다."""
    page = (
        f"[{entry['category']}] {entry['title']}\n"
        f"의미: {entry['meaning']}\n"
        f"상세: {entry['detail']}"
    )
    return Document(
        page_content=page,
        metadata={
            "id": entry["id"],
            "category": entry["category"],
            "title": entry["title"],
            "meaning": entry["meaning"],
        },
    )


def main() -> None:
    entries = json.loads(KNOWLEDGE_JSON_PATH.read_text(encoding="utf-8"))
    docs = [_build_document(e) for e in entries]
    ids = [e["id"] for e in entries]

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    store = Chroma(
        collection_name=KNOWLEDGE_COLLECTION,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    existing = store.get()
    if existing.get("ids"):
        store.delete(ids=existing["ids"])
        print(f"cleared {len(existing['ids'])} existing docs")

    store.add_documents(docs, ids=ids)
    print(f"indexed {len(docs)} knowledge entries into '{KNOWLEDGE_COLLECTION}'")
    print(f"persist dir: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
