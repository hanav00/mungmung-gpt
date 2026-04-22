"use client";

import type { KnowledgeHit } from "@/lib/api";

type Props = {
  caption: string;
  knowledge: KnowledgeHit[];
};

export function KnowledgePanel({ caption, knowledge }: Props) {
  if (!caption && knowledge.length === 0) return null;

  return (
    <details className="rounded-2xl border border-zinc-200 bg-white px-4 py-3 text-sm text-zinc-700">
      <summary className="cursor-pointer font-semibold text-zinc-800">
        🔎 참고한 관찰 & 지식
      </summary>

      {caption && (
        <div className="mt-3">
          <div className="text-xs font-semibold text-zinc-500 mb-1">
            관찰 요약
          </div>
          <div className="whitespace-pre-wrap text-zinc-800 leading-relaxed">
            {caption}
          </div>
        </div>
      )}

      {knowledge.length > 0 && (
        <div className="mt-3">
          <div className="text-xs font-semibold text-zinc-500 mb-1">
            검색된 지식 (top {knowledge.length})
          </div>
          <ul className="space-y-1">
            {knowledge.map((k, i) => (
              <li key={i} className="text-zinc-800">
                <span className="font-medium">{k.title}</span>
                <span className="text-zinc-500"> — {k.meaning}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </details>
  );
}
