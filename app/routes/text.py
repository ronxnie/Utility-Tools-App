from flask import Blueprint, render_template, request

from app.services.text_tools import convert_case, word_stats

text_bp = Blueprint("text", __name__)


@text_bp.route("/word-counter", methods=["GET", "POST"])
def word_counter():
    text = request.form.get("text", "")
    result = word_stats(text) if request.method == "POST" else None
    return render_template("tools/word_counter.html", title="Word Counter", text=text, result=result)


@text_bp.route("/case-converter", methods=["GET", "POST"])
def case_converter():
    text = request.form.get("text", "")
    mode = request.form.get("mode", "title")
    result = convert_case(text, mode) if request.method == "POST" else ""
    return render_template("tools/case_converter.html", title="Case Converter", text=text, mode=mode, result=result)
