from pathlib import Path

from PIL import Image, ImageOps


def _open_image(path: Path) -> Image.Image:
    image = Image.open(path)
    return ImageOps.exif_transpose(image)


def compress_image(input_path: Path, output_path: Path, quality: int = 70) -> Path:
    image = _open_image(input_path)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.save(output_path, optimize=True, quality=max(1, min(95, quality)))
    return output_path


def resize_image(input_path: Path, output_path: Path, width: int, height: int) -> Path:
    image = _open_image(input_path)
    resized = image.resize((width, height), Image.LANCZOS)
    if output_path.suffix.lower() in [".jpg", ".jpeg"] and resized.mode in ("RGBA", "P"):
        resized = resized.convert("RGB")
    resized.save(output_path, optimize=True)
    return output_path


def convert_png_jpg(input_path: Path, output_path: Path) -> Path:
    image = _open_image(input_path)
    if output_path.suffix.lower() in [".jpg", ".jpeg"] and image.mode in ("RGBA", "P"):
        background = Image.new("RGB", image.size, (255, 255, 255))
        if image.mode == "RGBA":
            background.paste(image, mask=image.getchannel("A"))
        else:
            background.paste(image.convert("RGB"))
        image = background
    image.save(output_path, optimize=True)
    return output_path
