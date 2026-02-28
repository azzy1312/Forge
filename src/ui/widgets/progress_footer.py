"""
Forge — Progress Footer
Fixed-height bottom bar. Pure grid layout.
Col 0 = status+bar (expands), Col 1 = percentage, Col 2 = buttons
"""

import customtkinter as ctk
from src.utils import theme as T
from src.core.queue_manager import QueueManager, FileStatus

FOOTER_H = 54
BTN_W    = 84
BTN_H    = 28


class ProgressFooter(ctk.CTkFrame):

    def __init__(self, master, queue: QueueManager, **kwargs):
        super().__init__(
            master, height=FOOTER_H, corner_radius=0, fg_color=T.PANEL, **kwargs,
        )
        self.queue = queue
        self.grid_propagate(False)
        # Col 0 = status area, Col 1 = pct label, Col 2 = btn area
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self._build()
        self.queue.add_listener(self._refresh)
        self._refresh()

    def _build(self):
        # Top divider pinned to very top of the frame
        ctk.CTkFrame(self, height=1, fg_color=T.BORDER2, corner_radius=0).grid(
            row=0, column=0, columnspan=3, sticky="new"
        )

        # ── Status area (Col 0) ───────────────────────────────────────────────
        status_area = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        status_area.grid(row=0, column=0, sticky="ew", padx=(16, 8), pady=(10, 8))
        status_area.grid_columnconfigure(0, weight=1)
        status_area.grid_rowconfigure(0, weight=0)
        status_area.grid_rowconfigure(1, weight=0)

        self._status_lbl = ctk.CTkLabel(
            status_area, text="Ready  —  add files to the queue",
            font=ctk.CTkFont(size=11, family="Courier New"),
            text_color=T.TEXT2, anchor="w",
        )
        self._status_lbl.grid(row=0, column=0, sticky="ew")

        self._progress = ctk.CTkProgressBar(
            status_area, height=3,
            progress_color=T.ACCENT, fg_color=T.SURFACE2, corner_radius=2,
        )
        self._progress.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        self._progress.set(0)

        # ── Percentage label (Col 1) ──────────────────────────────────────────
        self._pct_lbl = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=11, family="Courier New"),
            text_color=T.ACCENT_H, width=42, anchor="e",
        )
        self._pct_lbl.grid(row=0, column=1, sticky="e", padx=(0, 10))

        # ── Button area (Col 2) ───────────────────────────────────────────────
        btn_area = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        btn_area.grid(row=0, column=2, sticky="e", padx=(0, 14))
        btn_area.grid_columnconfigure(0, weight=0)
        btn_area.grid_columnconfigure(1, weight=0)
        btn_area.grid_rowconfigure(0, weight=1)

        self._pause_btn = ctk.CTkButton(
            btn_area, text="⏸  Pause",
            width=BTN_W, height=BTN_H,
            fg_color=T.SURFACE, hover_color=T.SURFACE2,
            text_color=T.TEXT2, corner_radius=T.RADIUS_SM,
            font=ctk.CTkFont(size=11),
            command=self._on_pause,
        )
        self._pause_btn.grid(row=0, column=0, padx=(0, 6))

        self._cancel_btn = ctk.CTkButton(
            btn_area, text="✕  Cancel",
            width=BTN_W, height=BTN_H,
            fg_color=T.SURFACE, hover_color=T.SURFACE2,
            text_color=T.RED, corner_radius=T.RADIUS_SM,
            border_color=T.RED, border_width=1,
            font=ctk.CTkFont(size=11),
            command=self._on_cancel,
        )
        self._cancel_btn.grid(row=0, column=1)

    def _refresh(self):
        encoding = [e for e in self.queue.entries if e.status == FileStatus.ENCODING]
        done  = self.queue.done_count()
        total = len(self.queue)

        if encoding:
            e = encoding[0]
            pct = int(e.progress * 100)
            self._status_lbl.configure(text=f"Encoding  {e.name}  —  {done}/{total} complete")
            self._progress.set(e.progress)
            self._pct_lbl.configure(text=f"{pct}%")
        elif total == 0:
            self._status_lbl.configure(text="Ready  —  add files to the queue")
            self._progress.set(0)
            self._pct_lbl.configure(text="")
        elif done == total:
            self._status_lbl.configure(text=f"All done  —  {done} file(s) converted")
            self._progress.set(1)
            self._pct_lbl.configure(text="100%")
        else:
            self._status_lbl.configure(
                text=f"{self.queue.ready_count()} file(s) queued  ·  {done} done"
            )
            self._progress.set(done / total if total else 0)
            self._pct_lbl.configure(text="")

    def _on_pause(self):
        pass

    def _on_cancel(self):
        pass
