export type PersonaKey = "happy" | "tsundere" | "poet" | "mz" | "ahjussi";

export type PersonaOption = {
  key: PersonaKey;
  label: string;
  emoji: string;
  description: string;
};

export const PERSONAS: PersonaOption[] = [
  {
    key: "happy",
    label: "해맑이",
    emoji: "🐶",
    description: "간식·산책 러버 · 감정 다양 · 단순",
  },
  {
    key: "tsundere",
    label: "츤데레",
    emoji: "😼",
    description: "겉은 새침, 속은 집사 바라기",
  },
  {
    key: "poet",
    label: "시인",
    emoji: "📜",
    description: "은유와 운율로 감정을 노래",
  },
  {
    key: "mz",
    label: "MZ",
    emoji: "✨",
    description: "ㅇㅈ, 킹받네, 갓벽…",
  },
  {
    key: "ahjussi",
    label: "아재",
    emoji: "🧔",
    description: "허허, 라네, 에잉",
  },
];

export const DEFAULT_PERSONA: PersonaKey = "happy";
