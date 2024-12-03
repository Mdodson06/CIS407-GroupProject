import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Requires the Pillow library
import subprocess

# Hardcoded credentials
credentials = {
    "admin": "12345",
    "user1": "12345"
}

def authenticate():
    username = username_entry.get()
    password = password_entry.get()

    if username in credentials and credentials[username] == password:
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        if username == "admin":
            subprocess.run(["python", "admin.py"])
        else:
            subprocess.run(["python", "user.py"])
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Create the main Tkinter window
root = tk.Tk()
root.title("Login Page")
root.geometry("400x500")  # Adjusted for better layout

# Load and display the logo image
try:
    image = Image.open("norefundsinn.jpg")
    image = image.resize((200, 200), Image.LANCZOS)  # Resize the image
    logo = ImageTk.PhotoImage(image)
    logo_label = tk.Label(root, image=logo)
    logo_label.pack(pady=20)  # Add space above and below the logo
except FileNotFoundError:
    messagebox.showerror("Error", "Image file 'norefundsinn.jpg' not found.")

# Username label and entry
username_label = tk.Label(root, text="Username:")
username_label.pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

# Password label and entry
password_label = tk.Label(root, text="Password:")
password_label.pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

# Login button
login_button = tk.Button(root, text="Login", command=authenticate)
login_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
