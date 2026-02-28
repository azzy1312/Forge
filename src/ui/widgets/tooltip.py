"""
Forge — Tooltip Helper
Small ⓘ button that shows a description on hover.
Used everywhere a setting or info field needs an explanation.
"""

import customtkinter as ctk
from src.utils import theme as T


class Tooltip(ctk.CTkFrame):
    """
    A small circular eye/info button.
    Hover to reveal a descriptive tooltip above it.
    """

    def __init__(self, master, text: str, **kwargs):
        super().__init__(
            master, width=16, height=16,
            fg_color="transparent", corner_radius=0,
            **kwargs,
        )
        self._text = text
        self._tip_win = None

        self._btn = ctk.CTkLabel(
            self, text="ⓘ",
            font=ctk.CTkFont(size=11),
            text_color=T.TEXT3,
            width=16, height=16,
            cursor="question_arrow",
        )
        self._btn.pack()
        self._btn.bind("<Enter>", self._show)
        self._btn.bind("<Leave>", self._hide)

    def _show(self, event):
        if self._tip_win:
            return
        x = self._btn.winfo_rootx() + 8
        y = self._btn.winfo_rooty() - 6

        self._tip_win = ctk.CTkToplevel(self)
        self._tip_win.wm_overrideredirect(True)
        self._tip_win.wm_geometry(f"+{x}+{y}")
        self._tip_win.configure(fg_color=T.SURFACE2)
        self._tip_win.attributes("-topmost", True)

        ctk.CTkLabel(
            self._tip_win,
            text=self._text,
            font=ctk.CTkFont(size=11),
            text_color=T.TEXT,
            wraplength=220,
            justify="left",
            corner_radius=T.RADIUS_SM,
            fg_color=T.SURFACE2,
        ).pack(padx=10, pady=8)

        # Reposition above the button after rendering
        self._tip_win.update_idletasks()
        tip_h = self._tip_win.winfo_height()
        self._tip_win.wm_geometry(f"+{x}+{y - tip_h}")

    def _hide(self, event):
        if self._tip_win:
            self._tip_win.destroy()
            self._tip_win = None
