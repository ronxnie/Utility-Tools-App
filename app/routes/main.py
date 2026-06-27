from flask import Blueprint, render_template

from app.services.catalog import TOOL_CATEGORIES

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template("index.html", categories=TOOL_CATEGORIES)
