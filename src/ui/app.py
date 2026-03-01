"""
VMC — App Shell
Root window. Sidebar left, topbar + pages right.

Layout:
  row 0, col 0  = Sidebar          (fixed width, full height)
  row 0, col 1  = Topbar+Pages     (expands)
  row 1, col 0+1 = ProgressFooter  (full width — the ONE bottom bar)

Putting the footer here at the root level means its top divider is a single
1px line that genuinely spans sidebar + main area with no gap or offset.
"""

import customtkinter as ctk
from src.utils import theme as T
from src.ui.sidebar import Sidebar
from src.ui.topbar  import Topbar
from src.ui.pages.convert   import ConvertPage
from src.ui.pages.inspector import InspectorPage
from src.ui.pages.presets   import PresetsPage
from src.ui.pages.settings  import SettingsPage
from src.core.queue_manager import QueueManager
from src.ui.widgets.progress_footer import ProgressFooter


class ForgeApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("VMC — Video Media Control")
        self.geometry(f"{T.WINDOW_DEFAULT_W}x{T.WINDOW_DEFAULT_H}")
        self.minsize(T.WINDOW_MIN_W, T.WINDOW_MIN_H)
        self.configure(fg_color=T.BG)

        self._build()
        self._navigate("convert")

    def _build(self):
        # row 0 = content, row 1 = footer (full width)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)   # sidebar fixed
        self.grid_columnconfigure(1, weight=1)   # main expands

        # ── Sidebar ───────────────────────────────────────────────────────────
        self._sidebar = Sidebar(self, on_navigate=self._navigate)
        self._sidebar.grid(row=0, column=0, sticky="nsew")

        # ── Right column ──────────────────────────────────────────────────────
        right = ctk.CTkFrame(self, corner_radius=0, fg_color=T.BG)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(0, weight=0)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self._topbar = Topbar(right)
        self._topbar.grid(row=0, column=0, sticky="ew")

        self._page_container = ctk.CTkFrame(right, corner_radius=0, fg_color=T.BG)
        self._page_container.grid(row=1, column=0, sticky="nsew")
        self._page_container.grid_rowconfigure(0, weight=1)
        self._page_container.grid_columnconfigure(0, weight=1)

        # ── Shared queue + full-width footer (row 1, spans both columns) ──────
        # The footer lives at the ROOT level so its top divider is one true
        # line across the entire window — sidebar and main area alike.
        self._queue = QueueManager()
        self._footer = ProgressFooter(self, self._queue)
        self._footer.grid(row=1, column=0, columnspan=2, sticky="ew")

        # ── Pages — pass the shared queue so convert page uses the same one ───
        self._pages: dict[str, object] = {
            "convert":   ConvertPage(self._page_container, self._topbar,
                                     self._queue),
            "inspector": InspectorPage(self._page_container, self._topbar),
            "presets":   PresetsPage(self._page_container,  self._topbar),
            "settings":  SettingsPage(self._page_container, self._topbar),
        }
        for page in self._pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def _navigate(self, key: str):
        page = self._pages.get(key)
        if page:
            page.show()
