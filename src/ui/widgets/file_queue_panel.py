"""
Forge — File Queue Panel
Left panel: drop zone + scrollable file list.
Pure grid layout throughout — no pack() calls anywhere.
"""

import os
import customtkinter as ctk
import tkinter.filedialog as fd

from src.utils import theme as T
from src.utils.file_utils import is_supported, friendly_size, friendly_ext
from src.core.queue_manager import QueueManager, QueueEntry, FileStatus

STATUS_COLOURS = {
    FileStatus.READY:    T.TEXT3,
    FileStatus.ENCODING: T.ACCENT,
    FileStatus.DONE:     T.GREEN,
    FileStatus.ERROR:    T.RED,
    FileStatus.SKIPPED:  T.AMBER,
}

# Fixed pixel dimensions
PANEL_W    = 300
HEADER_H   = 40
DROP_H     = 130   # fixed height drop zone
BTN_SIZE   = 26


class FileQueuePanel(ctk.CTkFrame):

    def __init__(self, master, queue: QueueManager, **kwargs):
        super().__init__(
            master, width=PANEL_W, corner_radius=0, fg_color=T.PANEL, **kwargs,
        )
        self.queue = queue
        self.grid_propagate(False)
        # Row 0 = header, Row 1 = drop zone, Row 2 = file list (expands), Row 3 = divider
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self._build()
        self.queue.add_listener(self._refresh)

    # ── Header ────────────────────────────────────────────────────────────────

    def _build(self):
        self._build_header()
        self._build_drop_zone()
        self._build_list()
        # Bottom divider
        ctk.CTkFrame(self, height=1, fg_color=T.BORDER2, corner_radius=0).grid(
            row=3, column=0, sticky="ew"
        )

    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color=T.PANEL, corner_radius=0, height=HEADER_H)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        # Col 0 = label (expands), Col 1 = folder btn, Col 2 = clear btn
        hdr.grid_columnconfigure(0, weight=1)
        hdr.grid_columnconfigure(1, weight=0)
        hdr.grid_columnconfigure(2, weight=0)
        hdr.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(
            hdr, text="QUEUE",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=T.TEXT3, anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=(14, 0))

        ctk.CTkButton(
            hdr, text="📁", width=BTN_SIZE, height=BTN_SIZE,
            fg_color="transparent", hover_color=T.SURFACE,
            text_color=T.TEXT3, corner_radius=T.RADIUS_SM,
            font=ctk.CTkFont(size=13), command=self._pick_folder,
        ).grid(row=0, column=1, padx=(0, 4))

        ctk.CTkButton(
            hdr, text="✕", width=BTN_SIZE, height=BTN_SIZE,
            fg_color="transparent", hover_color=T.SURFACE,
            text_color=T.TEXT3, corner_radius=T.RADIUS_SM,
            font=ctk.CTkFont(size=13), command=self._clear_all,
        ).grid(row=0, column=2, padx=(0, 8))

        # Divider under header
        ctk.CTkFrame(self, height=1, fg_color=T.BORDER2, corner_radius=0).grid(
            row=0, column=0, sticky="sew"
        )

    # ── Drop zone ─────────────────────────────────────────────────────────────

    def _build_drop_zone(self):
        outer = ctk.CTkFrame(
            self, fg_color=T.SURFACE, corner_radius=T.RADIUS,
            border_width=1, border_color=T.BORDER, height=DROP_H,
        )
        outer.grid(row=1, column=0, sticky="ew", padx=10, pady=(8, 6))
        outer.grid_propagate(False)
        outer.grid_columnconfigure(0, weight=1)
        # 4 rows: icon, title, subtitle, button
        for r in range(4):
            outer.grid_rowconfigure(r, weight=0)
        outer.grid_rowconfigure(4, weight=1)   # padding row at bottom

        ctk.CTkLabel(
            outer, text="⊕", font=ctk.CTkFont(size=20), text_color=T.TEXT3,
        ).grid(row=0, column=0, pady=(14, 0))

        ctk.CTkLabel(
            outer, text="Drop files or folders here",
            font=ctk.CTkFont(size=11, weight="bold"), text_color=T.TEXT3,
        ).grid(row=1, column=0, pady=(4, 0))

        ctk.CTkLabel(
            outer, text="MP4 · MKV · AVI · MOV · WebM · and more",
            font=ctk.CTkFont(size=10), text_color=T.TEXT3,
        ).grid(row=2, column=0)

        ctk.CTkButton(
            outer, text="Browse files", width=110, height=26,
            fg_color=T.SURFACE2, hover_color=T.BORDER,
            text_color=T.TEXT2, corner_radius=T.RADIUS_SM,
            font=ctk.CTkFont(size=11), command=self._pick_files,
        ).grid(row=3, column=0, pady=(6, 0))

        outer.bind("<Enter>", lambda e: outer.configure(border_color=T.ACCENT))
        outer.bind("<Leave>", lambda e: outer.configure(border_color=T.BORDER))

    # ── File list ─────────────────────────────────────────────────────────────

    def _build_list(self):
        self._list_scroll = ctk.CTkScrollableFrame(
            self, fg_color=T.PANEL, corner_radius=0,
            scrollbar_button_color=T.BORDER,
            scrollbar_button_hover_color=T.TEXT3,
        )
        self._list_scroll.grid(row=2, column=0, sticky="nsew")
        self._list_scroll.grid_columnconfigure(0, weight=1)

    def _refresh(self):
        for w in self._list_scroll.winfo_children():
            w.destroy()
        for i, entry in enumerate(self.queue.entries):
            self._add_row(i, entry)

    def _add_row(self, index: int, entry: QueueEntry):
        selected = (index == self.queue.selected_index)

        row = ctk.CTkFrame(
            self._list_scroll,
            fg_color=T.ACCENT_SUB if selected else "transparent",
            corner_radius=T.RADIUS_SM, cursor="hand2",
        )
        row.grid(row=index, column=0, sticky="ew", padx=4, pady=1)
        # Col 0 = ext badge, Col 1 = name+meta (expands), Col 2 = dot
        row.grid_columnconfigure(0, weight=0)
        row.grid_columnconfigure(1, weight=1)
        row.grid_columnconfigure(2, weight=0)

        def on_click(e, i=index):
            self.queue.select(i)

        ext = ctk.CTkLabel(
            row, text=friendly_ext(entry.path),
            width=36, height=26, fg_color=T.SURFACE2, corner_radius=3,
            font=ctk.CTkFont(size=10, weight="bold"), text_color=T.TEXT3,
        )
        ext.grid(row=0, column=0, rowspan=2, padx=(8, 6), pady=8, sticky="w")

        name = ctk.CTkLabel(
            row, text=entry.name,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=T.TEXT, anchor="w",
        )
        name.grid(row=0, column=1, sticky="ew", padx=(0, 4), pady=(8, 0))

        meta = ctk.CTkLabel(
            row, text=f"{entry.size_str}  ·  {entry.duration}",
            font=ctk.CTkFont(size=10), text_color=T.TEXT2, anchor="w",
        )
        meta.grid(row=1, column=1, sticky="ew", padx=(0, 4), pady=(0, 8))

        dot = ctk.CTkFrame(
            row, width=8, height=8,
            fg_color=STATUS_COLOURS.get(entry.status, T.TEXT3), corner_radius=4,
        )
        dot.grid(row=0, column=2, rowspan=2, padx=(0, 10), sticky="e")

        for w in (row, ext, name, meta, dot):
            w.bind("<Button-1>", on_click)

    # ── File picking ──────────────────────────────────────────────────────────

    def _pick_files(self):
        paths = fd.askopenfilenames(
            title="Add files to queue",
            filetypes=[
                ("Video files", "*.mp4 *.mkv *.avi *.mov *.webm *.m4v *.flv *.wmv *.ts *.mpg"),
                ("All files", "*.*"),
            ],
        )
        for p in paths:
            self._add_path(p)

    def _pick_folder(self):
        folder = fd.askdirectory(title="Add folder to queue")
        if folder:
            for root, _, files in os.walk(folder):
                for f in sorted(files):
                    self._add_path(os.path.join(root, f))

    def _add_path(self, path: str):
        if not is_supported(path):
            return
        self.queue.add(QueueEntry(
            path=path,
            name=os.path.basename(path),
            size_str=friendly_size(path),
            duration="—",
        ))

    def _clear_all(self):
        self.queue.clear()
