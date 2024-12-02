import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import SQL_connection as Backend 
import datetime as dt
def user_screen():
    guestID = 1
    name = "user1"
    contact = "user1@contact.com"
    password = "12345"
    print(Backend.get_booking())
    # Main window setup
    root = tk.Tk()
    root.title("User Dashboard")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    # Top frame: Greeting and logo
    top_frame = tk.Frame(root, bg="#f0f0f0")
    top_frame.pack(fill="x", padx=10, pady=(5, 0))

    greeting = tk.Label(top_frame, text="Hello, user1!", font=("Arial", 16), bg="#f0f0f0", anchor="w")
    greeting.pack(side="left", pady=(0, 5))

    # Top-right image
    try:
        image = Image.open("norefundsinn.jpg").resize((150, 150))  # Ensure image path is correct
        img = ImageTk.PhotoImage(image)
        img_label = tk.Label(top_frame, image=img, bg="#f0f0f0")
        img_label.image = img  # Keep a reference to avoid garbage collection
        img_label.pack(side="right", pady=(0, 5))
    except Exception as e:
        print(f"Error loading image: {e}")

    # Sidebar
    sidebar = tk.Frame(root, bg="#d0e7ff", width=200)
    sidebar.pack(side="left", fill="y")

    def show_popup(title, message):
        messagebox.showinfo(title, message)

    # Book Now pop-up window
    def book_now_popup():
        book_window = tk.Toplevel(root)
        book_window.title("Book Now")
        book_window.geometry("400x500")
        book_window.configure(bg="#f0f0f0")

        #Get room
        rooms = Backend.get_available_rooms()

        room_numbers = []
        for i in rooms:
            room_numbers.append(i[0])

        type_price = {}
        for i in rooms:
            type_price.update({i[1]:i[2]})

        # Room type label and combo box
        tk.Label(book_window, text="Select Room Type:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        room_types = ["Single", "Double", "Suite"]
        room_type_combobox = ttk.Combobox(book_window, values=room_types, state="readonly", width=20)
        room_type_combobox.pack(pady=10)

        # Room number label and dropdown
        tk.Label(book_window, text="Select Room Number:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        #room_numbers = ["101", "102", "103", "201", "202", "203"]
        room_number_combobox = ttk.Combobox(book_window, values=room_numbers, state="readonly", width=20)
        room_number_combobox.pack(pady=10)

        #Get check in
        tk.Label(book_window, text="Enter check-in date (YYYY-MM-DD):", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        checkin_entry = tk.Entry(book_window, font=("Arial", 12), width=25)
        checkin_entry.pack(pady=10)

        #Get check out
        tk.Label(book_window, text="Enter check-out date (YYYY-MM-DD):", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        checkout_entry = tk.Entry(book_window, font=("Arial", 12), width=25)
        checkout_entry.pack(pady=10)
            
        
        # Function to update the total based on selected room type
        def update_total(event):        
            room_type = room_type_combobox.get()
            total_price = type_price.get(room_type, 0)
            total_label.config(text=f"Total: ${total_price:.2f}")
            rooms = Backend.get_available_rooms(roomType=room_type)
            room_numbers = []
            for i in rooms:
                room_numbers.append(i[0])
            room_number_combobox.configure(values=room_numbers)

        # Bind the change in room type selection to update total
        room_type_combobox.bind("<<ComboboxSelected>>", update_total)

        # Book Now button and total display
        def book_room():
            flag = False
            checkin_date = ''
            checkout_date = ''
            try:
                checkin = checkin_entry.get().split("-")
                checkout = checkout_entry.get().split("-")
                print("split success")
                for i in range(3):
                    checkin[i] = int(checkin[i])
                    checkout[i] = int(checkout[i])
                print("checkin:",checkin)
                print("checkout:",checkout)
                checkin_date = dt.datetime(checkin[0],checkin[1],checkin[2])
                checkout_date = dt.datetime(checkout[0],checkout[1],checkout[2])
                flag = True
            except:
                messagebox.showerror("Error", "Please enter valid dates")
            
            room_type = room_type_combobox.get()
            room_number = room_number_combobox.get()
            bookingCheck = Backend.book_room(guestID, room_number, checkin_date, checkout_date)
            if flag and room_type and room_number and (bookingCheck == "Success"):
                total_price = type_price.get(room_type, 0)
                messagebox.showinfo("Booking Successful", f"Room {room_number} ({room_type}) booked successfully!")
            elif flag:
                messagebox.showerror("Error", "Please select an available room type and room number.")

        book_button = tk.Button(book_window, text="Book Now", font=("Arial", 12), command=book_room)
        book_button.pack(pady=20)

        # Total price label
        total_label = tk.Label(book_window, text="Total: $0", font=("Arial", 12), bg="#f0f0f0")
        total_label.pack(side="bottom", pady=10)

    # Services pop-up window
    def services_popup():
        services_window = tk.Toplevel(root)
        services_window.title("Request a Service")
        services_window.geometry("400x400")
        services_window.configure(bg="#f0f0f0")

        # Service type label and combo box
        tk.Label(services_window, text="Select Service:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        service_list = Backend.get_servicetype() #["Room Cleaning", "Food Delivery", "Maintenance"]
        services = []
        for i in service_list:
            services.append(i[1])
        service_combobox = ttk.Combobox(services_window, values=services, state="readonly", width=20)
        service_combobox.pack(pady=10)

        # Room number label and combo box
        tk.Label(services_window, text="Select Room Number:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        rooms = Backend.get_booking(guestName="user1")#TO DO: Backend.get_booking(guestID)
        print("user rooms:",rooms)
        room_numbers = []
        for i in rooms:
            room_numbers.append(i[2])
        print("user room_number:",room_numbers)
        #room_numbers = ["101", "102", "103", "201", "202", "203"]
        room_number_combobox = ttk.Combobox(services_window, values=room_numbers, state="readonly", width=20)
        room_number_combobox.pack(pady=10)

        # Request Service button
        def request_service():
            service = service_combobox.get()
            room_number = room_number_combobox.get()
            if service and room_number:
                Backend.request_service(Backend.get_bookingID(guestID,room_number)[0][0],Backend.get_servicetype(service)[0][0])
                print(Backend.get_unfilled_requests())
                messagebox.showinfo("Service Requested", f"Service '{service}' has been requested for room {room_number}.")
            else:
                messagebox.showerror("Error", "Please select a service and a room number.")

        request_button = tk.Button(services_window, text="Request Service", font=("Arial", 12), command=request_service)
        request_button.pack(pady=20)

    # Payments pop-up window
    def payments_popup():
        payment_window = tk.Toplevel(root)
        payment_window.title("Make Payment")
        payment_window.geometry("400x600")
        payment_window.configure(bg="#f0f0f0")

        # Credit Card Information
        tk.Label(payment_window, text="Enter room number:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        room_number_entry = tk.Entry(payment_window, font=("Arial", 12), width=25)
        room_number_entry.pack(pady=10)

        tk.Label(payment_window, text="Enter Card Number:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        card_number_entry = tk.Entry(payment_window, font=("Arial", 12), width=25)
        card_number_entry.pack(pady=10)

        tk.Label(payment_window, text="Enter Expiry Date (MM/YY):", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        expiry_entry = tk.Entry(payment_window, font=("Arial", 12), width=25)
        expiry_entry.pack(pady=10)

        tk.Label(payment_window, text="Enter CVV:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        cvv_entry = tk.Entry(payment_window, font=("Arial", 12), width=25, show="*")
        cvv_entry.pack(pady=10)

        tk.Label(payment_window, text="Enter amount you wish to pay:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        amt_entry = tk.Entry(payment_window, font=("Arial", 12), width=25)
        amt_entry.pack(pady=10)


        # Function to process payment
        def process_payment():
            room_number = room_number_entry.get()
            card_number = card_number_entry.get()
            expiry_date = expiry_entry.get()
            cvv = cvv_entry.get()
            amt = amt_entry.get()
            bookingID = ''
            try:
                room_number = int(room_number)
                bookingID = Backend.get_bookingID(guestID,room_number)[0][0]
                amt = int(amt)
            finally:
                # Simple validation for payment information (just checking if fields are filled)
                if bookingID and card_number and expiry_date and cvv and amt and isinstance(amt,int):
                    Backend.make_payment(bookingID=bookingID,amt=amt,payment_method="Credit card", card_number=card_number)
                    messagebox.showinfo("Payment Successful", "Your payment has been processed successfully!")
                else:
                    messagebox.showerror("Error", "Please fill in all payment details.")

        # Submit Payment button
        submit_button = tk.Button(payment_window, text="Submit Payment", font=("Arial", 12), command=process_payment)
        submit_button.pack(pady=20)

    # Buttons to show pop-ups
    buttons = [
        ("Book Now", book_now_popup),
        ("Services", services_popup),
        ("Payments", payments_popup)
    ]
    
    for text, command in buttons:
        tk.Button(sidebar, text=text, width=20, command=command).pack(pady=10)

    # Log Out button (no pop-up for this one)
    #NOTE: Kills the program entirely
    tk.Button(sidebar, text="Log Out", width=20, command=root.destroy,bg="red", fg="white").pack(side="bottom", pady=10)
    
    # Middle header
    center_frame = tk.Frame(root, bg="#f0f0f0")
    center_frame.place(relx=0.51, rely=0.2, anchor="n")
    
    tk.Label(center_frame, text="Reservations", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=(0, 50))
    bookings = Backend.get_booking(guestID)
    print(bookings)
    reservation_frame = tk.Frame(root)
    reservation_frame.place(relx=.55, rely=0.3, anchor="n")
    tk.Label(reservation_frame,text="Room number\tCheck-in\t\tCheck-out\t\tTotal Costs",font=("Arial",12,"underline"),bg="#f0f0f0").pack()
    for i in bookings:
        tempBooking = str(i[2])+'\t     '+i[3][:10]+'\t     '+i[4][:10]+'\t     '+f'{i[5]:.2f}\t'
        tk.Label(reservation_frame,text=tempBooking,font=("Arial",12),bg="#f0f0f0").pack()
    #Scrollbar for reservations
    '''
    
    scroll_bar = tk.Scrollbar(center_frame)
    scroll_bar.pack()
    reservation_scroll = tk.Listbox(center_frame,yscrollcommand = scroll_bar.set ) 

    for i in bookings:
        reservation_scroll.insert(tk.END, str(i)) 
    reservation_scroll.pack()
    scroll_bar.config( command = reservation_scroll.yview ) 
    '''
    
    # Bottom frame: Copyright
    bottom_frame = tk.Frame(root, bg="#f0f0f0")
    bottom_frame.pack(side="bottom", fill="x", pady=5)

    tk.Label(bottom_frame, text="© NoRefundsInn 2024", font=("Arial", 10), bg="#f0f0f0", anchor="e").pack(side="right", padx=10)

    root.mainloop()

if __name__ == "__main__":
    Backend.create_db()
    user_screen()
