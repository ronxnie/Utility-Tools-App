def existing(endpoint: str) -> dict:
    return {"endpoint": endpoint, "implemented": True}


def planned(slug: str, kind: str = "planned") -> dict:
    return {"slug": slug, "kind": kind, "implemented": kind != "planned"}


TOOL_CATEGORIES = [
    {
        "name": "PDF & Document Tools",
        "slug": "pdf",
        "accent": "from-coral to-aqua",
        "description": "High-demand document workflows for PDF conversion, editing, protection, and extraction.",
        "tools": [
            {"name": "PDF Merge", **existing("pdf.merge")},
            {"name": "PDF Split", **existing("pdf.split")},
            {"name": "PDF Compress", **existing("pdf.compress")},
            {"name": "PDF to Word", **planned("pdf-to-word")},
            {"name": "Word to PDF", **planned("word-to-pdf")},
            {"name": "PDF to JPG", **existing("pdf.to_jpg")},
            {"name": "JPG to PDF", **planned("jpg-to-pdf")},
            {"name": "PDF to Excel", **planned("pdf-to-excel")},
            {"name": "PDF Unlock", **planned("pdf-unlock")},
            {"name": "PDF Protect", **planned("pdf-protect")},
            {"name": "PDF Rotate", **planned("pdf-rotate")},
            {"name": "OCR (Image to Text)", **planned("ocr-image-to-text")},
            {"name": "PDF Page Delete / Reorder", **planned("pdf-page-delete-reorder")},
        ],
    },
    {
        "name": "Image & Media Tools",
        "slug": "image",
        "accent": "from-aqua to-limepop",
        "description": "Creator-friendly image and media utilities for quick optimization and conversion.",
        "tools": [
            {"name": "Image Compressor", **existing("image.compress")},
            {"name": "Image Resizer", **existing("image.resize")},
            {"name": "Image Cropper", **planned("image-cropper")},
            {"name": "Background Remover", **planned("background-remover")},
            {"name": "PNG ↔ JPG Converter", **existing("image.convert")},
            {"name": "WebP Converter", **planned("webp-converter")},
            {"name": "Video to MP3", **planned("video-to-mp3")},
            {"name": "Video Compressor", **planned("video-compressor")},
            {"name": "GIF Maker", **planned("gif-maker")},
            {"name": "Color Picker", **planned("color-picker", "color")},
            {"name": "Image Upscaler", **planned("image-upscaler")},
        ],
    },
    {
        "name": "Text & Writing Tools",
        "slug": "text",
        "accent": "from-limepop to-coral",
        "description": "Writing, counting, rewriting, and content-preparation tools.",
        "tools": [
            {"name": "Word Counter", **existing("text.word_counter")},
            {"name": "Character Counter", **planned("character-counter", "text-analyzer")},
            {"name": "Case Converter", **existing("text.case_converter")},
            {"name": "Plagiarism Checker", **planned("plagiarism-checker")},
            {"name": "Grammar Checker", **planned("grammar-checker")},
            {"name": "Text Summarizer", **planned("text-summarizer", "summarizer")},
            {"name": "Paraphraser", **planned("paraphraser")},
            {"name": "Lorem Ipsum Generator", **planned("lorem-ipsum-generator", "lorem")},
        ],
    },
    {
        "name": "Developer Tools",
        "slug": "dev",
        "accent": "from-ink to-aqua",
        "description": "Daily programmer helpers for formatting, encoding, testing, comparing, and color work.",
        "tools": [
            {"name": "JSON Formatter", **existing("dev.json_formatter")},
            {"name": "XML Formatter", **planned("xml-formatter", "xml")},
            {"name": "Base64 Encoder/Decoder", **existing("dev.base64_tool")},
            {"name": "UUID Generator", **existing("dev.uuid_generator")},
            {"name": "Regex Tester", **planned("regex-tester", "regex")},
            {"name": "QR Code Generator", **planned("qr-code-generator", "qr")},
            {"name": "Barcode Generator", **planned("barcode-generator")},
            {"name": "HTML/CSS/JS Minifier", **planned("html-css-js-minifier", "minifier")},
            {"name": "Diff Checker (Compare Text)", **planned("diff-checker", "diff")},
            {"name": "Color Code Converter (HEX ↔ RGB)", **planned("color-code-converter", "color-converter")},
        ],
    },
    {
        "name": "Calculators & Finance Tools",
        "slug": "calculators",
        "accent": "from-coral to-limepop",
        "description": "India-friendly and global calculators for money, dates, units, and daily math.",
        "tools": [
            {"name": "Scientific Calculator", **planned("scientific-calculator", "calculator")},
            {"name": "EMI Calculator", **existing("calc.emi")},
            {"name": "SIP Calculator", **planned("sip-calculator", "sip")},
            {"name": "GST Calculator", **planned("gst-calculator", "gst")},
            {"name": "FD Calculator", **planned("fd-calculator", "fd")},
            {"name": "Age Calculator", **existing("calc.age")},
            {"name": "Percentage Calculator", **planned("percentage-calculator", "percentage")},
            {"name": "Unit Converter", **planned("unit-converter", "unit")},
            {"name": "Currency Converter", **planned("currency-converter")},
            {"name": "Date Calculator", **planned("date-calculator", "date")},
        ],
    },
    {
        "name": "File Tools",
        "slug": "file",
        "accent": "from-aqua to-coral",
        "description": "No-login file utilities for archives, conversions, trimming, and metadata.",
        "tools": [
            {"name": "ZIP / Unzip", **planned("zip-unzip")},
            {"name": "RAR Extractor", **planned("rar-extractor")},
            {"name": "File Converter (Any format)", **planned("file-converter")},
            {"name": "Audio Cutter", **planned("audio-cutter")},
            {"name": "Video Cutter", **planned("video-cutter")},
            {"name": "Metadata Viewer (EXIF)", **planned("metadata-viewer-exif")},
        ],
    },
    {
        "name": "Social Media Tools",
        "slug": "social",
        "accent": "from-limepop to-aqua",
        "description": "Creator utilities for thumbnails, captions, hashtags, and profile assets.",
        "tools": [
            {"name": "YouTube Thumbnail Downloader", **planned("youtube-thumbnail-downloader", "youtube-thumb")},
            {"name": "YouTube to MP3", **planned("youtube-to-mp3")},
            {"name": "Instagram DP Viewer", **planned("instagram-dp-viewer")},
            {"name": "Instagram Story Downloader", **planned("instagram-story-downloader")},
            {"name": "Hashtag Generator", **planned("hashtag-generator", "hashtags")},
            {"name": "Caption Generator", **planned("caption-generator", "captions")},
        ],
    },
    {
        "name": "AI Utility Tools",
        "slug": "ai",
        "accent": "from-coral to-ink",
        "description": "AI-ready workflow pages for generation, rewriting, analysis, and voice tools.",
        "tools": [
            {"name": "AI Background Remover", **planned("ai-background-remover")},
            {"name": "AI Image Generator", **planned("ai-image-generator")},
            {"name": "AI Upscaler", **planned("ai-upscaler")},
            {"name": "AI Text Summarizer", **planned("ai-text-summarizer", "summarizer")},
            {"name": "AI Paraphraser", **planned("ai-paraphraser")},
            {"name": "AI Resume Analyzer", **planned("ai-resume-analyzer")},
            {"name": "AI Voice Generator", **planned("ai-voice-generator")},
        ],
    },
    {
        "name": "Security & Privacy Tools",
        "slug": "security",
        "accent": "from-ink to-coral",
        "description": "Quick privacy and safety helpers for passwords, email, IP, and sites.",
        "tools": [
            {"name": "Password Generator", **planned("password-generator", "password")},
            {"name": "Password Strength Checker", **planned("password-strength-checker", "password-strength")},
            {"name": "IP Lookup", **planned("ip-lookup")},
            {"name": "Temp Mail", **planned("temp-mail")},
            {"name": "Email Spam Checker", **planned("email-spam-checker")},
            {"name": "Website Safety Checker", **planned("website-safety-checker")},
        ],
    },
    {
        "name": "Daily Productivity Tools",
        "slug": "productivity",
        "accent": "from-aqua to-ink",
        "description": "Browser-based productivity tools that help users plan, focus, and capture ideas.",
        "tools": [
            {"name": "To-Do List", **planned("todo-list", "productivity")},
            {"name": "Pomodoro Timer", **planned("pomodoro-timer", "productivity")},
            {"name": "Stopwatch", **planned("stopwatch", "productivity")},
            {"name": "Notepad Online", **planned("notepad-online", "productivity")},
            {"name": "Habit Tracker", **planned("habit-tracker", "productivity")},
            {"name": "Calendar Generator", **planned("calendar-generator", "productivity")},
            {"name": "Mind Map Creator", **planned("mind-map-creator", "productivity")},
        ],
    },
]


TOOL_INDEX = {
    tool["slug"]: {**tool, "category": category["name"]}
    for category in TOOL_CATEGORIES
    for tool in category["tools"]
    if "slug" in tool
}
