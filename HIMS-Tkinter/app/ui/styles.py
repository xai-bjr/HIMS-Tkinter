import tkinter as tk
from tkinter import ttk

from app.config import PRIMARY, PRIMARY_DARK, SUCCESS, DANGER, BACKGROUND, SIDEBAR, CARD, BORDER, TEXT, MUTED


def configure_styles(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(".", font=("Segoe UI", 10))
    style.configure("TFrame", background=BACKGROUND)
    style.configure("TLabel", background=BACKGROUND, foreground=TEXT)
    style.configure("TButton", padding=(11, 8))
    style.configure("Primary.TButton", background=PRIMARY, foreground="white", borderwidth=0)
    style.map("Primary.TButton", background=[("active", PRIMARY_DARK)])
    style.configure("Success.TButton", background=SUCCESS, foreground="white", borderwidth=0)
    style.configure("Danger.TButton", background=DANGER, foreground="white", borderwidth=0)
    style.configure("Sidebar.TFrame", background=SIDEBAR)
    style.configure("Sidebar.TLabel", background=SIDEBAR, foreground="white")
    style.configure("Sidebar.TButton", background=SIDEBAR, foreground="white", borderwidth=0, anchor="w", padding=(18, 10))
    style.map("Sidebar.TButton", background=[("active", "#1E293B")])
    style.configure("Auth.TFrame", background=CARD, relief="solid", borderwidth=1)
    style.configure("Card.TFrame", background=CARD, relief="solid", borderwidth=1)
    style.configure("CardTitle.TLabel", background=CARD, foreground=MUTED, font=("Segoe UI", 9, "bold"))
    style.configure("CardValue.TLabel", background=CARD, foreground=TEXT, font=("Segoe UI", 21, "bold"))
    style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground=TEXT)
    style.configure("SubHeader.TLabel", foreground=MUTED)
    style.configure("Treeview", rowheight=29, background="white", fieldbackground="white", foreground=TEXT, bordercolor=BORDER)
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), padding=8)
    style.map("Treeview", background=[("selected", "#DBEAFE")], foreground=[("selected", TEXT)])
