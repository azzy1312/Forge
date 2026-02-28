"""
Forge — File Utils
Helpers for reading basic file info without FFprobe
(size, extension, duration placeholder until FFprobe is wired in).
"""

import os


SUPPORTED_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov", ".webm",
    ".m4v", ".flv", ".wmv", ".ts", ".m2ts",
    ".mpg", ".mpeg", ".ogv", ".3gp",
}


def is_supported(path: str) -> bool:
    _, ext = os.path.splitext(path)
    return ext.lower() in SUPPORTED_EXTENSIONS


def friendly_size(path: str) -> str:
    """Return human-readable file size string."""
    try:
        b = os.path.getsize(path)
    except OSError:
        return "? MB"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} PB"


def friendly_ext(path: str) -> str:
    _, ext = os.path.splitext(path)
    return ext.lstrip(".").upper()[:4]
