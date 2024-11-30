#login.py
import tkinter as tk
from tkinter import messagebox
import subprocess

# Hardcoded credentials
credentials = {
    "admin": "12345",
    "user1": "12345"
}

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username in credentials and credentials[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        if username == "admin":
            subprocess.run(["python", "admin.py"])
        else:
            subprocess.run(["python", "user.py"])
        root.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

# UI setup
root = tk.Tk()
root.title("Hotel Management System - Login")

# Labels and entries
tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Password").grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Login button
login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
