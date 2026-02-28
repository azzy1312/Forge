"""
Forge — Queue Manager
Holds the list of queued files and their encode state.
UI components observe this; encode workers will read from it.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable


class FileStatus(Enum):
    READY    = auto()
    ENCODING = auto()
    DONE     = auto()
    ERROR    = auto()
    SKIPPED  = auto()


@dataclass
class QueueEntry:
    path:     str
    name:     str
    size_str: str       # e.g. "2.1 GB"
    duration: str       # e.g. "47m 12s"
    status:   FileStatus = FileStatus.READY
    progress: float      = 0.0          # 0.0 – 1.0
    error_msg: str       = ""
    media_info: dict     = field(default_factory=dict)


class QueueManager:
    """
    Central state for the file queue.
    Observers (UI components) register via add_listener() and
    are called whenever the queue changes.
    """

    def __init__(self):
        self._entries:   list[QueueEntry] = []
        self._listeners: list[Callable]   = []
        self._selected:  int | None       = None

    # ── Listeners ─────────────────────────────────────────────────────────────

    def add_listener(self, fn: Callable):
        self._listeners.append(fn)

    def _notify(self):
        for fn in self._listeners:
            fn()

    # ── Queue operations ──────────────────────────────────────────────────────

    def add(self, entry: QueueEntry):
        # Avoid exact duplicates
        if any(e.path == entry.path for e in self._entries):
            return
        self._entries.append(entry)
        if self._selected is None:
            self._selected = 0
        self._notify()

    def remove(self, index: int):
        if 0 <= index < len(self._entries):
            self._entries.pop(index)
            # Clamp selection
            if self._entries:
                self._selected = min(self._selected or 0, len(self._entries) - 1)
            else:
                self._selected = None
            self._notify()

    def clear(self):
        self._entries.clear()
        self._selected = None
        self._notify()

    def clear_done(self):
        self._entries = [e for e in self._entries if e.status != FileStatus.DONE]
        self._selected = 0 if self._entries else None
        self._notify()

    # ── Selection ─────────────────────────────────────────────────────────────

    def select(self, index: int):
        if 0 <= index < len(self._entries):
            self._selected = index
            self._notify()

    @property
    def selected_index(self) -> int | None:
        return self._selected

    @property
    def selected(self) -> QueueEntry | None:
        if self._selected is not None and self._selected < len(self._entries):
            return self._entries[self._selected]
        return None

    # ── Accessors ─────────────────────────────────────────────────────────────

    @property
    def entries(self) -> list[QueueEntry]:
        return self._entries

    def __len__(self):
        return len(self._entries)

    def ready_count(self) -> int:
        return sum(1 for e in self._entries if e.status == FileStatus.READY)

    def done_count(self) -> int:
        return sum(1 for e in self._entries if e.status == FileStatus.DONE)
