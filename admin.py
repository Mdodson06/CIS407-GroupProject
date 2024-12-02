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

    def add_service_popup():
        # Services pop-up window
        services_window = tk.Toplevel(root)
        services_window.title("Add Service")
        services_window.geometry("400x200")
        services_window.configure(bg="#f0f0f0")

        # Label for instruction
        tk.Label(services_window, text="Add Service", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)

        # Text box to input the service
        service_entry = tk.Entry(services_window, width=30, font=("Arial", 12))
        service_entry.pack(pady=10)

        # Function to handle adding the service
        def add_service():
            service_name = service_entry.get().strip()
            if service_name:
                # Simulate saving the service to a data source
                messagebox.showinfo("Success", f"Service '{service_name}' has been added!")
                services_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter a service name.")

        # Button to confirm adding the service
        tk.Button(services_window, text="Add Service", font=("Arial", 12), command=add_service).pack(pady=20)

    def bookings_popup():
        # Bookings pop-up window
        bookings_window = tk.Toplevel(root)
        bookings_window.title("Bookings")
        bookings_window.geometry("400x300")
        bookings_window.configure(bg="#f0f0f0")

        # Label for instruction
        tk.Label(bookings_window, text="Guest Booking", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)

        # Frame for buttons
        button_frame = tk.Frame(bookings_window, bg="#f0f0f0")
        button_frame.pack(pady=10)

        def check_in_guest():
            # Check-in pop-up window
            check_in_window = tk.Toplevel(bookings_window)
            check_in_window.title("Check In Guest")
            check_in_window.geometry("400x200")
            check_in_window.configure(bg="#f0f0f0")

            tk.Label(check_in_window, text="Guest ID:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
            guest_id_entry = tk.Entry(check_in_window, width=30, font=("Arial", 12))
            guest_id_entry.pack(pady=5)

            tk.Label(check_in_window, text="Select Room:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
            rooms = ["101", "102", "103", "201", "202", "203"]  # Example room numbers
            room_combobox = ttk.Combobox(check_in_window, values=rooms, state="readonly", width=28)
            room_combobox.pack(pady=5)

            def confirm_check_in():
                guest_id = guest_id_entry.get().strip()
                room = room_combobox.get()
                if guest_id and room:
                    # Simulate check-in logic
                    messagebox.showinfo("Success", f"Guest {guest_id} checked into Room {room}.")
                    check_in_window.destroy()
                else:
                    messagebox.showerror("Error", "Please fill out all fields.")

            tk.Button(check_in_window, text="Confirm Check In", font=("Arial", 12), command=confirm_check_in).pack(pady=20)

        def check_out_guest():
            # Check-out pop-up window
            check_out_window = tk.Toplevel(bookings_window)
            check_out_window.title("Check Out Guest")
            check_out_window.geometry("400x200")
            check_out_window.configure(bg="#f0f0f0")

            tk.Label(check_out_window, text="Guest ID:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
            guest_id_entry = tk.Entry(check_out_window, width=30, font=("Arial", 12))
            guest_id_entry.pack(pady=5)

            tk.Label(check_out_window, text="Select Room:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
            rooms = ["101", "102", "103", "201", "202", "203"]  # Example room numbers
            room_combobox = ttk.Combobox(check_out_window, values=rooms, state="readonly", width=28)
            room_combobox.pack(pady=5)

            def confirm_check_out():
                guest_id = guest_id_entry.get().strip()
                room = room_combobox.get()
                if guest_id and room:
                    # Simulate check-out logic
                    messagebox.showinfo("Success", f"Guest {guest_id} checked out from Room {room}.")
                    check_out_window.destroy()
                else:
                    messagebox.showerror("Error", "Please fill out all fields.")

            tk.Button(check_out_window, text="Confirm Check Out", font=("Arial", 12), command=confirm_check_out).pack(pady=20)

        # Buttons for check-in and check-out
        tk.Button(button_frame, text="Check In", font=("Arial", 12), command=check_in_guest).pack(side="left", padx=10)
        tk.Button(button_frame, text="Check Out", font=("Arial", 12), command=check_out_guest).pack(side="left", padx=10)
    # Button to show the Rooms pop-up
    buttons = [("Rooms", show_rooms_popup), ("Services", add_service_popup), ("Bookings", bookings_popup)]
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

