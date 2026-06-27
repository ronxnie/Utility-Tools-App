import shutil
import uuid
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def new_job_dir(kind: str) -> tuple[str, Path, Path]:
    job_id = uuid.uuid4().hex
    upload_dir = current_app.config["UPLOAD_FOLDER"] / kind / job_id
    output_dir = current_app.config["OUTPUT_FOLDER"] / kind / job_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    return job_id, upload_dir, output_dir


def save_uploads(files: list[FileStorage], target_dir: Path) -> list[Path]:
    saved = []
    for item in files:
        if not item or not item.filename:
            continue
        filename = secure_filename(item.filename)
        path = target_dir / filename
        item.save(path)
        saved.append(path)
    return saved


def zip_directory(source_dir: Path, zip_path: Path) -> Path:
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
        for file_path in source_dir.rglob("*"):
            if file_path.is_file() and file_path != zip_path:
                archive.write(file_path, file_path.relative_to(source_dir))
    return zip_path


def clean_old_jobs(root: Path, keep_latest: int = 60) -> None:
    jobs = sorted([p for p in root.glob("*/*") if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
    for old_job in jobs[keep_latest:]:
        shutil.rmtree(old_job, ignore_errors=True)
