"""Forge — Convert page (placeholder)"""
import customtkinter as ctk
from src.ui.pages.base import BasePage
from src.utils import theme as T


class ConvertPage(BasePage):

    def build(self):
        ctk.CTkLabel(
            self, text="Convert / Queue",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=T.TEXT2,
        ).place(relx=0.5, rely=0.5, anchor="center")

    def get_topbar(self):
        return ("Convert", "— batch re-encode media files", [])
