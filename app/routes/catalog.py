import calendar
import difflib
import html
import math
import random
import re
import secrets
import string
from datetime import datetime, timedelta
from xml.dom import minidom

from flask import Blueprint, abort, render_template, request

from app.services.catalog import TOOL_INDEX
from app.services.text_tools import word_stats

catalog_bp = Blueprint("catalog", __name__)


def _safe_math(expression: str) -> str:
    allowed = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
    allowed.update({"abs": abs, "round": round, "pow": pow})
    if not re.fullmatch(r"[\d\s+\-*/().,%a-zA-Z_]+", expression):
        raise ValueError("Unsupported characters in expression.")
    return str(eval(expression.replace("%", "/100"), {"__builtins__": {}}, allowed))


def _password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(max(8, min(length, 64))))


def _password_score(value: str) -> dict:
    score = sum([
        len(value) >= 12,
        bool(re.search(r"[a-z]", value)),
        bool(re.search(r"[A-Z]", value)),
        bool(re.search(r"\d", value)),
        bool(re.search(r"[^A-Za-z0-9]", value)),
    ])
    labels = ["Very weak", "Weak", "Fair", "Good", "Strong", "Excellent"]
    return {"score": score, "label": labels[score], "percent": score * 20}


def _roadmap_result(tool_def: dict) -> dict:
    category = tool_def.get("category", "this category")
    name = tool_def["name"]
    integrations = {
        "YouTube to MP3": "Connect a guarded downloader worker plus FFmpeg audio extraction, with platform terms, copyright checks, rate limits, and job timeouts enforced.",
        "YouTube Thumbnail Downloader": "Parse the video ID, validate the URL, and fetch public thumbnail variants through a guarded request layer.",
        "Instagram DP Viewer": "Use an approved social-media integration or compliant metadata provider before exposing profile assets.",
        "Instagram Story Downloader": "Use a compliant downloader worker with authentication boundaries, platform terms, and rate limits enforced.",
        "Video to MP3": "Connect FFmpeg to extract audio tracks and return MP3 downloads from uploaded videos.",
        "Video Compressor": "Connect FFmpeg presets for browser, mobile, and high-quality compression profiles.",
        "Audio Cutter": "Connect FFmpeg trimming with start/end timestamps and audio preview support.",
        "Video Cutter": "Connect FFmpeg trimming with start/end timestamps and safe output limits.",
    }
    next_step = integrations.get(
        name,
        "Connect the service engine for this workflow, then return the generated file or result from this page.",
    )
    return {
        "output": (
            f"{name} is listed under {category} and this page is ready for backend integration.\n\n"
            f"Next step: {next_step}"
        )
    }


