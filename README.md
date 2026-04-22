# 🐶 멍멍 GPT

우리집 강아지 사진을 올리면 표정·자세·바디랭귀지를 분석해서 **강아지 본인의 속마음**을 페르소나별로 통역해주는 멀티모달 챗봇.

## MVP 기능

- 사진 업로드 → 페르소나 선택 → 강아지 시점 독백 생성 (SSE 스트리밍)
- 페르소나 5종 (기본 `happy`: 간식/산책 러버, 감정 다양)

## 디렉토리

```
mungmung-gpt/
├── backend/           # FastAPI + LangChain (vision)
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── prompts.py
│       ├── core/      # image_processor, generator
│       ├── api/       # /translate (SSE)
│       └── models/
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

- [ ] 감정 퍼센트 (행복/지루함/배고픔 등) 구조화 출력
- [ ] 바디랭귀지 지식 RAG (`MultiVectorRetriever`, Chroma)
- [ ] OpenCLIP 기반 유사 표정 태깅
- [ ] 일기장 모드 (SQLite 저장 + 주간 기분 리포트)
- [ ] LangGraph 워크플로우 (analyze → retrieve → generate → save_diary)
