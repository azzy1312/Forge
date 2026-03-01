"""
VMC — Convert Page
Queue is injected from the app shell so the shell-level ProgressFooter
shares the same state. This page no longer owns its own footer.
"""

import customtkinter as ctk
from src.ui.pages.base import BasePage
from src.utils import theme as T
from src.core.queue_manager import QueueManager
from src.ui.widgets.file_queue_panel import FileQueuePanel
from src.ui.widgets.detail_panel     import DetailPanel


class ConvertPage(BasePage):

    def __init__(self, master, topbar, queue: QueueManager, **kwargs):
        super().__init__(master, topbar, **kwargs)
        self._queue = queue   # injected — shared with shell footer

    def build(self):
        # Row 0 = full content (no footer row needed — footer is in app shell)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)   # file queue fixed
        self.grid_columnconfigure(1, weight=1)   # detail panel expands

        # ── Left: file queue panel ────────────────────────────────────────────
        self._file_panel = FileQueuePanel(self, self._queue)
        self._file_panel.grid(row=0, column=0, sticky="nsew")

        # Vertical divider between queue and detail panel
        ctk.CTkFrame(self, width=1, fg_color=T.BORDER2, corner_radius=0).grid(
            row=0, column=0, sticky="nse"
        )

        # ── Right: detail panel ───────────────────────────────────────────────
        self._detail_panel = DetailPanel(self, self._queue)
        self._detail_panel.grid(row=0, column=1, sticky="nsew")

        # ── Topbar buttons — created once, reused on every navigation ─────────
        self._add_btn = ctk.CTkButton(
            self._topbar.btn_container,
            text="＋  Add Files",
            width=100, height=30,
            fg_color=T.SURFACE, hover_color=T.SURFACE2,
            text_color=T.TEXT2, corner_radius=T.RADIUS_SM,
            border_color=T.BORDER, border_width=1,
            font=ctk.CTkFont(size=12),
            command=self._file_panel._pick_files,
        )
        self._start_btn = ctk.CTkButton(
            self._topbar.btn_container,
            text="▶  Start Queue",
            width=115, height=30,
            fg_color=T.ACCENT, hover_color=T.ACCENT_H,
            text_color="#FFFFFF", corner_radius=T.RADIUS_SM,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._start_queue,
        )

    def get_topbar(self):
        return ("Convert", "— batch re-encode media files",
                [self._add_btn, self._start_btn])

    def _start_queue(self):
        pass
