"""
Codex — Detail Panel
Tabbed right-side panel. Pure grid layout throughout.
Tabs: Media Info | Encode Settings | Tracks | Output
"""

import customtkinter as ctk
from src.utils import theme as T
from src.core.queue_manager import QueueManager
from src.ui.widgets.tooltip import Tooltip

TABS     = ["Media Info", "Encode Settings", "Tracks", "Output"]
TAB_H    = 40


class DetailPanel(ctk.CTkFrame):

    def __init__(self, master, queue: QueueManager, **kwargs):
        super().__init__(master, corner_radius=0, fg_color=T.BG, **kwargs)
        self.queue = queue
        self._tab_frames: dict[str, ctk.CTkScrollableFrame] = {}
        self._tab_btns:   dict[str, ctk.CTkButton]          = {}

        self.grid_rowconfigure(0, weight=0)   # tab bar
        self.grid_rowconfigure(1, weight=0)   # divider
        self.grid_rowconfigure(2, weight=1)   # body
        self.grid_columnconfigure(0, weight=1)

        self._build_tab_bar()
        self._build_bodies()
        self._switch_tab(TABS[0])
        self.queue.add_listener(self._on_queue_change)

    # ── Tab bar ───────────────────────────────────────────────────────────────

    def _build_tab_bar(self):
        bar = ctk.CTkFrame(self, fg_color=T.PANEL, corner_radius=0, height=TAB_H)
        bar.grid(row=0, column=0, sticky="ew")
        bar.grid_propagate(False)
        bar.grid_rowconfigure(0, weight=1)
        for i in range(len(TABS)):
            bar.grid_columnconfigure(i, weight=0)

        for col, name in enumerate(TABS):
            btn = ctk.CTkButton(
                bar, text=name,
                width=120, height=TAB_H,
                fg_color="transparent", hover_color=T.SURFACE,
                text_color=T.TEXT3, corner_radius=0,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda n=name: self._switch_tab(n),
            )
            btn.grid(row=0, column=col, sticky="ns")
            self._tab_btns[name] = btn

        ctk.CTkFrame(self, height=1, fg_color=T.BORDER2, corner_radius=0).grid(
            row=1, column=0, sticky="ew"
        )

    def _switch_tab(self, name: str):
        for n, btn in self._tab_btns.items():
            btn.configure(
                text_color=T.TEXT if n == name else T.TEXT3,
                fg_color=T.SURFACE if n == name else "transparent",
            )
        for n, frame in self._tab_frames.items():
            if n == name:
                frame.grid()
            else:
                frame.grid_remove()

    # ── Body ─────────────────────────────────────────────────────────────────

    def _build_bodies(self):
        container = ctk.CTkFrame(self, fg_color=T.BG, corner_radius=0)
        container.grid(row=2, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for name, builder in [
            ("Media Info",      self._build_media_info),
            ("Encode Settings", self._build_encode_settings),
            ("Tracks",          self._build_tracks),
            ("Output",          self._build_output),
        ]:
            scroll = ctk.CTkScrollableFrame(
                container, fg_color=T.BG, corner_radius=0,
                scrollbar_button_color=T.BORDER,
                scrollbar_button_hover_color=T.TEXT3,
            )
            scroll.grid(row=0, column=0, sticky="nsew")
            scroll.grid_columnconfigure(0, weight=1)
            builder(scroll)
            self._tab_frames[name] = scroll

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _card(self, parent, title: str, grid_row: int,
              first: bool = False) -> ctk.CTkFrame:
        """
        Titled card. The card frame itself has corner_radius=T.RADIUS so its
        border is visibly rounded. The header strip inside is corner_radius=0
        — the card clips its children so you never see square corners poking
        through the rounded border. No hacks needed.
        first=True adds 14px top gap so the card isn't flush against the tab bar.
        """
        top_pad = 14 if first else 0

        card = ctk.CTkFrame(
            parent, fg_color=T.PANEL, corner_radius=T.RADIUS,
            border_width=1, border_color=T.BORDER2,
        )
        card.grid(row=grid_row, column=0, sticky="ew",
                  padx=T.PAD, pady=(top_pad, 10))
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=0)
        card.grid_rowconfigure(1, weight=0)
        card.grid_rowconfigure(2, weight=0)

        # Header strip — flat, inset 1px so card rounded border shows all around
        hdr = ctk.CTkFrame(card, fg_color=T.SURFACE, corner_radius=0, height=34)
        hdr.grid(row=0, column=0, sticky="ew", padx=1, pady=(1, 0))
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(0, weight=1)
        hdr.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(
            hdr, text=title,
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=T.TEXT2, anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=14)

        # Thin separator between header and body
        ctk.CTkFrame(card, height=1, fg_color=T.BORDER2, corner_radius=0).grid(
            row=1, column=0, sticky="ew", padx=1
        )

        # Body frame
        body = ctk.CTkFrame(card, fg_color="transparent", corner_radius=0)
        body.grid(row=2, column=0, sticky="ew", padx=T.PAD, pady=T.PAD_V)
        body.grid_columnconfigure(0, weight=1)
        return body

    def _info_field(self, parent, grid_row: int, grid_col: int,
                    label: str, value: str, tip: str):
        cell = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=0)
        cell.grid(row=grid_row, column=grid_col, sticky="nw",
                  padx=(0, 20), pady=6)
        cell.grid_rowconfigure(0, weight=0)
        cell.grid_rowconfigure(1, weight=0)
        cell.grid_columnconfigure(0, weight=0)

        lbl_frame = ctk.CTkFrame(cell, fg_color="transparent", corner_radius=0)
        lbl_frame.grid(row=0, column=0, sticky="w")
        lbl_frame.grid_columnconfigure(0, weight=0)
        lbl_frame.grid_columnconfigure(1, weight=0)
        lbl_frame.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(
            lbl_frame, text=label.upper(),
            font=ctk.CTkFont(size=9, weight="bold"), text_color=T.TEXT3,
        ).grid(row=0, column=0, sticky="w")
        Tooltip(lbl_frame, tip).grid(row=0, column=1, padx=(5, 0), sticky="w")

        ctk.CTkLabel(
            cell, text=value,
            font=ctk.CTkFont(size=12, family="Courier New"),
            text_color=T.TEXT, anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))

    def _setting_row(self, parent, grid_row: int,
                     label: str, tip: str, control):
        fr = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=0)
        fr.grid(row=grid_row, column=0, sticky="ew", pady=6)
        fr.grid_columnconfigure(0, weight=1)
        fr.grid_columnconfigure(1, weight=0)
        fr.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(fr, fg_color="transparent", corner_radius=0)
        left.grid(row=0, column=0, sticky="w")
        left.grid_columnconfigure(0, weight=0)
        left.grid_columnconfigure(1, weight=0)
        left.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(
            left, text=label,
            font=ctk.CTkFont(size=12, weight="bold"), text_color=T.TEXT,
        ).grid(row=0, column=0, sticky="w")
        Tooltip(left, tip).grid(row=0, column=1, padx=(7, 0), sticky="w")

        control.grid(in_=fr, row=0, column=1, sticky="e")

    def _make_option(self, parent, values: list, default: str = None):
        om = ctk.CTkOptionMenu(
            parent, values=values,
            fg_color=T.SURFACE, button_color=T.SURFACE2,
            button_hover_color=T.BORDER,
            dropdown_fg_color=T.SURFACE,
            dropdown_hover_color=T.ACCENT_SUB,
            text_color=T.TEXT,
            font=ctk.CTkFont(size=11, family="Courier New"),
            width=160,
        )
        if default:
            om.set(default)
        return om

    def _make_toggle(self, parent, default: bool = False):
        sw = ctk.CTkSwitch(
            parent, text="",
            progress_color=T.ACCENT,
            button_color=T.TEXT,
            button_hover_color=T.TEXT2,
            fg_color=T.SURFACE2,
            width=40,
        )
        if default:
            sw.select()
        return sw

    def _on_queue_change(self):
        pass

    # ── Media Info ────────────────────────────────────────────────────────────

    def _build_media_info(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            parent,
            text="Select a file from the queue to inspect it",
            font=ctk.CTkFont(size=13), text_color=T.TEXT3,
        ).grid(row=0, column=0, pady=(40, 16))

        vbody = self._card(parent, "VIDEO STREAM", grid_row=1, first=False)
        vbody.grid_columnconfigure((0, 1), weight=1)
        for i, (lbl, val, tip) in enumerate([
            ("Codec",        "—", "The compression standard used for the video. H.265/HEVC is modern and efficient; H.264 is older but universally compatible."),
            ("Resolution",   "—", "The pixel dimensions of the video frame. 3840×2160 is 4K UHD — four times the detail of 1080p."),
            ("Frame Rate",   "—", "How many individual frames are shown per second. 23.976 fps is the standard cinematic rate used in most films."),
            ("Bit Rate",     "—", "Data used per second of video. Higher = better quality and larger file. 42 Mbps is typical for a 4K Blu-ray."),
            ("Bit Depth",    "—", "Shades per colour channel. 10-bit (1,024 shades) enables HDR and smoother gradients vs 8-bit (256 shades)."),
            ("Colour Space", "—", "The gamut of colours the video can represent. BT.2020 is the wide HDR gamut; BT.709 is standard HD."),
            ("HDR Format",   "—", "High Dynamic Range flavour. HDR10 is the open baseline. Dolby Vision / HDR10+ add dynamic per-scene metadata."),
            ("Scan Type",    "—", "Progressive = complete frames. Interlaced = alternating lines (older broadcast technique, can cause combing artefacts)."),
        ]):
            self._info_field(vbody, i // 2, i % 2, lbl, val, tip)

        cbody = self._card(parent, "CONTAINER", grid_row=2)
        cbody.grid_columnconfigure((0, 1), weight=1)
        for i, (lbl, val, tip) in enumerate([
            ("Format",    "—", "The wrapper that holds all streams. MKV supports unlimited tracks and chapters. MP4 has the widest device compatibility."),
            ("Duration",  "—", "Total playback length of the file."),
            ("File Size", "—", "Total size on disk, including all audio, video, and subtitle streams."),
            ("Chapters",  "—", "Named scene markers embedded in the file. Media players use these for chapter navigation."),
        ]):
            self._info_field(cbody, i // 2, i % 2, lbl, val, tip)

    # ── Encode Settings ───────────────────────────────────────────────────────

    def _build_encode_settings(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        vbody = self._card(parent, "VIDEO ENCODER", grid_row=0, first=True)
        vbody.grid_columnconfigure(0, weight=1)

        self._setting_row(vbody, 0, "Output Codec",
            "The format your output video will be compressed in. H.265 offers the best size-to-quality ratio for modern devices. AV1 is more efficient but much slower to encode.",
            self._make_option(vbody, ["H.265 / HEVC", "H.264 / AVC", "AV1", "VP9"], "H.265 / HEVC"))

        self._setting_row(vbody, 1, "Encoder Preset",
            "Speed vs compression trade-off. Slower presets take longer but produce smaller, better-quality files at the same CRF value. Medium is a sensible default.",
            self._make_option(vbody, ["ultrafast","veryfast","fast","medium","slow","veryslow"], "medium"))

        self._setting_row(vbody, 2, "Rate Control",
            "CRF targets consistent visual quality and lets file size vary. ABR targets a fixed average bitrate. 2-Pass ABR is most accurate for size-constrained encodes.",
            self._make_option(vbody, ["CRF (Quality)", "ABR (Bitrate)", "2-Pass ABR"], "CRF (Quality)"))

        # CRF slider — custom row with live value readout
        crf_row = ctk.CTkFrame(vbody, fg_color="transparent", corner_radius=0)
        crf_row.grid(row=3, column=0, sticky="ew", pady=6)
        crf_row.grid_columnconfigure(0, weight=1)
        crf_row.grid_columnconfigure(1, weight=0)
        crf_row.grid_columnconfigure(2, weight=0)
        crf_row.grid_rowconfigure(0, weight=1)

        lbl_fr = ctk.CTkFrame(crf_row, fg_color="transparent", corner_radius=0)
        lbl_fr.grid(row=0, column=0, sticky="w")
        lbl_fr.grid_columnconfigure(0, weight=0)
        lbl_fr.grid_columnconfigure(1, weight=0)
        lbl_fr.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(
            lbl_fr, text="CRF Value",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=T.TEXT,
        ).grid(row=0, column=0, sticky="w")
        Tooltip(lbl_fr,
            "Quality level for CRF mode. Lower = better quality, larger file. "
            "For H.265: 0 is lossless, 28 is default, 51 is worst. "
            "Values 18–24 are visually near-transparent."
        ).grid(row=0, column=1, padx=(7, 0), sticky="w")

        self._crf_val = ctk.CTkLabel(
            crf_row, text="22", width=30,
            font=ctk.CTkFont(size=11, family="Courier New"),
            text_color=T.ACCENT_H,
        )
        self._crf_val.grid(row=0, column=1, padx=(0, 8), sticky="e")

        ctk.CTkSlider(
            crf_row, from_=0, to=51, number_of_steps=51,
            width=140, progress_color=T.ACCENT,
            button_color=T.ACCENT, button_hover_color=T.ACCENT_H,
            fg_color=T.SURFACE2,
            command=lambda v: self._crf_val.configure(text=str(int(v))),
        ).grid(row=0, column=2, sticky="e")

        self._setting_row(vbody, 4, "Hardware Acceleration",
            "Uses your GPU (NVENC, VideoToolbox, QSV) instead of the CPU. Much faster, but output quality is usually slightly lower at the same settings.",
            self._make_toggle(vbody, default=False))

        rbody = self._card(parent, "RESOLUTION & FRAME RATE", grid_row=1)
        rbody.grid_columnconfigure(0, weight=1)

        self._setting_row(rbody, 0, "Output Resolution",
            "Pixel dimensions of the output. 'Match Source' keeps the original. Downscaling from 4K to 1080p dramatically reduces file size.",
            self._make_option(rbody, ["Match Source","3840×2160 (4K)","1920×1080 (FHD)","1280×720 (HD)","Custom…"], "Match Source"))

        self._setting_row(rbody, 1, "Frame Rate",
            "Frames per second of the output. 'Match Source' is almost always correct. Changing this can introduce motion judder if done incorrectly.",
            self._make_option(rbody, ["Match Source","23.976","24","25","29.97","30","50","59.94","60"], "Match Source"))

    # ── Tracks ────────────────────────────────────────────────────────────────

    def _build_tracks(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        abody = self._card(parent, "AUDIO TRACKS", grid_row=0, first=True)
        abody.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(abody,
            text="Add files to the queue to see available audio tracks.",
            font=ctk.CTkFont(size=11), text_color=T.TEXT3,
        ).grid(row=0, column=0, sticky="w", pady=6)

        sbody = self._card(parent, "SUBTITLE TRACKS", grid_row=1)
        sbody.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(sbody,
            text="Add files to the queue to see available subtitle tracks.",
            font=ctk.CTkFont(size=11), text_color=T.TEXT3,
        ).grid(row=0, column=0, sticky="w", pady=6)

    # ── Output ────────────────────────────────────────────────────────────────

    def _build_output(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        obody = self._card(parent, "OUTPUT DESTINATION", grid_row=0, first=True)
        obody.grid_columnconfigure(0, weight=1)

        self._setting_row(obody, 0, "Output Folder",
            "Where converted files are saved. 'Same folder as source' places them next to the originals.",
            self._make_option(obody, ["Same folder as source","Custom folder…"], "Same folder as source"))

        self._setting_row(obody, 1, "Container Format",
            "The wrapper format for your output file. MKV supports the most tracks. MP4 is most compatible with TVs and devices. WebM is for web use.",
            self._make_option(obody, ["MKV","MP4","WebM"], "MKV"))

        self._setting_row(obody, 2, "File Naming Pattern",
            "Template for output filenames. Variables replaced automatically: {name} = original name, {codec} = output codec, {res} = resolution.",
            self._make_option(obody, ["{name}_{codec}","{name}_{res}","{name}_converted","Custom…"], "{name}_{codec}"))

        self._setting_row(obody, 3, "Overwrite Existing Files",
            "If a file with the same name already exists, overwrite it. When off, Codex appends a number to avoid collision.",
            self._make_toggle(obody, default=False))
