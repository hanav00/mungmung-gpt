# 🐶 멍멍 GPT

우리집 강아지 사진을 올리면 표정·자세·바디랭귀지를 분석해서 **강아지 본인의 속마음**을 페르소나별로 통역해주는 멀티모달 챗봇.

## MVP 기능

- 사진 업로드 → 페르소나 선택 → 강아지 시점 독백 생성 (SSE 스트리밍)
- 페르소나 5종 (기본 `happy`: 간식/산책 러버, 감정 다양)
- **바디랭귀지 지식 RAG** — 업로드 사진의 관찰 요약을 쿼리로 Chroma 에서
  top-k 지식을 가져와 프롬프트에 주입. 참고한 관찰/지식은 결과 하단 패널에서 확인.

## 디렉토리

```
mungmung-gpt/
├── backend/           # FastAPI + LangChain (vision + RAG)
│   ├── scripts/       # seed_knowledge.py (Chroma 인덱싱)
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── prompts.py
│       ├── core/      # image_processor, generator, retriever
│       ├── api/       # /translate (SSE: meta/token/done/error)
│       ├── models/
│       └── data/
│           ├── knowledge/  # body_language.json (지식 시드)
│           └── chroma/     # 임베딩 영속화 (gitignored)
├── frontend/          # Next.js 16 + Tailwind 4
│   ├── app/
│   ├── components/    # upload/, result/
│   └── lib/           # api.ts, types.ts
└── docs/notebooks/    # 참고 강의 노트북
```

## 실행

### 1. Backend

```bash
cd backend
cp .env.example .env            # OPENAI_API_KEY 채워넣기
uv sync                         # 의존성 설치

# 최초 1회: 바디랭귀지 지식 Chroma 인덱싱 (재실행 안전)
uv run python -m scripts.seed_knowledge

uv run uvicorn app.main:app --reload --port 8000
```

→ `http://localhost:8000/docs` 에서 OpenAPI UI 확인

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

→ `http://localhost:3000`

## 다음 단계 (TODO)

- [x] **Phase 1**: 바디랭귀지 지식 RAG (Chroma + `text-embedding-3-small`)
- [ ] **Phase 2**: OpenCLIP 기반 감정 카테고리 매칭 (reference 이미지 + 코사인 유사도)
- [ ] 감정 퍼센트 (행복/지루함/배고픔 등) 구조화 출력
- [ ] 일기장 모드 (SQLite 저장 + 주간 기분 리포트)
- [ ] LangGraph 워크플로우 (analyze → retrieve → generate → save_diary)
