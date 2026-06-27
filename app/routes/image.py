from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for

from app.services.file_store import new_job_dir, save_uploads
from app.services.image_tools import compress_image, convert_png_jpg, resize_image

image_bp = Blueprint("image", __name__)


@image_bp.route("/compress", methods=["GET", "POST"])
def compress():
    if request.method == "POST":
        _, upload_dir, output_dir = new_job_dir("image-compress")
        files = save_uploads(request.files.getlist("files"), upload_dir)
        quality = int(request.form.get("quality", 70))
        if not files:
            flash("Upload an image to compress.", "error")
            return redirect(url_for("image.compress"))
        output = output_dir / f"compressed-{Path(files[0]).stem}.jpg"
        compress_image(files[0], output, quality)
        flash("Image compression finished.", "success")
        return send_file(output, as_attachment=True, download_name=output.name)
    fields = [{"type": "number", "name": "quality", "label": "Quality", "value": 70, "min": 1, "max": 95}]
    return render_template("tools/file_tool.html", title="Image Compressor", accept="image/*", multiple=False, fields=fields, button="Compress Image")


@image_bp.route("/resize", methods=["GET", "POST"])
def resize():
    if request.method == "POST":
        _, upload_dir, output_dir = new_job_dir("image-resize")
        files = save_uploads(request.files.getlist("files"), upload_dir)
        width = int(request.form.get("width", 800))
        height = int(request.form.get("height", 600))
        if not files:
            flash("Upload an image to resize.", "error")
            return redirect(url_for("image.resize"))
        suffix = Path(files[0]).suffix or ".jpg"
        output = output_dir / f"resized-{Path(files[0]).stem}{suffix}"
        resize_image(files[0], output, width, height)
        flash("Image resize finished.", "success")
        return send_file(output, as_attachment=True, download_name=output.name)
    fields = [
        {"type": "number", "name": "width", "label": "Width", "value": 800, "min": 1, "max": 8000},
        {"type": "number", "name": "height", "label": "Height", "value": 600, "min": 1, "max": 8000},
    ]
    return render_template("tools/file_tool.html", title="Image Resizer", accept="image/*", multiple=False, fields=fields, button="Resize Image")


@image_bp.route("/convert", methods=["GET", "POST"])
def convert():
    if request.method == "POST":
        _, upload_dir, output_dir = new_job_dir("image-convert")
        files = save_uploads(request.files.getlist("files"), upload_dir)
        target = request.form.get("target", "jpg")
        if not files:
            flash("Upload a PNG or JPG image to convert.", "error")
            return redirect(url_for("image.convert"))
        extension = ".png" if target == "png" else ".jpg"
        output = output_dir / f"converted-{Path(files[0]).stem}{extension}"
        convert_png_jpg(files[0], output)
        flash("Image conversion finished.", "success")
        return send_file(output, as_attachment=True, download_name=output.name)
    fields = [{"type": "select", "name": "target", "label": "Convert To", "options": [("jpg", "JPG"), ("png", "PNG")]}]
    return render_template("tools/file_tool.html", title="PNG/JPG Converter", accept=".png,.jpg,.jpeg", multiple=False, fields=fields, button="Convert Image")
