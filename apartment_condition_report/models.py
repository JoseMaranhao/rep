from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Photo:
    path: Path
    source: str
    evidence_filename: str


@dataclass(frozen=True)
class Finding:
    category: str
    severity: str
    description: str
    location: str
    confidence: str
    photo_source: str
    evidence_filename: str


@dataclass
class Report:
    title: str
    created_at: str
    findings: list[Finding] = field(default_factory=list)
    reviewed_photos: int = 0
