import tkinter as tk
from PIL import Image, ImageTk

def admin_screen():
    # Main window setup
    root = tk.Tk()
    root.title("Admin Dashboard")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    # Top frame: Greeting and logo
    top_frame = tk.Frame(root, bg="#f0f0f0")
    top_frame.pack(fill="x", padx=10, pady=(5, 0))

    greeting = tk.Label(top_frame, text="Hello, admin!", font=("Arial", 16), bg="#f0f0f0", anchor="w")
    greeting.pack(side="left", pady=(0, 5))

    try:
        image = Image.open("norefundsinn.jpg").resize((150, 150))
        img = ImageTk.PhotoImage(image)
        img_label = tk.Label(top_frame, image=img, bg="#f0f0f0")
        img_label.image = img
        img_label.pack(side="right", pady=(0, 5))
    except Exception as e:
        print(f"Error loading image: {e}")

    # Sidebar
    sidebar = tk.Frame(root, bg="#d0e7ff", width=200)
    sidebar.pack(side="left", fill="y")

    buttons = [("Rooms", None), ("Services", None), ("Bookings", None)]
    for text, command in buttons:
        tk.Button(sidebar, text=text, width=20).pack(pady=10)

    tk.Button(sidebar, text="Log Out", width=20, bg="red", fg="white").pack(side="bottom", pady=10)

    # Middle headers
    center_frame = tk.Frame(root, bg="#f0f0f0")
    center_frame.place(relx=0.5, rely=0.2, anchor="n")  # Moved higher for Service Requests

    # Header: Service Requests
    tk.Label(center_frame, text="Service Requests", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=(0, 50))

    # Header: Booked Rooms (fixed position)
    tk.Label(center_frame, text="Booked Rooms", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=(150, 30))

    # Bottom frame: Copyright
    bottom_frame = tk.Frame(root, bg="#f0f0f0")
    bottom_frame.pack(side="bottom", fill="x", pady=5)

    tk.Label(bottom_frame, text="Copyright © NoRefundsInn 2024", font=("Arial", 10), bg="#f0f0f0", anchor="e").pack(side="right", padx=10)

    root.mainloop()

if __name__ == "__main__":
    admin_screen()
