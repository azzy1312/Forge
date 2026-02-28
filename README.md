# Forge

A self-contained desktop media conversion and re-encoding tool built on HandBrakeCLI and FFprobe.

## Features
- Select individual files or entire folder trees (recursive)
- Supports MP4, MKV, AVI, MOV, WebM, and more
- Full media inspection: audio tracks, subtitle tracks, languages, resolution, framerate, bitrate, codec info
- Add/remove audio and subtitle tracks independently
- Edit metadata
- Batch convert with custom output naming patterns
- Configurable encoding presets
- Double-click to run (bundled with PyInstaller)

## Requirements
- [HandBrakeCLI](https://handbrake.fr/downloads2.php)
- [FFmpeg / FFprobe](https://ffmpeg.org/download.html)

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Build Standalone App

```bash
pyinstaller forge.spec
```
