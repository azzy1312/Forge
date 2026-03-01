"""
Forge — Topbar
Fixed header bar. Title/subtitle on the left, action buttons on the right.
Height matches LOGO_H in theme so the bottom divider is a single unbroken
line across the full window width.
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

        # 3 columns: title | spacer | buttons
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self._title_lbl = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T.TEXT,
            anchor="w",
        )
        self._title_lbl.grid(row=0, column=0, sticky="w", padx=(20, 0))

        self._sub_lbl = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=11),
            text_color=T.TEXT2,
            anchor="w",
        )
        self._sub_lbl.grid(row=0, column=0, sticky="w", padx=(20, 0))

        # Button container — right-anchored, fixed slot
        self.btn_container = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.btn_container.grid(row=0, column=2, sticky="e", padx=(0, 16))
        self.btn_container.grid_rowconfigure(0, weight=1)

        # Bottom divider — must be flush with sidebar logo divider
        ctk.CTkFrame(self, height=1, fg_color=T.BORDER2, corner_radius=0).grid(
            row=0, column=0, columnspan=3, sticky="sew"
        )

    def set_content(self, title: str, subtitle: str = "", right_widgets=None):
        # Measure title width in pixels (rough: 9px per char at size 14 bold)
        title_px = len(title) * 9 + 20
        self._title_lbl.configure(text=title)
        self._sub_lbl.configure(text=f"  {subtitle}" if subtitle else "")
        self._sub_lbl.grid(row=0, column=0, sticky="w", padx=(title_px, 0))

        # Detach all current buttons without destroying them
        for w in self.btn_container.winfo_children():
            w.grid_remove()

        if right_widgets:
            for col, w in enumerate(right_widgets):
                w.grid(row=0, column=col, padx=(0 if col == 0 else 8, 0), sticky="e")
