"""
Forge — Convert Page
Buttons are created ONCE in build() and stored.
get_topbar() just returns the cached references — never creates new widgets.
"""

import customtkinter as ctk
from src.ui.pages.base import BasePage
from src.utils import theme as T
from src.core.queue_manager import QueueManager
from src.ui.widgets.file_queue_panel import FileQueuePanel
from src.ui.widgets.detail_panel     import DetailPanel
from src.ui.widgets.progress_footer  import ProgressFooter


class ConvertPage(BasePage):

    def build(self):
        self._queue = QueueManager()

        # Row 0 = main content area, Row 1 = footer
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        # Col 0 = file queue (fixed), Col 1 = detail panel (expands)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # ── Left: file queue panel ─────────────────────────────────────────
        self._file_panel = FileQueuePanel(self, self._queue)
        self._file_panel.grid(row=0, column=0, sticky="nsew")

        # ── Vertical divider ───────────────────────────────────────────────
        ctk.CTkFrame(self, width=1, fg_color=T.BORDER2, corner_radius=0).grid(
            row=0, column=0, sticky="nse"
        )

        # ── Right: detail panel ────────────────────────────────────────────
        self._detail_panel = DetailPanel(self, self._queue)
        self._detail_panel.grid(row=0, column=1, sticky="nsew")

        # ── Bottom: progress footer ────────────────────────────────────────
        self._footer = ProgressFooter(self, self._queue)
        self._footer.grid(row=1, column=0, columnspan=2, sticky="ew")

        # ── Topbar buttons — created ONCE here, reused on every navigation ─
        self._add_btn = ctk.CTkButton(
            self,                          # parent doesn't matter — re-gridded by topbar
            text="＋  Add Files",
            width=100, height=30,
            fg_color=T.SURFACE,
            hover_color=T.SURFACE2,
            text_color=T.TEXT2,
            corner_radius=T.RADIUS_SM,
            border_color=T.BORDER,
            border_width=1,
            font=ctk.CTkFont(size=12),
            command=self._file_panel._pick_files,
        )
        self._start_btn = ctk.CTkButton(
            self,
            text="▶  Start Queue",
            width=115, height=30,
            fg_color=T.ACCENT,
            hover_color=T.ACCENT_H,
            text_color="#FFFFFF",
            corner_radius=T.RADIUS_SM,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._start_queue,
        )

    def get_topbar(self):
        # Returns cached buttons — no new widgets created
        return ("Convert", "— batch re-encode media files",
                [self._add_btn, self._start_btn])

    def _start_queue(self):
        pass  # encode engine wired in later
