"""PIL 기반 이미지 전처리.

업로드 원본(HEIC/PNG/거대한 JPG 등)을 vision LLM이 소화하기 좋은
JPEG 바이트로 정규화한다.

MVP 정책: **비율 유지 리사이즈 + RGB 변환 + JPEG 재인코딩**만 수행한다.
정사각 패딩은 CLIP 임베딩 도입 단계에서 별도 함수로 추가 예정.
"""
from __future__ import annotations

import io

from PIL import Image, ImageOps

from app.config import JPEG_QUALITY, MAX_IMAGE_SIDE


def preprocess_image(
    raw: bytes,
    max_side: int = MAX_IMAGE_SIDE,
    jpeg_quality: int = JPEG_QUALITY,
) -> bytes:
    """바이트 → 바이트. LLM 호출 직전에 부른다.

    - EXIF 회전 반영 (핸드폰 사진의 세로/가로 회전 처리)
    - 긴 변을 `max_side` 이하로 축소 (비율 유지)
    - RGB 변환 후 JPEG로 재인코딩
    """
    img = Image.open(io.BytesIO(raw))
    img = ImageOps.exif_transpose(img)
    if img.mode != "RGB":
        img = img.convert("RGB")

    w, h = img.size
    longest = max(w, h)
    if longest > max_side:
        scale = max_side / longest
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=jpeg_quality, optimize=True)
    return buf.getvalue()
