import tkinter as tk
from tkinter import ttk, messagebox
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

    def show_rooms_popup():
        # Rooms pop-up window
        rooms_window = tk.Toplevel(root)
        rooms_window.title("Edit Room Information")
        rooms_window.geometry("400x400")
        rooms_window.configure(bg="#f0f0f0")

        # Room selection dropdown
        tk.Label(rooms_window, text="Select Room:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        rooms = ["101", "102", "103", "201", "202", "203"]  # Example room numbers
        room_combobox = ttk.Combobox(rooms_window, values=rooms, state="readonly", width=20)
        room_combobox.pack(pady=10)

        # Room Type dropdown (updated)
        tk.Label(rooms_window, text="Room Type:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        room_types = ["Single", "Double", "Suite", "Penthouse"]  # Available room types
        room_type_combobox = ttk.Combobox(rooms_window, values=room_types, state="readonly", width=20)
        room_type_combobox.pack(pady=10)

        # Room Price field
        tk.Label(rooms_window, text="Room Price ($):", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        room_price_entry = tk.Entry(rooms_window, width=20)
        room_price_entry.pack(pady=10)

        # Function to load room details into the fields based on selected room
        def load_room_details():
            room_number = room_combobox.get()
            if room_number:
                # Simulate loading room details from a data source (e.g., database)
                if room_number == "101":
                    room_type_combobox.set("Single")
                    room_price_entry.delete(0, tk.END)
                    room_price_entry.insert(0, "100")
                elif room_number == "102":
                    room_type_combobox.set("Double")
                    room_price_entry.delete(0, tk.END)
                    room_price_entry.insert(0, "150")
                elif room_number == "103":
                    room_type_combobox.set("Suite")
                    room_price_entry.delete(0, tk.END)
                    room_price_entry.insert(0, "250")
                # Add similar conditions for other rooms...

        # Load room details when a room is selected
        room_combobox.bind("<<ComboboxSelected>>", lambda event: load_room_details())

        # Function to save updated room details
        def save_room_details():
            room_number = room_combobox.get()
            room_type = room_type_combobox.get()
            room_price = room_price_entry.get()

            if room_number and room_type and room_price:
                # Simulate saving the updated details to a data source (e.g., database)
                messagebox.showinfo("Success", f"Room {room_number} has been updated:\nType: {room_type}\nPrice: ${room_price}")
            else:
                messagebox.showerror("Error", "Please fill out all fields.")

        # Save button to save updated information
        save_button = tk.Button(rooms_window, text="Save Changes", font=("Arial", 12), command=save_room_details)
        save_button.pack(pady=20)

    # Button to show the Rooms pop-up
    buttons = [("Rooms", show_rooms_popup), ("Services", None), ("Bookings", None)]
    for text, command in buttons:
        tk.Button(sidebar, text=text, width=20, command=command).pack(pady=10)

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

    tk.Label(bottom_frame, text="© NoRefundsInn 2024", font=("Arial", 10), bg="#f0f0f0", anchor="e").pack(side="right", padx=10)

    root.mainloop()

if __name__ == "__main__":
    admin_screen()

