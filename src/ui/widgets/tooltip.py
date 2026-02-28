"""
Forge — Tooltip
Small ⓘ icon that shows a description popup on hover.
Self-contained widget — grid-safe, no pack() used outside this file.
"""

import customtkinter as ctk
from src.utils import theme as T


class Tooltip(ctk.CTkFrame):

    def __init__(self, master, text: str, **kwargs):
        super().__init__(
            master, width=16, height=16,
            fg_color="transparent", corner_radius=0, **kwargs,
        )
        self._text    = text
        self._tip_win = None
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._icon = ctk.CTkLabel(
            self, text="ⓘ",
            font=ctk.CTkFont(size=11),
            text_color=T.TEXT3,
            width=16, height=16,
            cursor="question_arrow",
        )
        self._icon.grid(row=0, column=0)
        self._icon.bind("<Enter>", self._show)
        self._icon.bind("<Leave>", self._hide)
        self.bind("<Enter>", self._show)
        self.bind("<Leave>", self._hide)

    def _show(self, event=None):
        if self._tip_win:
            return
        x = self._icon.winfo_rootx() + 8
        y = self._icon.winfo_rooty() - 8

        self._tip_win = ctk.CTkToplevel(self)
        self._tip_win.wm_overrideredirect(True)
        self._tip_win.configure(fg_color=T.SURFACE2)
        self._tip_win.attributes("-topmost", True)

        ctk.CTkLabel(
            self._tip_win,
            text=self._text,
            font=ctk.CTkFont(size=11),
            text_color=T.TEXT,
            wraplength=220,
            justify="left",
            fg_color=T.SURFACE2,
            corner_radius=T.RADIUS_SM,
        ).grid(row=0, column=0, padx=10, pady=8)

        self._tip_win.update_idletasks()
        tip_h = self._tip_win.winfo_height()
        tip_w = self._tip_win.winfo_width()
        # Position above and centred on the icon
        self._tip_win.wm_geometry(f"{tip_w}x{tip_h}+{x}+{y - tip_h}")

    def _hide(self, event=None):
        if self._tip_win:
            self._tip_win.destroy()
            self._tip_win = None
