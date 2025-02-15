import mysql.connector
from dotenv import load_dotenv
import os
from tkinter import messagebox

# Load database environment variables
dotenv_path = os.path.join(
    "C:/Users/Krypton/Desktop/projects/Biometric Attendance/config/.env"
)
load_dotenv(dotenv_path=dotenv_path)

# Global trial counter
trial_no = 0


# exit window after attempted login trials
def trial(window):
    global trial_no
    trial_no += 1
    print("Trial #", trial_no)

    if trial_no == 3:
        messagebox.showwarning("Warning!", "You have reached the login limit")
        window.destroy()


# error for not inputting username or password
def loginuser(username, password, window):
    if (
        username == ""
        or username == "UserID"
        or password == ""
        or password == "Password"
    ):
        messagebox.showerror("Entry error", "Type username or password")
        return

    try:
        # Connect to the database
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        mycursor = mydb.cursor()
        print("Connected to database")
    except:  # noqa: E722
        messagebox.showerror("Connection", "Database connection not connected")
        return

    command = "USE loginregistration"
    mycursor.execute(command)

    command = "SELECT * FROM login WHERE Username = %s AND Password = %s"
    mycursor.execute(command, (username, password))
    myresult = mycursor.fetchone()
    print(myresult)

    if myresult is None:
        messagebox.showinfo("Invalid", "Invalid UserID or Password")
        trial(window)
    else:
        messagebox.showinfo("Login", "Successfully Logged In")
        window.destroy()
