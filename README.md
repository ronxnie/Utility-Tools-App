# Utility Tools Hub

A production-ready Flask multipage web application for everyday PDF, image, text, developer, and calculator utilities. It uses local processing only, so uploaded files remain on the server running the app.

## Tool Catalog

The dashboard now includes all requested high-search utility groups and routes every option to either a working local tool or a dedicated integration-ready page.

### PDF & Document Tools

- PDF Merge
- PDF Split
- PDF Compress
- PDF to Word
- Word to PDF
- PDF to JPG
- JPG to PDF
- PDF to Excel
- PDF Unlock
- PDF Protect
- PDF Rotate
- OCR (Image to Text)
- PDF Page Delete / Reorder

### Image & Media Tools

- Image Compressor
- Image Resizer
- Image Cropper
- Background Remover
- PNG ↔ JPG Converter
- WebP Converter
- Video to MP3
- Video Compressor
- GIF Maker
- Color Picker
- Image Upscaler

### Text & Writing Tools

- Word Counter
- Character Counter
- Case Converter
- Plagiarism Checker
- Grammar Checker
- Text Summarizer
- Paraphraser
- Lorem Ipsum Generator

### Developer Tools

- JSON Formatter
- XML Formatter
- Base64 Encoder/Decoder
- UUID Generator
- Regex Tester
- QR Code Generator
- Barcode Generator
- HTML/CSS/JS Minifier
- Diff Checker (Compare Text)
- Color Code Converter (HEX ↔ RGB)

### Calculators & Finance Tools

- Scientific Calculator
- EMI Calculator
- SIP Calculator
- GST Calculator
- FD Calculator
- Age Calculator
- Percentage Calculator
- Unit Converter
- Currency Converter
- Date Calculator

### File Tools

- ZIP / Unzip
- RAR Extractor
- File Converter (Any format)
- Audio Cutter
- Video Cutter
- Metadata Viewer (EXIF)

### Social Media Tools

- YouTube Thumbnail Downloader
- YouTube to MP3
- Instagram DP Viewer
- Instagram Story Downloader
- Hashtag Generator
- Caption Generator

### AI Utility Tools

- AI Background Remover
- AI Image Generator
- AI Upscaler
- AI Text Summarizer
- AI Paraphraser
- AI Resume Analyzer
- AI Voice Generator

### Security & Privacy Tools

- Password Generator
- Password Strength Checker
- IP Lookup
- Temp Mail
- Email Spam Checker
- Website Safety Checker

### Daily Productivity Tools

- To-Do List
- Pomodoro Timer
- Stopwatch
- Notepad Online
- Habit Tracker
- Calendar Generator
- Mind Map Creator

The original MVP file-processing tools remain fully implemented. Many newly added no-dependency tools are interactive immediately, including XML formatter, regex tester, diff checker, color converter, scientific/SIP/GST/FD/percentage/unit/date calculators, password tools, hashtags, captions, and YouTube thumbnail URL generation. Heavy tools that require external engines or AI providers have dedicated pages ready for service integration.

## Folder Structure

```text
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── routes/
│   │   ├── main.py
│   │   ├── pdf.py
│   │   ├── image.py
│   │   ├── text.py
│   │   ├── dev.py
│   │   └── calc.py
│   ├── services/
│   │   ├── file_store.py
│   │   ├── pdf_tools.py
│   │   ├── image_tools.py
│   │   ├── text_tools.py
│   │   └── calculators.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── input.css
│   │   │   └── theme.css
│   │   └── js/app.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── tools/
├── docker-compose.yml
├── Dockerfile
├── package.json
├── requirements.txt
├── tailwind.config.js
└── run.py
```

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open `http://localhost:5000`.

## Docker

Run the full app:

```bash
docker compose up --build
```

Run category-focused service containers from the same image:

```bash
docker compose --profile microservices up --build
```

The default web service is exposed on `http://localhost:5000`. The profile services demonstrate a microservice-ready layout using the same codebase and shared processing volume.

## Tailwind

The app uses Tailwind through the CDN for immediate startup and includes a Tailwind build pipeline for production hardening:

```bash
npm install
npm run build:css
```

You can then switch templates from the CDN script to the generated `app/static/css/tailwind.css`.

## MySQL Note

No database is required for the MVP because every tool processes stateless requests and returns downloads immediately. MySQL Server 8.x can be added later for user accounts, job history, audit logs, usage limits, subscriptions, or saved files.

## Adding More Tools

1. Add reusable logic under `app/services/`.
2. Add a route to the matching blueprint in `app/routes/`, or create a new blueprint.
3. Add a template under `app/templates/tools/`.
4. Register the tool in `app/services/catalog.py`.
5. Add Docker environment variables if the tool needs service-specific configuration.

Keep long-running or CPU-heavy tools behind a queue such as Celery/RQ when usage grows. The current structure is ready for that because web routes already delegate processing to service modules.

For the heavier catalog tools, recommended service engines are:

- LibreOffice or Pandoc for Word/PDF conversion.
- Tesseract OCR for image-to-text.
- FFmpeg for video/audio conversion, compression, and cutting.
- unrar/7zip for RAR extraction.
- A vetted AI provider or local model server for AI generation, summarization, paraphrasing, resume analysis, and voice.
- A guarded downloader worker for social-media media extraction, with platform terms and rate limits enforced.
