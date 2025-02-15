from pathlib import Path
from tkinter import *
import os
import sys

# Get the absolute path of the project root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Add project root to sys.path
sys.path.append(BASE_DIR)

from src.backend.login_service import (
    loginuser,
)  # Ensure this import works before building


class LoginGUI:
    def __init__(self):
        # Setup paths
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if getattr(sys, "frozen", False):  # If running as an EXE
            self.BASE_DIR = (
                sys._MEIPASS
            )  # Temporary folder where PyInstaller unpacks files
        self.ASSETS_PATH = Path(self.BASE_DIR) / Path(
            r"C:\Users\Krypton\Desktop\projects\Biometric Attendance\assets\frame0"
        )

        # Initialize Tkinter
        self.window = Tk()
        self.window.geometry("1440x800")
        self.window.title("Admin Login")
        self.window.resizable(False, False)
        self.window.configure(bg="#FFFFFF")

        # Create Canvas
        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=800,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(
            712.0, 0.0, 1440.0, 800.0, fill="#344865", outline=""
        )

        # Title Text
        self.canvas.create_text(
            880.0,
            146.0,
            anchor="nw",
            text="ADMIN LOGIN",
            fill="#FFFFFF",
            font=("InriaSans Bold", 64 * -1),
        )

        # Input Fields
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(1086.0, 342.0, image=self.entry_image_1)
        self.canvas.create_image(1086.0, 509.0, image=self.entry_image_2)

        # Username Field
        self.canvas.create_text(
            834.0,
            275.0,
            anchor="nw",
            text="Username",
            fill="#FFFFFF",
            font=("InriaSans Regular", 24 * -1),
        )
        self.entry_1 = Entry(
            self.window,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=("Calibri 25"),
            highlightthickness=0,
        )
        self.entry_1.place(x=834.0, y=313.0, width=504.0, height=56.0)
        self.entry_1.insert(0, "UserID")
        self.entry_1.bind("<FocusIn>", self.user_enter)
        self.entry_1.bind("<FocusOut>", self.user_leave)

        # Password Field
        self.canvas.create_text(
            834.0,
            444.0,
            anchor="nw",
            text="Password\n",
            fill="#FFFFFF",
            font=("InriaSans Regular", 24 * -1),
        )
        self.entry_2 = Entry(
            self.window,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=("Calibri 25"),
            highlightthickness=0,
        )
        self.entry_2.place(x=834.0, y=480.0, width=504.0, height=56.0)
        self.entry_2.insert(0, "Password")
        self.entry_2.bind("<FocusIn>", self.password_enter)
        self.entry_2.bind("<FocusOut>", self.password_leave)

        # Show/Hide Password
        self.button_mode = True
        self.showpass_img = PhotoImage(file=self.relative_to_assets("showpass.png"))
        self.hidepass_img = PhotoImage(file=self.relative_to_assets("hidepass.png"))
        self.showpass_btn = Button(
            self.window,
            image=self.showpass_img,
            bg="#ffffff",
            borderwidth=0,
            highlightthickness=0,
            command=self.toggle_password,
        )
        self.showpass_btn.place(x=1280.0, y=483.0)

        # Login Button
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.window,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_login,
            relief="flat",
        )
        self.button_1.place(x=902.0, y=654.0, width=344.0, height=102.0)

        # Hover effect
        self.button_image_hover_1 = PhotoImage(
            file=self.relative_to_assets("button_hover_1.png")
        )
        self.button_1.bind("<Enter>", self.button_1_hover)
        self.button_1.bind("<Leave>", self.button_1_leave)

        # Side Image
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(356.0, 400.0, image=self.image_image_1)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def user_enter(self, event):
        self.entry_1.delete(0, "end")

    def user_leave(self, event):
        if self.entry_1.get() == "":
            self.entry_1.insert(0, "UserID")

    def password_enter(self, event):
        self.entry_2.delete(0, "end")

    def password_leave(self, event):
        if self.entry_2.get() == "":
            self.entry_2.insert(0, "Password")

    def toggle_password(self):
        if self.button_mode:
            self.showpass_btn.config(image=self.hidepass_img, activebackground="white")
            self.entry_2.config(show="*")  # Hide password
        else:
            self.showpass_btn.config(image=self.showpass_img, activebackground="white")
            self.entry_2.config(show="")  # Show password
        self.button_mode = not self.button_mode

    def handle_login(self):
        username = self.entry_1.get()
        password = self.entry_2.get()
        loginuser(username, password, self.window)  # Call login function

    def button_1_hover(self, event):
        self.button_1.config(image=self.button_image_hover_1)

    def button_1_leave(self, event):
        self.button_1.config(image=self.button_image_1)

    def run(self):
        """Run the GUI main loop."""
        self.window.mainloop()


if __name__ == "__main__":
    gui = LoginGUI()
    gui.run()
