# Forge

A self-contained video transcoding GUI application built on HandBrakeCLI and ffprobe.

## Features
- Select individual files, folders, or nested folder trees (MP4, MKV, MOV, AVI, and more)
- Inspect full metadata per file — streams, languages, codecs, resolution, framerate, bitrate
- Add/remove audio and subtitle tracks independently
- Full encoding settings — codec, preset, quality (CRF), resolution, framerate, bitrate
- Output filename templating (e.g. `{name}.720p.x265.mkv`)
- Queue-based batch conversion with per-file progress
- Double-click to run — no terminal needed

## Requirements
- macOS (primary target)
- [HandBrakeCLI](https://handbrake.fr/downloads2.php) installed
- [ffprobe](https://ffmpeg.org/download.html) installed (part of ffmpeg)
- Python 3.11+

## Setup (dev)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Build (standalone .app)

```bash
pip install pyinstaller
pyinstaller forge.spec
```

## Project Structure

```
Forge/
├── main.py              # Entry point
├── requirements.txt
├── forge.spec           # PyInstaller spec (to be created at build time)
├── assets/              # Icons, images
└── src/
    ├── ui/              # All UI components and windows
    ├── core/            # Transcoding engine, queue, HandBrakeCLI wrapper
    └── utils/           # ffprobe metadata, file tree walker, helpers
```
