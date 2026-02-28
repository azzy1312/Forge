"""
Forge — Detail Panel
Tabbed right-side panel on the Convert page.
Tabs: Media Info | Encode Settings | Tracks | Output
"""

import customtkinter as ctk
from src.utils import theme as T
from src.core.queue_manager import QueueManager
from src.ui.widgets.tooltip import Tooltip


TABS = ["Media Info", "Encode Settings", "Tracks", "Output"]


class DetailPanel(ctk.CTkFrame):

    def __init__(self, master, queue: QueueManager, **kwargs):
        super().__init__(master, corner_radius=0, fg_color=T.BG, **kwargs)
        self.queue = queue
        self._active_tab = TABS[0]
        self._tab_frames: dict[str, ctk.CTkFrame] = {}
        self._tab_btns:   dict[str, ctk.CTkButton] = {}

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_tabs()
        self._build_bodies()
        self._switch_tab(TABS[0])
        self.queue.add_listener(self._on_queue_change)

    # ── Tab bar ───────────────────────────────────────────────────────────────

    def _build_tabs(self):
        bar = ctk.CTkFrame(self, fg_color=T.PANEL, corner_radius=0, height=40)
        bar.grid(row=0, column=0, sticky="ew")
        bar.grid_propagate(False)

        for i, name in enumerate(TABS):
            btn = ctk.CTkButton(
                bar, text=name,
                width=120, height=40,
                fg_color="transparent",
                hover_color=T.SURFACE,
                text_color=T.TEXT3,
                corner_radius=0,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda n=name: self._switch_tab(n),
            )
            btn.pack(side="left")
            self._tab_btns[name] = btn

        div = ctk.CTkFrame(self, height=1, fg_color=T.BORDER2, corner_radius=0)
        div.grid(row=0, column=0, sticky="sew")

    def _switch_tab(self, name: str):
        self._active_tab = name
        for n, btn in self._tab_btns.items():
            if n == name:
                btn.configure(text_color=T.TEXT, fg_color=T.SURFACE)
            else:
                btn.configure(text_color=T.TEXT3, fg_color="transparent")
        for n, frame in self._tab_frames.items():
            if n == name:
                frame.grid()
            else:
                frame.grid_remove()

    # ── Tab bodies ────────────────────────────────────────────────────────────

    def _build_bodies(self):
        container = ctk.CTkFrame(self, fg_color=T.BG, corner_radius=0)
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        builders = {
            "Media Info":      self._build_media_info,
            "Encode Settings": self._build_encode_settings,
            "Tracks":          self._build_tracks,
            "Output":          self._build_output,
        }
        for name, builder in builders.items():
            scroll = ctk.CTkScrollableFrame(
                container, fg_color=T.BG, corner_radius=0,
                scrollbar_button_color=T.BORDER,
                scrollbar_button_hover_color=T.TEXT3,
            )
            scroll.grid(row=0, column=0, sticky="nsew")
            scroll.grid_columnconfigure(0, weight=1)
            builder(scroll)
            self._tab_frames[name] = scroll

    # ── Shared helpers ────────────────────────────────────────────────────────

    def _card(self, parent, title: str, row: int) -> ctk.CTkFrame:
        """Create a titled card and return its body frame."""
        card = ctk.CTkFrame(parent, fg_color=T.PANEL, corner_radius=T.RADIUS,
                            border_width=1, border_color=T.BORDER2)
        card.grid(row=row, column=0, sticky="ew", padx=14, pady=(0, 10))
        card.grid_columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(card, fg_color=T.SURFACE, corner_radius=0, height=32)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(hdr, text=title,
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=T.TEXT2, anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=12, pady=0)

        body = ctk.CTkFrame(card, fg_color="transparent", corner_radius=0)
        body.grid(row=1, column=0, sticky="ew", padx=12, pady=10)
        body.grid_columnconfigure((0, 1), weight=1)
        return body

    def _info_field(self, parent, row: int, col: int,
                    label: str, value: str, tip: str):
        """One label+value+tooltip cell in the info grid."""
        cell = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=0)
        cell.grid(row=row, column=col, sticky="nw", padx=(0, 16), pady=5)

        lbl_row = ctk.CTkFrame(cell, fg_color="transparent", corner_radius=0)
        lbl_row.pack(anchor="w")
        ctk.CTkLabel(lbl_row,
                     text=label.upper(),
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=T.TEXT3,
        ).pack(side="left")
        Tooltip(lbl_row, tip).pack(side="left", padx=(4, 0))

        ctk.CTkLabel(cell, text=value,
                     font=ctk.CTkFont(size=12, family="Courier New"),
                     text_color=T.TEXT, anchor="w",
        ).pack(anchor="w", pady=(2, 0))

    def _setting_row(self, parent, row: int,
                     label: str, tip: str, control: ctk.CTkBaseClass):
        """One setting row: label+tooltip on left, control on right."""
        fr = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=0)
        fr.grid(row=row, column=0, sticky="ew", pady=4)
        fr.grid_columnconfigure(0, weight=1)

        left = ctk.CTkFrame(fr, fg_color="transparent", corner_radius=0)
        left.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(left, text=label,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=T.TEXT,
        ).pack(side="left")
        Tooltip(left, tip).pack(side="left", padx=(6, 0))

        control.grid(row=0, column=1, sticky="e", padx=(8, 0))

    def _make_option(self, parent, values: list, default: str = None) -> ctk.CTkOptionMenu:
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

    def _make_toggle(self, parent, default: bool = False) -> ctk.CTkSwitch:
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

    # ── Queue change ──────────────────────────────────────────────────────────

    def _on_queue_change(self):
        # Future: refresh media info when selected file changes
        pass

    # ── Media Info tab ────────────────────────────────────────────────────────

    def _build_media_info(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        # Empty state shown when no file selected
        self._info_empty = ctk.CTkLabel(
            parent,
            text="Select a file from the queue to inspect it",
            font=ctk.CTkFont(size=13),
            text_color=T.TEXT3,
        )
        self._info_empty.grid(row=0, column=0, pady=60)

        # Video card
        vbody = self._card(parent, "VIDEO STREAM", row=1)
        fields = [
            ("Codec",       "—",  "The compression standard used for the video. H.265/HEVC is modern and efficient; H.264 is older but universally compatible."),
            ("Resolution",  "—",  "The pixel dimensions of the video frame. 3840×2160 is 4K UHD — four times the detail of 1080p."),
            ("Frame Rate",  "—",  "How many individual frames are shown per second. 23.976 fps is the standard cinematic rate used in most films."),
            ("Bit Rate",    "—",  "Data used per second of video. Higher = better quality and larger file. 42 Mbps is typical for a 4K Blu-ray."),
            ("Bit Depth",   "—",  "Shades per colour channel. 10-bit (1,024 shades) enables HDR and smoother gradients vs 8-bit (256 shades)."),
            ("Colour Space","—",  "The gamut of colours the video can represent. BT.2020 is the wide HDR gamut; BT.709 is standard HD."),
            ("HDR Format",  "—",  "High Dynamic Range flavour. HDR10 is the open baseline. Dolby Vision / HDR10+ add dynamic per-scene metadata."),
            ("Scan Type",   "—",  "Progressive = complete frames. Interlaced = alternating lines (older broadcast technique, can cause combing artefacts)."),
        ]
        for i, (lbl, val, tip) in enumerate(fields):
            self._info_field(vbody, i // 2, i % 2, lbl, val, tip)

        # Container card
        cbody = self._card(parent, "CONTAINER", row=2)
        cfields = [
            ("Format",    "—",  "The wrapper that holds all streams. MKV supports unlimited tracks and chapters. MP4 has the widest device compatibility."),
            ("Duration",  "—",  "Total playback length of the file."),
            ("File Size", "—",  "Total size on disk, including all audio, video, and subtitle streams."),
            ("Chapters",  "—",  "Named scene markers embedded in the file. Media players use these for chapter navigation."),
        ]
        for i, (lbl, val, tip) in enumerate(cfields):
            self._info_field(cbody, i // 2, i % 2, lbl, val, tip)

    # ── Encode Settings tab ───────────────────────────────────────────────────

    def _build_encode_settings(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        # Video encoder card
        vbody = self._card(parent, "VIDEO ENCODER", row=0)
        vbody.grid_columnconfigure(0, weight=1)

        codec_om = self._make_option(vbody, ["H.265 / HEVC", "H.264 / AVC", "AV1", "VP9"], "H.265 / HEVC")
        self._setting_row(vbody, 0, "Output Codec",
            "The format your output video will be compressed in. H.265 offers the best size-to-quality ratio for modern devices. AV1 is more efficient but much slower to encode.",
            codec_om)

        preset_om = self._make_option(vbody, ["ultrafast","veryfast","fast","medium","slow","veryslow"], "medium")
        self._setting_row(vbody, 1, "Encoder Preset",
            "Speed vs compression trade-off. Slower presets take longer but produce smaller, better-quality files at the same CRF value. Medium is a sensible default.",
            preset_om)

        rc_om = self._make_option(vbody, ["CRF (Quality)", "ABR (Bitrate)", "2-Pass ABR"], "CRF (Quality)")
        self._setting_row(vbody, 2, "Rate Control",
            "CRF targets consistent visual quality throughout the video and lets file size vary. ABR targets a fixed average bitrate instead. 2-Pass ABR is most accurate for size-constrained encodes.",
            rc_om)

        # CRF slider row (custom — not using _setting_row because it has a live readout)
        crf_fr = ctk.CTkFrame(vbody, fg_color="transparent", corner_radius=0)
        crf_fr.grid(row=3, column=0, sticky="ew", pady=4)
        crf_fr.grid_columnconfigure(0, weight=1)

        crf_left = ctk.CTkFrame(crf_fr, fg_color="transparent", corner_radius=0)
        crf_left.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(crf_left, text="CRF Value",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=T.TEXT).pack(side="left")
        Tooltip(crf_left,
            "Quality level for CRF mode. Lower = better quality, larger file. For H.265: 0 is lossless, 28 is the default, 51 is worst. Values 18–24 are visually near-transparent."
        ).pack(side="left", padx=(6, 0))

        crf_right = ctk.CTkFrame(crf_fr, fg_color="transparent", corner_radius=0)
        crf_right.grid(row=0, column=1, sticky="e")
        self._crf_val = ctk.CTkLabel(crf_right, text="22",
                                     font=ctk.CTkFont(size=11, family="Courier New"),
                                     text_color=T.ACCENT_H, width=28)
        self._crf_val.pack(side="right")
        crf_slider = ctk.CTkSlider(
            crf_right, from_=0, to=51, number_of_steps=51,
            width=140, progress_color=T.ACCENT,
            button_color=T.ACCENT, button_hover_color=T.ACCENT_H,
            fg_color=T.SURFACE2,
            command=lambda v: self._crf_val.configure(text=str(int(v))),
        )
        crf_slider.set(22)
        crf_slider.pack(side="right", padx=(0, 8))

        hw_sw = self._make_toggle(vbody, default=False)
        self._setting_row(vbody, 4, "Hardware Acceleration",
            "Uses your GPU (NVENC, VideoToolbox, QSV) to encode instead of the CPU. Much faster, but output quality is usually slightly lower at the same settings.",
            hw_sw)

        # Resolution card
        rbody = self._card(parent, "RESOLUTION & FRAME RATE", row=1)
        rbody.grid_columnconfigure(0, weight=1)

        res_om = self._make_option(rbody, ["Match Source", "3840×2160 (4K)", "1920×1080 (FHD)", "1280×720 (HD)", "Custom…"], "Match Source")
        self._setting_row(rbody, 0, "Output Resolution",
            "Pixel dimensions of the output. 'Match Source' keeps the original. Downscaling from 4K to 1080p dramatically reduces file size with minimal visible quality loss at normal viewing distances.",
            res_om)

        fps_om = self._make_option(rbody, ["Match Source", "23.976", "24", "25", "29.97", "30", "50", "59.94", "60"], "Match Source")
        self._setting_row(rbody, 1, "Frame Rate",
            "Frames per second of the output. 'Match Source' is almost always correct. Changing this can introduce motion judder or duplicated frames if done incorrectly.",
            fps_om)

    # ── Tracks tab ────────────────────────────────────────────────────────────

    def _build_tracks(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        # Audio
        abody = self._card(parent, "AUDIO TRACKS", row=0)
        abody.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(abody,
            text="Add files to the queue to see available audio tracks.",
            font=ctk.CTkFont(size=11), text_color=T.TEXT3,
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        # Subtitle
        sbody = self._card(parent, "SUBTITLE TRACKS", row=1)
        sbody.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(sbody,
            text="Add files to the queue to see available subtitle tracks.",
            font=ctk.CTkFont(size=11), text_color=T.TEXT3,
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

    # ── Output tab ────────────────────────────────────────────────────────────

    def _build_output(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        obody = self._card(parent, "OUTPUT DESTINATION", row=0)
        obody.grid_columnconfigure(0, weight=1)

        dest_om = self._make_option(obody, ["Same folder as source", "Custom folder…"], "Same folder as source")
        self._setting_row(obody, 0, "Output Folder",
            "Where converted files are saved. 'Same folder as source' places them next to the originals. Choose 'Custom folder' to send everything to one place.",
            dest_om)

        fmt_om = self._make_option(obody, ["MKV", "MP4", "WebM"], "MKV")
        self._setting_row(obody, 1, "Container Format",
            "The wrapper format for your output file. MKV supports the most tracks and features. MP4 is the most compatible with TVs, phones, and media players. WebM is for web use.",
            fmt_om)

        naming_om = self._make_option(obody, ["{name}_{codec}", "{name}_{res}", "{name}_converted", "Custom…"], "{name}_{codec}")
        self._setting_row(obody, 2, "File Naming Pattern",
            "Template for output filenames. Variables are replaced automatically: {name} = original name, {codec} = output codec, {res} = resolution. E.g. 'movie_{codec}' → 'movie_h265.mkv'.",
            naming_om)

        overwrite_sw = self._make_toggle(obody, default=False)
        self._setting_row(obody, 3, "Overwrite Existing Files",
            "If a file with the same name already exists at the destination, overwrite it. When off, Forge will append a number to avoid collision.",
            overwrite_sw)
