import base64
import json
import re
import uuid


def word_stats(text: str) -> dict:
    words = re.findall(r"\b[\w'-]+\b", text)
    sentences = re.findall(r"[^.!?]+[.!?]?", text.strip()) if text.strip() else []
    return {
        "characters": len(text),
        "characters_no_spaces": len(text.replace(" ", "")),
        "words": len(words),
        "sentences": len([s for s in sentences if s.strip()]),
        "paragraphs": len([p for p in text.splitlines() if p.strip()]),
        "reading_minutes": max(1, round(len(words) / 220, 1)) if words else 0,
    }


def convert_case(text: str, mode: str) -> str:
    conversions = {
        "upper": text.upper,
        "lower": text.lower,
        "title": text.title,
        "sentence": lambda: re.sub(r"(^\s*\w|[.!?]\s+\w)", lambda m: m.group(0).upper(), text.lower()),
    }
    return conversions.get(mode, text.title)()


def format_json(raw: str, indent: int = 2) -> str:
    return json.dumps(json.loads(raw), indent=indent, ensure_ascii=False)


def base64_transform(raw: str, mode: str) -> str:
    if mode == "decode":
        return base64.b64decode(raw.encode("utf-8")).decode("utf-8")
    return base64.b64encode(raw.encode("utf-8")).decode("utf-8")


def generate_uuid(version: str = "4") -> str:
    if version == "1":
        return str(uuid.uuid1())
    return str(uuid.uuid4())
