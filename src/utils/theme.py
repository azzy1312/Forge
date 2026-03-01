"""
Codex — Theme
All colours, fonts, and sizing constants live here.
Change something once, it updates everywhere.
"""

# ── Palette ──────────────────────────────────────────────────────────────────
BG           = "#1A171B"   # window background
PANEL        = "#242025"   # sidebar, topbar, cards
SURFACE      = "#2E2A30"   # slightly raised elements
SURFACE2     = "#3A353C"   # hover states, table rows
BORDER       = "#48434A"   # visible borders
BORDER2      = "#3A353C"   # subtle dividers

TEXT         = "#F0EEF1"   # primary text
TEXT2        = "#9C929E"   # secondary / muted
TEXT3        = "#635E65"   # placeholder / disabled

ACCENT       = "#591D8F"   # primary accent — deep royal purple
ACCENT_H     = "#6B25AC"   # accent hover
ACCENT_SUB   = "#2E1048"   # accent tint background
ACCENT_GLOW  = "#591D8F"   # used in box-shadow equivalents

RED          = "#C0392B"
GREEN        = "#27AE60"
AMBER        = "#D4892A"

# ── Typography ────────────────────────────────────────────────────────────────
FONT_UI      = "Helvetica Neue"
FONT_MONO    = ("Courier New", 11)

# ── Sizing ────────────────────────────────────────────────────────────────────
SIDEBAR_W         = 220
SIDEBAR_COLLAPSED = 60

# TOPBAR_H and LOGO_H must be identical — they share the same horizontal band
# across the full window width. The divider at the bottom of each must be
# at exactly the same Y coordinate so they appear as one continuous line.
TOPBAR_H          = 56      # matches sidebar logo row height exactly
LOGO_H            = 56      # sidebar logo row — keep in sync with TOPBAR_H

QUEUE_HEADER_H    = 56      # queue panel header — same band as topbar

RADIUS            = 8
RADIUS_SM         = 5

# Inner padding used consistently inside every card body
PAD               = 14      # horizontal card inset
PAD_V             = 12      # vertical card inset

WINDOW_MIN_W = 1000
WINDOW_MIN_H = 640
WINDOW_DEFAULT_W = 1280
WINDOW_DEFAULT_H = 760
