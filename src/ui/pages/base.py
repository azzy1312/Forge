"""
Forge — Base Page
All pages inherit from this.
Topbar buttons are built ONCE in build() and cached — never recreated on navigation.
"""

import customtkinter as ctk
from src.utils import theme as T


class BasePage(ctk.CTkFrame):

    def __init__(self, master, topbar, **kwargs):
        super().__init__(master, corner_radius=0, fg_color=T.BG, **kwargs)
        self._topbar = topbar
        self._built  = False

    def show(self):
        """Called by the app shell on navigation. Builds once, then just lifts."""
        if not self._built:
            self.build()
            self._built = True
        title, subtitle, right_widgets = self.get_topbar()
        self._topbar.set_content(title, subtitle, right_widgets)
        self.lift()

    def build(self):
        raise NotImplementedError

    def get_topbar(self) -> tuple:
        return ("Page", "", [])
