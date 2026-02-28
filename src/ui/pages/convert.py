"""
Forge — Convert Page
Core page: file queue + encode settings + progress footer.

Layout:
  ┌──────────────────────────────────────────────┐
  │  FileQueuePanel (left)  │  DetailPanel (right)│
  │                         │                     │
  ├─────────────────────────────────────────────-─┤
  │         ProgressFooter (full width)           │
  └──────────────────────────────────────────────┘
"""

import customtkinter as ctk
from src.ui.pages.base  import BasePage
from src.utils import theme as T
from src.core.queue_manager import QueueManager
from src.ui.widgets.file_queue_panel import FileQueuePanel
from src.ui.widgets.detail_panel     import DetailPanel
from src.ui.widgets.progress_footer  import ProgressFooter


class ConvertPage(BasePage):

    def build(self):
        # Shared queue state
        self._queue = QueueManager()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ── File queue (left) ─────────────────────────────────────────────────
        self._file_panel = FileQueuePanel(self, self._queue)
        self._file_panel.grid(row=0, column=0, sticky="nsew")

        # Vertical divider
        ctk.CTkFrame(self, width=1, fg_color=T.BORDER2, corner_radius=0).grid(
            row=0, column=0, sticky="nse"
        )

        # ── Detail panel (right) ──────────────────────────────────────────────
        self._detail_panel = DetailPanel(self, self._queue)
        self._detail_panel.grid(row=0, column=1, sticky="nsew")

        # ── Progress footer (bottom, full width) ──────────────────────────────
        self._footer = ProgressFooter(self, self._queue)
        self._footer.grid(row=1, column=0, columnspan=2, sticky="ew")

    def get_topbar(self):
        # Right-side topbar buttons — built after build() so queue exists
        add_btn = ctk.CTkButton(
            self._topbar,
            text="＋  Add Files",
            width=100, height=30,
            fg_color=T.SURFACE, hover_color=T.SURFACE2,
            text_color=T.TEXT2, corner_radius=T.RADIUS_SM,
            border_color=T.BORDER, border_width=1,
            font=ctk.CTkFont(size=12),
            command=self._file_panel._pick_files,
        )
        start_btn = ctk.CTkButton(
            self._topbar,
            text="▶  Start Queue",
            width=110, height=30,
            fg_color=T.ACCENT, hover_color=T.ACCENT_H,
            text_color="#FFFFFF", corner_radius=T.RADIUS_SM,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._start_queue,
        )
        return ("Convert", "— batch re-encode media files", [add_btn, start_btn])

    def _start_queue(self):
        # Encode engine will be wired in here later
        pass
