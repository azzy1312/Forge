"""
Forge — Sidebar
Collapsible navigation sidebar with icon + label nav items.
"""

import customtkinter as ctk
from src.utils import theme as T


# ── Nav item definition ───────────────────────────────────────────────────────
NAV_ITEMS = [
    # (section_label, key, icon, label)
    ("MAIN",     "convert",   "⬡",  "Convert"),
    ("MAIN",     "inspector", "◎",  "Inspector"),
    ("MAIN",     "presets",   "▤",  "Presets"),
    ("SYSTEM",   "settings",  "⊙",  "Settings"),
]


class Sidebar(ctk.CTkFrame):
    """
    Collapsible sidebar.  Calls on_navigate(key) when a nav item is clicked.
    """

    def __init__(self, master, on_navigate, **kwargs):
        super().__init__(
            master,
            width=T.SIDEBAR_W,
            corner_radius=0,
            fg_color=T.PANEL,
            **kwargs,
        )
        self.on_navigate = on_navigate
        self._expanded   = True
        self._active_key = "convert"
        self._nav_buttons: dict[str, ctk.CTkButton] = {}

        self.grid_propagate(False)
        self._build()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build(self):
        self.grid_rowconfigure(1, weight=1)   # nav section expands
        self.grid_columnconfigure(0, weight=1)

        self._build_logo()
        self._build_nav()
        self._build_footer()

    def _build_logo(self):
        logo_frame = ctk.CTkFrame(self, fg_color=T.PANEL, corner_radius=0, height=56)
        logo_frame.grid(row=0, column=0, sticky="ew")
        logo_frame.grid_propagate(False)
        logo_frame.grid_columnconfigure(1, weight=1)

        # purple square logo mark
        self._logo_mark = ctk.CTkLabel(
            logo_frame,
            text="F",
            width=28, height=28,
            fg_color=T.ACCENT,
            corner_radius=6,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T.TEXT,
        )
        self._logo_mark.grid(row=0, column=0, padx=(14, 8), pady=14)

        self._logo_text = ctk.CTkLabel(
            logo_frame,
            text="FORGE",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=T.TEXT,
            anchor="w",
        )
        self._logo_text.grid(row=0, column=1, sticky="w")

        # bottom divider
        div = ctk.CTkFrame(self, height=1, fg_color=T.BORDER2, corner_radius=0)
        div.grid(row=0, column=0, sticky="sew", padx=0)

    def _build_nav(self):
        nav_outer = ctk.CTkScrollableFrame(
            self,
            fg_color=T.PANEL,
            scrollbar_button_color=T.BORDER,
            scrollbar_button_hover_color=T.TEXT3,
            corner_radius=0,
        )
        nav_outer.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        nav_outer.grid_columnconfigure(0, weight=1)

        self._nav_widgets: list[ctk.CTkBaseClass] = []
        last_section = None
        row = 0

        for section, key, icon, label in NAV_ITEMS:
            # section divider label
            if section != last_section:
                lbl = ctk.CTkLabel(
                    nav_outer,
                    text=section,
                    font=ctk.CTkFont(size=9, weight="bold"),
                    text_color=T.TEXT3,
                    anchor="w",
                )
                lbl.grid(row=row, column=0, sticky="ew", padx=10, pady=(10, 2))
                self._nav_widgets.append(lbl)
                row += 1
                last_section = section

            btn = self._make_nav_button(nav_outer, key, icon, label)
            btn.grid(row=row, column=0, sticky="ew", padx=6, pady=1)
            self._nav_buttons[key] = btn
            self._nav_widgets.append(btn)
            row += 1

        self._refresh_active()

    def _make_nav_button(self, parent, key, icon, label) -> ctk.CTkButton:
        def on_click():
            self._set_active(key)
            self.on_navigate(key)

        btn = ctk.CTkButton(
            parent,
            text=f"  {icon}   {label}",
            anchor="w",
            height=36,
            corner_radius=T.RADIUS_SM,
            fg_color="transparent",
            hover_color=T.SURFACE,
            text_color=T.TEXT2,
            font=ctk.CTkFont(size=12, weight="normal"),
            command=on_click,
        )
        return btn

    def _build_footer(self):
        div = ctk.CTkFrame(self, height=1, fg_color=T.BORDER2, corner_radius=0)
        div.grid(row=2, column=0, sticky="ew")

        footer = ctk.CTkFrame(self, fg_color=T.PANEL, corner_radius=0, height=44)
        footer.grid(row=3, column=0, sticky="ew")
        footer.grid_propagate(False)
        footer.grid_columnconfigure(0, weight=1)

        self._collapse_btn = ctk.CTkButton(
            footer,
            text="  ◁   Collapse",
            anchor="w",
            height=32,
            corner_radius=T.RADIUS_SM,
            fg_color="transparent",
            hover_color=T.SURFACE,
            text_color=T.TEXT3,
            font=ctk.CTkFont(size=11),
            command=self.toggle,
        )
        self._collapse_btn.grid(row=0, column=0, sticky="ew", padx=6, pady=6)

    # ── State ─────────────────────────────────────────────────────────────────

    def _set_active(self, key: str):
        self._active_key = key
        self._refresh_active()

    def _refresh_active(self):
        for k, btn in self._nav_buttons.items():
            if k == self._active_key:
                btn.configure(
                    fg_color=T.ACCENT_SUB,
                    text_color=T.TEXT,
                    hover_color=T.ACCENT_SUB,
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=T.TEXT2,
                    hover_color=T.SURFACE,
                )

    def toggle(self):
        if self._expanded:
            self._collapse()
        else:
            self._expand()

    def _collapse(self):
        self._expanded = False
        self.configure(width=T.SIDEBAR_COLLAPSED)
        self._logo_text.grid_remove()
        self._collapse_btn.configure(text="  ▷")
        for k, btn in self._nav_buttons.items():
            icon = [i for _, key, i, _ in NAV_ITEMS if key == k][0]
            btn.configure(text=f"  {icon}", anchor="center")
        # hide section labels
        for w in self._nav_widgets:
            if isinstance(w, ctk.CTkLabel):
                w.grid_remove()

    def _expand(self):
        self._expanded = True
        self.configure(width=T.SIDEBAR_W)
        self._logo_text.grid()
        self._collapse_btn.configure(text="  ◁   Collapse")
        for k, btn in self._nav_buttons.items():
            icon = [i for _, key, i, _ in NAV_ITEMS if key == k][0]
            label = [l for _, key, _, l in NAV_ITEMS if key == k][0]
            btn.configure(text=f"  {icon}   {label}", anchor="w")
        for w in self._nav_widgets:
            if isinstance(w, ctk.CTkLabel):
                w.grid()
