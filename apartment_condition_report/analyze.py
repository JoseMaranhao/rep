from __future__ import annotations

import base64
import json
import os
from openai import OpenAI

from .models import Finding, Photo

PROMPT = """You are reviewing move-in apartment photos to preserve factual evidence.
Identify only clearly visible pre-existing conditions likely relevant to a rental inspection:
paint damage/scuffs/holes, stains, dirt or residue, cracks, chips, water damage, broken or missing fixtures, and damaged floors/windows/cabinets/appliances.
Do not infer hidden damage, cause, age, responsibility, or repair costs. Do not identify people or sensitive personal items.
Return JSON only: an array of objects with category, severity (low|medium|high), description, location, confidence (low|medium|high).
If nothing is clearly visible, return []."""


def analyze_photo(photo: Photo, client: OpenAI | None = None, model: str | None = None) -> list[Finding]:
    """Ask a vision model for conservative, structured observations for one photo."""
    client = client or OpenAI()
    model = model or os.environ.get("OPENAI_VISION_MODEL", "gpt-4.1-mini")
    mime = "image/jpeg" if photo.path.suffix.lower() in {".jpg", ".jpeg"} else f"image/{photo.path.suffix.lower().lstrip('.')}"
    data_url = f"data:{mime};base64,{base64.b64encode(photo.path.read_bytes()).decode()}"
    response = client.responses.create(
        model=model,
        input=[{"role": "user", "content": [
            {"type": "input_text", "text": PROMPT},
            {"type": "input_image", "image_url": data_url, "detail": "high"},
        ]}],
    )
    try:
        observations = json.loads(response.output_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model did not return valid JSON for {photo.source}") from exc
    if not isinstance(observations, list):
        raise ValueError(f"Model did not return an array for {photo.source}")
    return [Finding(
        category=str(item.get("category", "other")), severity=str(item.get("severity", "low")),
        description=str(item.get("description", "")), location=str(item.get("location", "not specified")),
        confidence=str(item.get("confidence", "low")), photo_source=photo.source,
        evidence_filename=photo.evidence_filename,
    ) for item in observations if isinstance(item, dict) and item.get("description")]
