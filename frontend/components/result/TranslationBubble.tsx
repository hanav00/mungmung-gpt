"use client";

import { PERSONAS, type PersonaKey } from "@/lib/types";

type Props = {
  text: string;
  persona: PersonaKey;
  streaming: boolean;
};

export function TranslationBubble({ text, persona, streaming }: Props) {
  const p = PERSONAS.find((x) => x.key === persona) ?? PERSONAS[0];

  return (
    <div className="flex gap-3">
      <div className="shrink-0 w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center text-2xl">
        {p.emoji}
      </div>
      <div className="flex-1 bg-white rounded-3xl rounded-tl-md border border-zinc-200 px-5 py-4 shadow-sm">
        <div className="text-xs text-amber-700 font-semibold mb-1">
          {p.label} 모드
        </div>
        <div className="text-zinc-900 leading-relaxed whitespace-pre-wrap min-h-[1.5em]">
          {text || (streaming ? "..." : "")}
          {streaming && text && <span className="animate-pulse">▍</span>}
        </div>
      </div>
    </div>
  );
}
