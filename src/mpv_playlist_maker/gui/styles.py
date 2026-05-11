from tkinter import ttk
from .constants import (
    ACCENT_COLOR,
    BACKGROUND_COLOR,
    FOREGROUND_COLOR,
    SECONDARY_COLOR,
    CARD_COLOR,
)


def configure_style(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background=BACKGROUND_COLOR)
    style.configure("Card.TFrame", background=CARD_COLOR, relief="flat")
    style.configure("TLabel", background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR, font=("Segoe UI", 10))
    style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=FOREGROUND_COLOR)
    style.configure("SubHeader.TLabel", font=("Segoe UI", 10), foreground=SECONDARY_COLOR)
    style.configure("Section.TLabel", font=("Segoe UI", 11, "bold"), foreground=FOREGROUND_COLOR)
    style.configure("Label.TLabel", font=("Segoe UI", 10), foreground=FOREGROUND_COLOR)
    style.configure("Accent.TButton", foreground="#ffffff", background=ACCENT_COLOR, font=("Segoe UI", 10, "bold"), padding=10)
    style.map(
        "Accent.TButton",
        background=[("active", "#3f51b5")],
        foreground=[("disabled", "#d1d1d1")],
    )
    style.configure("Secondary.TButton", foreground=FOREGROUND_COLOR, background="#ffffff", font=("Segoe UI", 10, "bold"), padding=10)
    style.map("Secondary.TButton", background=[("active", "#e8eaf6")])
    style.configure("TCombobox", fieldbackground="#ffffff", background="#ffffff", foreground=FOREGROUND_COLOR, padding=8)
