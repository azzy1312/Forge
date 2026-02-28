"""
Forge — Topbar
Title bar strip at the top of the main panel.
Content (title, subtitle, buttons) is swapped by each page.
"""

import customtkinter as ctk
from src.utils import theme as T


class Topbar(ctk.CTkFrame):
    """
    Thin bar across the top of the main content area.
    Pages call set_content() to inject their own title + action buttons.
    """

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            height=T.TOPBAR_H,
            corner_radius=0,
            fg_color=T.PANEL,
            **kwargs,
        )
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._inner = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self._inner.grid(row=0, column=0, sticky="nsew", padx=16, pady=0)
        self._inner.grid_columnconfigure(0, weight=1)
        self._inner.grid_rowconfigure(0, weight=1)

        # bottom divider
        div = ctk.CTkFrame(self, height=1, fg_color=T.BORDER2, corner_radius=0)
        div.grid(row=0, column=0, sticky="sew")

    def set_content(self, title: str, subtitle: str = "", right_widgets: list = None):
        """Clear and re-populate the topbar for a given page."""
        for w in self._inner.winfo_children():
            w.destroy()

        # left — title + subtitle
        left = ctk.CTkFrame(self._inner, fg_color="transparent", corner_radius=0)
        left.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            left,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T.TEXT,
        ).pack(side="left", padx=(0, 6))

        if subtitle:
            ctk.CTkLabel(
                left,
                text=subtitle,
                font=ctk.CTkFont(size=11),
                text_color=T.TEXT2,
            ).pack(side="left")

        # right — action widgets provided by the page
        if right_widgets:
            right = ctk.CTkFrame(self._inner, fg_color="transparent", corner_radius=0)
            right.grid(row=0, column=1, sticky="e")
            for w in right_widgets:
                w.pack(side="left", padx=4)