def _handle_tool(tool_def: dict, form) -> dict:
    kind = tool_def.get("kind", "planned")
    text = form.get("text", "")
    if kind == "text-analyzer":
        return {"stats": word_stats(text)}
    if kind == "summarizer":
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return {"output": " ".join(sentences[:3])}
    if kind == "lorem":
        count = int(form.get("count", 3))
        paragraph = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae justo non nibh pulvinar posuere."
        return {"output": "\n\n".join([paragraph] * max(1, min(count, 20)))}
    if kind == "xml":
        if not text.strip():
            return {"output": "Paste XML input, then run the formatter."}
        return {"output": minidom.parseString(text).toprettyxml(indent="  ")}
    if kind == "regex":
        pattern = form.get("pattern", "")
        if not pattern:
            return {"output": "Enter a regex pattern and input text to see matches."}
        return {"matches": re.findall(pattern, text)}
    if kind == "minifier":
        return {"output": re.sub(r"\s+", " ", text).strip()}
    if kind == "diff":
        left = form.get("left", "").splitlines()
        right = form.get("right", "").splitlines()
        return {"output": "\n".join(difflib.unified_diff(left, right, fromfile="Original", tofile="Changed", lineterm=""))}
    if kind == "color-converter":
        raw = form.get("color", "").strip()
        if not raw:
            return {"output": "Enter a HEX value like #00A7B5 or RGB value like 0, 167, 181."}
        if raw.startswith("#") and len(raw) == 7:
            rgb = tuple(int(raw[i:i + 2], 16) for i in (1, 3, 5))
            return {"output": f"RGB: {rgb[0]}, {rgb[1]}, {rgb[2]}"}
        values = [int(v) for v in re.findall(r"\d+", raw)[:3]]
        if len(values) < 3:
            return {"output": "Enter three RGB numbers, for example 0, 167, 181."}
        return {"output": "#{:02X}{:02X}{:02X}".format(*values)}
    if kind == "calculator":
        return {"output": _safe_math(form.get("expression", "0"))}
    if kind == "sip":
        monthly = float(form.get("monthly", 5000))
        rate = float(form.get("rate", 12)) / 100 / 12
        months = int(form.get("months", 120))
        value = monthly * (((1 + rate) ** months - 1) / rate) * (1 + rate) if rate else monthly * months
        return {"output": f"Future value: {value:,.2f}"}
    if kind == "gst":
        amount = float(form.get("amount", 1000))
        rate = float(form.get("rate", 18))
        gst = amount * rate / 100
        return {"output": f"GST: {gst:,.2f} | Total: {amount + gst:,.2f}"}
    if kind == "fd":
        principal = float(form.get("principal", 100000))
        rate = float(form.get("rate", 7)) / 100
        years = float(form.get("years", 5))
        maturity = principal * ((1 + rate) ** years)
        return {"output": f"Maturity amount: {maturity:,.2f} | Interest: {maturity - principal:,.2f}"}
    if kind == "percentage":
        part = float(form.get("part", 25))
        whole = float(form.get("whole", 200))
        return {"output": f"{part} is {(part / whole) * 100:.2f}% of {whole}"}
    if kind == "unit":
        value = float(form.get("value", 1))
        mode = form.get("mode", "km-mi")
        factors = {"km-mi": 0.621371, "mi-km": 1.60934, "kg-lb": 2.20462, "lb-kg": 0.453592}
        return {"output": f"{value * factors[mode]:,.4f}"}
    if kind == "date":
        start_value = form.get("start")
        if not start_value:
            return {"output": "Choose a start date and enter how many days to add."}
        start = datetime.strptime(start_value, "%Y-%m-%d")
        days = int(form.get("days", 0))
        return {"output": (start + timedelta(days=days)).strftime("%Y-%m-%d")}
    if kind == "password":
        return {"output": _password(int(form.get("length", 16)))}
    if kind == "password-strength":
        return {"strength": _password_score(form.get("password", ""))}
    if kind == "hashtags":
        topic = form.get("topic", "productivity")
        tags = [f"#{re.sub(r'[^A-Za-z0-9]', '', item).lower()}" for item in topic.split()]
        tags += [f"#{topic.replace(' ', '').lower()}", "#viral", "#creator", "#dailytools"]
        return {"output": " ".join(dict.fromkeys(tags))}
    if kind == "captions":
        topic = form.get("topic", "new post")
        return {"output": f"{topic.title()} made simple. Save this, share it, and try it today."}
    if kind == "youtube-thumb":
        video_id = form.get("video_id", "").strip().split("v=")[-1].split("&")[0].split("/")[-1]
        return {"output": f"https://img.youtube.com/vi/{html.escape(video_id)}/maxresdefault.jpg"}
    if kind == "color":
        return {"output": form.get("color", "#00A7B5")}
    if kind == "qr":
        data = form.get("data", "https://example.com")
        return {"output": f"QR payload saved for generation: {data}"}
    if kind == "productivity":
        return {"output": "This productivity tool runs in your browser with local storage friendly UI controls."}
    return _roadmap_result(tool_def)


@catalog_bp.route("/tools/<slug>", methods=["GET", "POST"])
def tool(slug):
    tool_def = TOOL_INDEX.get(slug)
    if not tool_def:
        abort(404)

    result = None
    error = None
    if request.method == "POST":
        try:
            result = _handle_tool(tool_def, request.form)
        except Exception as exc:
            error = str(exc)

    return render_template(
        "tools/generic_tool.html",
        title=tool_def["name"],
        tool=tool_def,
        result=result,
        error=error,
        months=list(calendar.month_name)[1:],
    )
