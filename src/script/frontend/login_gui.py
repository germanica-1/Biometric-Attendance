from pathlib import Path
from tkinter import *
from functools import partial
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the script directory
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, "..", "..")))  # Adjust path to include `src`

from script.backend.login_service import loginuser  # Ensure this import works before building

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    r"C:\Users\Krypton\Desktop\projects\Biometric Attendance\assets\frame0"
)

# Correct asset path for PyInstaller
if getattr(sys, 'frozen', False):  # If running as an EXE
    BASE_DIR = sys._MEIPASS  # Temporary folder where PyInstaller unpacks files
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1440x800")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=800,
    width=1440,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvas.pack(fill="both", expand=True)

canvas.create_rectangle(712.0, 0.0, 1440.0, 800.0, fill="#344865", outline="")

canvas.create_text(
    880.0,
    146.0,
    anchor="nw",
    text="ADMIN LOGIN",
    fill="#FFFFFF",
    font=("InriaSans Bold", 64 * -1),
)


entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(1086.0, 342.0, image=entry_image_1)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(1086.0, 509.0, image=entry_image_2)

################ username&password


# function for deleting username placeholder
def user_enter(e):
    entry_1.delete(0, "end")


def user_leave(e):
    name = entry_1.get()
    if name == "":
        entry_1.insert(0, "UserID")


# User username entry
canvas.create_text(
    834.0,
    275.0,
    anchor="nw",
    text="Username",
    fill="#FFFFFF",
    font=("InriaSans Regular", 24 * -1),
)

entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    font=("Calibri 25"),
    highlightthickness=0,
)

entry_1.place(x=834.0, y=313.0, width=504.0, height=56.0)

# placeholder for username
entry_1.insert(0, "UserID")
entry_1.bind("<FocusIn>", user_enter)
entry_1.bind("<FocusOut>", user_leave)


# function for deleting password placeholder
def password_enter(e):
    entry_2.delete(0, "end")


def password_leave(e):
    name = entry_2.get()
    if name == "":
        entry_2.insert(0, "Password")


# User password entry
canvas.create_text(
    834.0,
    444.0,
    anchor="nw",
    text="Password\n",
    fill="#FFFFFF",
    font=("InriaSans Regular", 24 * -1),
)

entry_2 = Entry(
    bd=0, bg="#FFFFFF", fg="#000716", font=("Calibri 25"), highlightthickness=0
)

entry_2.place(x=834.0, y=480.0, width=504.0, height=56.0)

# placeholder for Password
entry_2.insert(0, "Password")
entry_2.bind("<FocusIn>", password_enter)
entry_2.bind("<FocusOut>", password_leave)


# Function to get the user inputs and call loginuser
def handle_login():
    username = entry_1.get()
    password = entry_2.get()
    loginuser(username, password, window)  # Pass the required arguments


################ username&password


################ show/hide password
button_mode = True


def toggle_password():
    global button_mode

    if button_mode:
        showpass_btn.config(image=hidepass_img, activebackground="white")
        entry_2.config(show="*")  # Hide password
        button_mode = False
    else:
        showpass_btn.config(image=showpass_img, activebackground="white")
        entry_2.config(show="")  # Show password
        button_mode = True


# Load Images
showpass_img = PhotoImage(file="assets/frame0/showpass.png")
hidepass_img = PhotoImage(file="assets/frame0/hidepass.png")

# Create Button for Show/Hide Password
showpass_btn = Button(
    window,
    image=showpass_img,
    bg="#ffffff",
    borderwidth=0,
    highlightthickness=0,
    command=toggle_password,
)
showpass_btn.place(x=1280.0, y=483.0)
################ show/hide password


button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=handle_login,
    relief="flat",
)

button_1.place(x=902.0, y=654.0, width=344.0, height=102.0)

button_image_hover_1 = PhotoImage(file=relative_to_assets("button_hover_1.png"))


def button_1_hover(e):
    button_1.config(image=button_image_hover_1)


def button_1_leave(e):
    button_1.config(image=button_image_1)


button_1.bind("<Enter>", button_1_hover)
button_1.bind("<Leave>", button_1_leave)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(356.0, 400.0, image=image_image_1)

if __name__ == "__main__":  # Run mainloop only when executed directly
    window.mainloop()

window.resizable(True, True)
