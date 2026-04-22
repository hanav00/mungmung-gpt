from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class PersonaKey(str, Enum):
    happy = "happy"
    tsundere = "tsundere"
    poet = "poet"
    mz = "mz"
    ahjussi = "ahjussi"


class HealthResponse(BaseModel):
    status: str
    version: str
