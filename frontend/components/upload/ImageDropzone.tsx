"use client";

import { useCallback } from "react";
import { useDropzone } from "react-dropzone";

type Props = {
  onFile: (file: File) => void;
  preview: string | null;
  disabled?: boolean;
};

export function ImageDropzone({ onFile, preview, disabled }: Props) {
  const onDrop = useCallback(
    (files: File[]) => {
      const first = files[0];
      if (first) onFile(first);
    },
    [onFile]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/jpeg": [],
      "image/png": [],
      "image/webp": [],
      "image/heic": [],
      "image/heif": [],
    },
    maxFiles: 1,
    disabled,
  });

  return (
    <div
      {...getRootProps()}
      className={[
        "relative w-full aspect-square rounded-3xl border-2 border-dashed",
        "flex items-center justify-center text-center px-6 cursor-pointer",
        "transition-colors overflow-hidden",
        isDragActive
          ? "border-amber-400 bg-amber-50"
          : "border-zinc-300 bg-zinc-50 hover:border-amber-300 hover:bg-amber-50/40",
        disabled && "opacity-50 cursor-not-allowed",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <input {...getInputProps()} />
      {preview ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={preview}
          alt="업로드한 강아지"
          className="absolute inset-0 w-full h-full object-cover"
        />
      ) : (
        <div className="text-zinc-500">
          <div className="text-5xl mb-2">📸</div>
          <div className="font-semibold text-zinc-700">
            {isDragActive ? "여기에 놓으세요" : "강아지 사진을 드래그하거나 클릭"}
          </div>
          <div className="text-xs mt-1">JPG / PNG / WEBP / HEIC</div>
        </div>
      )}
    </div>
  );
}
