"use client";

import { PERSONAS, type PersonaKey } from "@/lib/types";

type Props = {
  value: PersonaKey;
  onChange: (key: PersonaKey) => void;
  disabled?: boolean;
};

export function PersonaSelector({ value, onChange, disabled }: Props) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
      {PERSONAS.map((p) => {
        const selected = p.key === value;
        return (
          <button
            key={p.key}
            type="button"
            disabled={disabled}
            onClick={() => onChange(p.key)}
            className={[
              "flex flex-col items-center gap-1 px-2 py-3 rounded-2xl border text-center",
              "transition-colors",
              selected
                ? "border-amber-400 bg-amber-50 text-amber-900"
                : "border-zinc-200 bg-white text-zinc-700 hover:border-amber-200",
              disabled && "opacity-50 cursor-not-allowed",
            ].join(" ")}
            aria-pressed={selected}
          >
            <span className="text-2xl leading-none">{p.emoji}</span>
            <span className="text-sm font-semibold">{p.label}</span>
            <span className="text-[10px] text-zinc-500 leading-tight">
              {p.description}
            </span>
          </button>
        );
      })}
    </div>
  );
}
