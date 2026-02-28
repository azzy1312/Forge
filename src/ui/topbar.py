"""
Forge — Topbar
Fixed header bar. Title/subtitle on the left, action buttons on the right.
Buttons are passed in as already-created widgets and placed via grid only.
"""

import customtkinter as ctk
from src.utils import theme as T


class Topbar(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            height=T.TOPBAR_H,
            corner_radius=0,
            fg_color=T.PANEL,
            **kwargs,
        )
        self.grid_propagate(False)

        # 3 columns: title area | spacer | buttons area
        self.grid_columnconfigure(0, weight=0)   # title
        self.grid_columnconfigure(1, weight=1)   # spacer
        self.grid_columnconfigure(2, weight=0)   # buttons
        self.grid_rowconfigure(0, weight=1)

        # Title label
        self._title_lbl = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T.TEXT,
            anchor="w",
        )
        self._title_lbl.grid(row=0, column=0, sticky="w", padx=(16, 0))

        # Subtitle label
        self._sub_lbl = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=11),
            text_color=T.TEXT2,
            anchor="w",
        )
        self._sub_lbl.grid(row=0, column=0, sticky="w", padx=(105, 0))

        # Right-side button container — fixed slot, contents swapped per page
        self._btn_container = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self._btn_container.grid(row=0, column=2, sticky="e", padx=(0, 14))

        # Bottom divider
        ctk.CTkFrame(self, height=1, fg_color=T.BORDER2, corner_radius=0).grid(
            row=0, column=0, columnspan=3, sticky="sew"
        )

    def set_content(self, title: str, subtitle: str = "", right_widgets=None):
        """Update title/subtitle and swap in the right-side buttons."""

        # Recompute subtitle x offset based on title length
        title_px = len(title) * 9 + 16
        self._title_lbl.configure(text=title)
        self._sub_lbl.configure(text=f"  {subtitle}" if subtitle else "")
        self._sub_lbl.grid(row=0, column=0, sticky="w", padx=(title_px, 0))

        # Clear old buttons
        for w in self._btn_container.winfo_children():
            w.destroy()

        # Place new buttons via grid inside the container
        if right_widgets:
            for col, w in enumerate(right_widgets):
                w.grid(in_=self._btn_container, row=0, column=col,
                       padx=(0 if col == 0 else 6, 0), sticky="e")
