from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter

from .file_store import zip_directory


def merge_pdfs(inputs: list[Path], output_path: Path) -> Path:
    writer = PdfWriter()
    for pdf in inputs:
        reader = PdfReader(str(pdf))
        for page in reader.pages:
            writer.add_page(page)
    with output_path.open("wb") as handle:
        writer.write(handle)
    return output_path


def split_pdf(input_pdf: Path, output_dir: Path) -> Path:
    reader = PdfReader(str(input_pdf))
    for index, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        with (output_dir / f"page-{index:03}.pdf").open("wb") as handle:
            writer.write(handle)
    return zip_directory(output_dir, output_dir / "split-pages.zip")


def compress_pdf(input_pdf: Path, output_path: Path) -> Path:
    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()
    for page in reader.pages:
        # remove duplicated object references and unused metadata while preserving page content
        page.compress_content_streams()
        writer.add_page(page)
    writer.add_metadata({})
    with output_path.open("wb") as handle:
        writer.write(handle)
    return output_path


def pdf_to_images(input_pdf: Path, output_dir: Path, dpi: int = 150, image_format: str = "jpg") -> Path:
    document = fitz.open(input_pdf)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    extension = "jpg" if image_format.lower() in {"jpg", "jpeg"} else "png"
    for index, page in enumerate(document, start=1):
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)
        pixmap.save(output_dir / f"page-{index:03}.{extension}")
    document.close()
    return zip_directory(output_dir, output_dir / "pdf-images.zip")
