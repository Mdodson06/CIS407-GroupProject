import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os

def admin_screen():
    global root, booked_rooms_listbox, service_requests_listbox
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

    # Sidebar setup
    sidebar = tk.Frame(root, bg="#d0e7ff", width=200)
    sidebar.pack(side="left", fill="y")

    def log_out():
        confirm = messagebox.askyesno("Log Out", "Are you sure you want to log out?")
        if confirm:
            root.destroy()
            os.system("python login.py")

    def show_rooms_popup():
        rooms_window = tk.Toplevel(root)
        rooms_window.title("Edit Room Information")
        rooms_window.geometry("400x400")
        rooms_window.configure(bg="#f0f0f0")

        tk.Label(rooms_window, text="Select Room:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        rooms = ["101", "102", "103", "201", "202", "203"]
        room_combobox = ttk.Combobox(rooms_window, values=rooms, state="readonly", width=20)
        room_combobox.pack(pady=10)

        tk.Label(rooms_window, text="Room Type:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        room_types = ["Single", "Double", "Suite", "Penthouse"]
        room_type_combobox = ttk.Combobox(rooms_window, values=room_types, state="readonly", width=20)
        room_type_combobox.pack(pady=10)

        tk.Label(rooms_window, text="Room Price ($):", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        room_price_entry = tk.Entry(rooms_window, width=20)
        room_price_entry.pack(pady=10)

        def load_room_details():
            room_number = room_combobox.get()
            if room_number == "101":
                room_type_combobox.set("Single")
                room_price_entry.delete(0, tk.END)
                room_price_entry.insert(0, "100")
            elif room_number == "102":
                room_type_combobox.set("Double")
                room_price_entry.delete(0, tk.END)
                room_price_entry.insert(0, "150")

        room_combobox.bind("<<ComboboxSelected>>", lambda event: load_room_details())

        def save_room_details():
            room_number = room_combobox.get()
            room_type = room_type_combobox.get()
            room_price = room_price_entry.get()
            if room_number and room_type and room_price:
                messagebox.showinfo("Success", f"Room {room_number} updated:\nType: {room_type}\nPrice: ${room_price}")
            else:
                messagebox.showerror("Error", "Please fill out all fields.")

        tk.Button(rooms_window, text="Save Changes", font=("Arial", 12), command=save_room_details).pack(pady=20)

    def add_service_popup():
        services_window = tk.Toplevel(root)
        services_window.title("Add Service")
        services_window.geometry("400x200")
        services_window.configure(bg="#f0f0f0")

        tk.Label(services_window, text="Add Service", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        service_entry = tk.Entry(services_window, width=30, font=("Arial", 12))
        service_entry.pack(pady=10)

        def add_service():
            service_name = service_entry.get().strip()
            if service_name:
                messagebox.showinfo("Success", f"Service '{service_name}' added!")
                services_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter a service name.")

        tk.Button(services_window, text="Add Service", font=("Arial", 12), command=add_service).pack(pady=20)

    def bookings_popup():
        bookings_window = tk.Toplevel(root)
        bookings_window.title("Bookings")
        bookings_window.geometry("400x300")
        bookings_window.configure(bg="#f0f0f0")

        tk.Label(bookings_window, text="Guest Booking", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)

        button_frame = tk.Frame(bookings_window, bg="#f0f0f0")
        button_frame.pack(pady=10)

        def check_in_guest():
            check_in_window = tk.Toplevel(bookings_window)
            check_in_window.title("Check In Guest")
            check_in_window.geometry("400x200")
            check_in_window.configure(bg="#f0f0f0")

            tk.Label(check_in_window, text="Guest ID:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
            guest_id_entry = tk.Entry(check_in_window, width=30, font=("Arial", 12))
            guest_id_entry.pack(pady=5)

            tk.Label(check_in_window, text="Select Room:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
            rooms = ["101", "102", "103", "201", "202", "203"]
            room_combobox = ttk.Combobox(check_in_window, values=rooms, state="readonly", width=28)
            room_combobox.pack(pady=5)

            def confirm_check_in():
                guest_id = guest_id_entry.get().strip()
                room = room_combobox.get()
                if guest_id and room:
                    booked_rooms_listbox.insert(tk.END, f"Room {room} - Guest ID {guest_id}")
                    messagebox.showinfo("Success", f"Guest {guest_id} checked into Room {room}.")
                    check_in_window.destroy()
                else:
                    messagebox.showerror("Error", "Please fill out all fields.")

            tk.Button(check_in_window, text="Confirm Check In", font=("Arial", 12), command=confirm_check_in).pack(pady=20)

        def check_out_guest():
            check_out_window = tk.Toplevel(bookings_window)
            check_out_window.title("Check Out Guest")
            check_out_window.geometry("400x200")
            check_out_window.configure(bg="#f0f0f0")

            tk.Label(check_out_window, text="Guest ID:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
            guest_id_entry = tk.Entry(check_out_window, width=30, font=("Arial", 12))
            guest_id_entry.pack(pady=5)

            tk.Label(check_out_window, text="Select Room:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
            rooms = ["101", "102", "103", "201", "202", "203"]
            room_combobox = ttk.Combobox(check_out_window, values=rooms, state="readonly", width=28)
            room_combobox.pack(pady=5)

            def confirm_check_out():
                guest_id = guest_id_entry.get().strip()
                room = room_combobox.get()
                if guest_id and room:
                    items = booked_rooms_listbox.get(0, tk.END)
                    for i, item in enumerate(items):
                        if f"Room {room} - Guest ID {guest_id}" in item:
                            booked_rooms_listbox.delete(i)
                            break
                    messagebox.showinfo("Success", f"Guest {guest_id} checked out from Room {room}.")
                    check_out_window.destroy()
                else:
                    messagebox.showerror("Error", "Please fill out all fields.")

            tk.Button(check_out_window, text="Confirm Check Out", font=("Arial", 12), command=confirm_check_out).pack(pady=20)

        tk.Button(button_frame, text="Check In", font=("Arial", 12), command=check_in_guest).pack(side="left", padx=10)
        tk.Button(button_frame, text="Check Out", font=("Arial", 12), command=check_out_guest).pack(side="left", padx=10)

    def handle_service_request():
        selected_request = service_requests_listbox.curselection()
        if selected_request:
            service = service_requests_listbox.get(selected_request)
            admin_id = simpledialog.askstring("Assign Admin", "Enter Admin ID to handle this request:")
            if admin_id:
                service_requests_listbox.delete(selected_request)
                messagebox.showinfo("Success", f"Service request handled by Admin ID {admin_id}.")
            else:
                messagebox.showerror("Error", "Admin ID cannot be empty.")
        else:
            messagebox.showerror("Error", "Please select a service request.")

    # Sidebar buttons
    tk.Button(sidebar, text="Rooms", width=20, command=show_rooms_popup).pack(pady=10)
    tk.Button(sidebar, text="Services", width=20, command=add_service_popup).pack(pady=10)
    tk.Button(sidebar, text="Bookings", width=20, command=bookings_popup).pack(pady=10)
    tk.Button(sidebar, text="Log Out", width=20, bg="red", fg="white", command=log_out).pack(side="bottom", pady=10)

    # Center frame with headers and dynamic lists
    center_frame = tk.Frame(root, bg="#f0f0f0")
    center_frame.place(relx=0.5, rely=0.2, anchor="n")

    tk.Label(center_frame, text="Service Requests", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=(0, 5))
    service_requests_listbox = tk.Listbox(center_frame, width=50, height=5)
    service_requests_listbox.pack(pady=5)
    service_requests_listbox.insert(0, "Fix AC - Guest ID 001")
    service_requests_listbox.insert(1, "Clean Room 101 - Guest ID 002")
    service_requests_listbox.insert(2, "Room Service - Guest ID 003")
    service_requests_listbox.insert(3, "Repair TV - Guest ID 004")

    tk.Button(center_frame, text="Handle Selected Request", command=handle_service_request).pack(pady=10)

    tk.Label(center_frame, text="Booked Rooms", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=(10, 5))
    booked_rooms_listbox = tk.Listbox(center_frame, width=50, height=5)
    booked_rooms_listbox.pack(pady=5)

    # Bottom frame
    bottom_frame = tk.Frame(root, bg="#f0f0f0")
    bottom_frame.pack(side="bottom", fill="x", pady=5)
    tk.Label(bottom_frame, text="© NoRefundsInn 2024", font=("Arial", 10), bg="#f0f0f0", anchor="e").pack(side="right", padx=10)

    root.mainloop()

if __name__ == "__main__":
    admin_screen()
