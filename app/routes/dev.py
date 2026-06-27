from flask import Blueprint, flash, render_template, request

from app.services.text_tools import base64_transform, format_json, generate_uuid

dev_bp = Blueprint("dev", __name__)


@dev_bp.route("/json-formatter", methods=["GET", "POST"])
def json_formatter():
    raw = request.form.get("raw", "")
    result = ""
    if request.method == "POST":
        try:
            result = format_json(raw)
        except Exception as exc:
            flash(f"Invalid JSON: {exc}", "error")
    return render_template("tools/json_formatter.html", title="JSON Formatter", raw=raw, result=result)


@dev_bp.route("/base64", methods=["GET", "POST"])
def base64_tool():
    raw = request.form.get("raw", "")
    mode = request.form.get("mode", "encode")
    result = ""
    if request.method == "POST":
        try:
            result = base64_transform(raw, mode)
        except Exception as exc:
            flash(f"Base64 operation failed: {exc}", "error")
    return render_template("tools/base64.html", title="Base64 Encoder/Decoder", raw=raw, mode=mode, result=result)


@dev_bp.route("/uuid", methods=["GET", "POST"])
def uuid_generator():
    version = request.form.get("version", "4")
    count = min(int(request.form.get("count", 5)), 100)
    uuids = [generate_uuid(version) for _ in range(count)]
    return render_template("tools/uuid.html", title="UUID Generator", version=version, count=count, uuids=uuids)
