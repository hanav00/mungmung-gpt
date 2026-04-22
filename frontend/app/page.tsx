"use client";

import { useEffect, useRef, useState } from "react";

import { ImageDropzone } from "@/components/upload/ImageDropzone";
import { PersonaSelector } from "@/components/upload/PersonaSelector";
import { TranslationBubble } from "@/components/result/TranslationBubble";
import { translateStream } from "@/lib/api";
import { DEFAULT_PERSONA, type PersonaKey } from "@/lib/types";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [persona, setPersona] = useState<PersonaKey>(DEFAULT_PERSONA);

  const [translation, setTranslation] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (!file) {
      setPreview(null);
      return;
    }
    const url = URL.createObjectURL(file);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  useEffect(() => {
    return () => abortRef.current?.abort();
  }, []);

  async function handleTranslate() {
    if (!file || streaming) return;
    setError(null);
    setTranslation("");
    setStreaming(true);

    const ctrl = new AbortController();
    abortRef.current = ctrl;

    try {
      for await (const ev of translateStream(file, persona, ctrl.signal)) {
        if (ev.type === "token") setTranslation((t) => t + ev.text);
        else if (ev.type === "error") setError(ev.message);
        else if (ev.type === "done") break;
      }
    } catch (err) {
      if ((err as Error).name !== "AbortError") {
        setError((err as Error).message);
      }
    } finally {
      setStreaming(false);
    }
  }

  return (
    <main className="flex flex-1 justify-center bg-gradient-to-b from-amber-50 via-white to-white">
      <div className="w-full max-w-2xl px-5 py-10 space-y-6">
        <header className="text-center space-y-1">
          <h1 className="text-3xl font-bold tracking-tight text-zinc-900">
            🐶 멍멍 GPT
          </h1>
          <p className="text-sm text-zinc-500">
            우리집 강아지 사진을 올리면 속마음을 통역해드려요.
          </p>
        </header>

        <ImageDropzone
          onFile={setFile}
          preview={preview}
          disabled={streaming}
        />

        <section className="space-y-2">
          <div className="text-sm font-semibold text-zinc-700">페르소나</div>
          <PersonaSelector
            value={persona}
            onChange={setPersona}
            disabled={streaming}
          />
        </section>

        <button
          type="button"
          onClick={handleTranslate}
          disabled={!file || streaming}
          className={[
            "w-full py-3 rounded-2xl font-semibold text-white transition-colors",
            !file || streaming
              ? "bg-zinc-300 cursor-not-allowed"
              : "bg-amber-500 hover:bg-amber-600",
          ].join(" ")}
        >
          {streaming ? "통역 중..." : "통역 시작"}
        </button>

        {(translation || streaming) && (
          <section className="pt-2">
            <TranslationBubble
              text={translation}
              persona={persona}
              streaming={streaming}
            />
          </section>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-2xl px-4 py-3 text-sm">
            {error}
          </div>
        )}
      </div>
    </main>
  );
}
