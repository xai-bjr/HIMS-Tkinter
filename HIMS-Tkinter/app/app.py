import tkinter as tk

from app.config import APP_NAME, BACKGROUND, initialize_app
from app.database.csv_manager import CSVManager
from app.ui.styles import configure_styles
from app.auth.login import LoginFrame
from app.auth.signup import SignupFrame, FirstRunSetupFrame
from app.ui.main_window import MainWindow


class HIMSApp:
    def __init__(self):
        initialize_app()
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry("1100x720")
        self.root.minsize(980, 650)
        self.root.configure(bg=BACKGROUND)
        configure_styles(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.current_frame = None
        self.show_login()

    def _clear(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = None

    def show_login(self):
        self._clear()
        if not CSVManager("accounts.csv").read():
            self.current_frame = FirstRunSetupFrame(self.root, self)
        else:
            self.current_frame = LoginFrame(self.root, self)
        self.current_frame.pack(fill="both", expand=True)

    def show_signup(self):
        self._clear()
        self.current_frame = SignupFrame(self.root, self)
        self.current_frame.pack(fill="both", expand=True)

    def login_success(self, account):
        self._clear()
        self.current_frame = MainWindow(self.root, self, account)
        self.current_frame.pack(fill="both", expand=True)

    def logout(self):
        self.show_login()

    def run(self):
        self.root.mainloop()
