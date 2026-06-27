from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for

from app.services.file_store import new_job_dir, save_uploads
from app.services.pdf_tools import compress_pdf, merge_pdfs, pdf_to_images, split_pdf

pdf_bp = Blueprint("pdf", __name__)


@pdf_bp.route("/merge", methods=["GET", "POST"])
def merge():
    if request.method == "POST":
        _, upload_dir, output_dir = new_job_dir("pdf-merge")
        files = save_uploads(request.files.getlist("files"), upload_dir)
        if len(files) < 2:
            flash("Upload at least two PDF files to merge.", "error")
            return redirect(url_for("pdf.merge"))
        output = merge_pdfs(files, output_dir / "merged.pdf")
        flash("Your merged PDF is ready.", "success")
        return send_file(output, as_attachment=True, download_name="merged.pdf")
    return render_template("tools/file_tool.html", title="PDF Merge", accept=".pdf", multiple=True, fields=[], button="Merge PDFs")


@pdf_bp.route("/split", methods=["GET", "POST"])
def split():
    if request.method == "POST":
        _, upload_dir, output_dir = new_job_dir("pdf-split")
        files = save_uploads(request.files.getlist("files"), upload_dir)
        if not files:
            flash("Upload one PDF file to split.", "error")
            return redirect(url_for("pdf.split"))
        output = split_pdf(files[0], output_dir)
        flash("PDF pages were split into a ZIP file.", "success")
        return send_file(output, as_attachment=True, download_name="split-pages.zip")
    return render_template("tools/file_tool.html", title="PDF Split", accept=".pdf", multiple=False, fields=[], button="Split PDF")


@pdf_bp.route("/compress", methods=["GET", "POST"])
def compress():
    if request.method == "POST":
        _, upload_dir, output_dir = new_job_dir("pdf-compress")
        files = save_uploads(request.files.getlist("files"), upload_dir)
        if not files:
            flash("Upload one PDF file to compress.", "error")
            return redirect(url_for("pdf.compress"))
        output = compress_pdf(files[0], output_dir / "compressed.pdf")
        flash("PDF compression finished.", "success")
        return send_file(output, as_attachment=True, download_name="compressed.pdf")
    return render_template("tools/file_tool.html", title="PDF Compress", accept=".pdf", multiple=False, fields=[], button="Compress PDF")


@pdf_bp.route("/to-jpg", methods=["GET", "POST"])
def to_jpg():
    if request.method == "POST":
        _, upload_dir, output_dir = new_job_dir("pdf-images")
        files = save_uploads(request.files.getlist("files"), upload_dir)
        dpi = int(request.form.get("dpi", 150))
        if not files:
            flash("Upload one PDF file to convert.", "error")
            return redirect(url_for("pdf.to_jpg"))
        output = pdf_to_images(files[0], output_dir, dpi=dpi, image_format="jpg")
        flash("PDF pages were exported as JPG images.", "success")
        return send_file(output, as_attachment=True, download_name="pdf-jpg.zip")
    fields = [{"type": "number", "name": "dpi", "label": "Image DPI", "value": 150, "min": 72, "max": 300}]
    return render_template("tools/file_tool.html", title="PDF to JPG", accept=".pdf", multiple=False, fields=fields, button="Export JPG")


@pdf_bp.route("/to-images", methods=["GET", "POST"])
def to_images():
    return to_jpg()
