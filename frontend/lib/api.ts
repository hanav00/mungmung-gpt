import type { PersonaKey } from "./types";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE?.replace(/\/$/, "") ?? "http://localhost:8000";

export type KnowledgeHit = { title: string; meaning: string };

export type TranslateEvent =
  | { type: "meta"; caption: string; knowledge: KnowledgeHit[] }
  | { type: "token"; text: string }
  | { type: "done" }
  | { type: "error"; message: string };

/**
 * POST /translate 로 multipart 업로드 후 SSE 스트림을 async iterable로 반환.
 * EventSource가 POST를 지원하지 않아 fetch + ReadableStream 수동 파싱.
 */
export async function* translateStream(
  image: File,
  persona: PersonaKey,
  signal?: AbortSignal
): AsyncGenerator<TranslateEvent> {
  const form = new FormData();
  form.append("image", image);
  form.append("persona", persona);

  const res = await fetch(`${API_BASE}/translate`, {
    method: "POST",
    body: form,
    signal,
  });

  if (!res.ok || !res.body) {
    const detail = await res.text().catch(() => res.statusText);
    yield { type: "error", message: `HTTP ${res.status}: ${detail}` };
    return;
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    // SSE events are separated by a blank line (\n\n)
    let idx: number;
    while ((idx = buffer.indexOf("\n\n")) !== -1) {
      const raw = buffer.slice(0, idx);
      buffer = buffer.slice(idx + 2);
      const ev = parseSseBlock(raw);
      if (ev) yield ev;
    }
  }
}

function parseSseBlock(raw: string): TranslateEvent | null {
  let event = "message";
  let data = "";
  for (const line of raw.split("\n")) {
    if (line.startsWith("event:")) event = line.slice(6).trim();
    else if (line.startsWith("data:")) data += line.slice(5).trim();
  }
  if (!data) return null;
  try {
    const payload = JSON.parse(data);
    if (event === "meta")
      return {
        type: "meta",
        caption: payload.caption ?? "",
        knowledge: payload.knowledge ?? [],
      };
    if (event === "token") return { type: "token", text: payload.text ?? "" };
    if (event === "done") return { type: "done" };
    if (event === "error")
      return { type: "error", message: payload.message ?? "unknown error" };
  } catch {
    return { type: "error", message: `parse failed: ${data}` };
  }
  return null;
}
