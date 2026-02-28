"""
Forge — Base Page
All pages inherit from this. Provides a standard structure:
  - topbar content registration on show()
  - a body frame to build into
"""

import customtkinter as ctk
from src.utils import theme as T


class BasePage(ctk.CTkFrame):
    """
    Every page in Forge inherits from BasePage.

    Subclasses must implement:
        build()          → called once on first show, build your widgets here
        get_topbar()     → return (title, subtitle, [right_widgets])
    """

    def __init__(self, master, topbar, **kwargs):
        super().__init__(
            master,
            corner_radius=0,
            fg_color=T.BG,
            **kwargs,
        )
        self._topbar  = topbar
        self._built   = False

    def show(self):
        """Called by app shell when navigating to this page."""
        if not self._built:
            self.build()
            self._built = True
        title, subtitle, right_widgets = self.get_topbar()
        self._topbar.set_content(title, subtitle, right_widgets)
        self.lift()

    # ── Subclasses override these ─────────────────────────────────────────────

    def build(self):
        raise NotImplementedError

    def get_topbar(self) -> tuple:
        return ("Page", "", [])
