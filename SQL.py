import sqlite3
from tkinter import *
cursor = ''
con = ''

def create_db():
    #TO DO: make DateTimes NOT NULL
    #currently not set to NOT NULL because I don't know how to insert a DateTime :>
    
    global con
    global cursor
    con = sqlite3.connect("Hotel.db")
    cursor = con.cursor()
    cursor.executescript(
        '''
        CREATE TABLE IF NOT EXISTS Guest(
            guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
            password TEXT NOT NULL
            );

        CREATE TABLE IF NOT EXISTS Room(
            room_number INTEGER PRIMARY KEY NOT NULL,
            type TEXT NOT NULL,
            price DOUBLE(8,2) NOT NULL
            );
        
        CREATE TABLE IF NOT EXISTS Booking(
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_id INTEGER NOT NULL,
            room_number INTEGER NOT NULL,
            check_in_date DATETIME,
            check_out_date DATETIME,
            FOREIGN KEY(guest_id) REFERENCES Guest(guest_id),
            FOREIGN KEY(room_number) REFERENCES Room(room_id)
            );




    CREATE TABLE IF NOT EXISTS Payment(
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            payment_method TEXT NOT NULL,
            credit_card_number TEXT,
            total_cost DOUBLE(8,2) NOT NULL
            );
    CREATE TABLE IF NOT EXISTS Service(
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            service_staff_id INTEGER,
            request TEXT NOT NULL,
            request_cost DOUBLE(8,2),
            request_datetime DATETIME,
            FOREIGN KEY(booking_id) REFERENCES Booking(booking_id)
            );
    CREATE TABLE IF NOT EXISTS Staff(
            staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
            );
    CREATE TABLE IF NOT EXISTS ServiceStaff(
            servicestaff_id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            filled_datetime DATETIME,
            FOREIGN KEY(staff_id) REFERENCES Staff(staff_id),
            FOREIGN KEY(service_id) REFERENCES Service(service_id)
            );
    

    
        
        '''
        )
    con.commit()

#### Inserts #### 
def insert_guest(valueList):
    cursor.execute(
        "INSERT INTO Guest(name, phone_number, email, password) VALUES (?, ?, ?,?)",
        (valueList[0], valueList[1], valueList[2],valueList[3])
    )
def insert_room(valueList):
    cursor.execute(
        "INSERT INTO Room(room_number, type, price) VALUES (?, ?, ?)",
        (valueList[0], valueList[1], valueList[2])
    )
    con.commit()  
def insert_booking(valueList):
    cursor.execute(
        "INSERT INTO Booking(guest_id, room_number) VALUES (?, ?)",
        (valueList[0], valueList[1])
    )    
    con.commit()



    
def insert_payment(valueList):
    cursor.execute(
        "INSERT INTO Payment(booking_id, payment_method, total_cost) VALUES (?, ?, ?)",
        (valueList[0], valueList[1], valueList[2])
    )
def insert_service(valueList):
    cursor.execute(
        "INSERT INTO Service(booking_id, request) VALUES (?, ?)",
        (valueList[0], valueList[1])
    )
    con.commit()  
def insert_staff(valueList):
    cursor.execute(
        "INSERT INTO Staff(name, email, password) VALUES (?, ?, ?)",
        (valueList[0], valueList[1],valueList[2])
    )
    con.commit()
def insert_servicestaff(valueList):
    cursor.execute(
        "INSERT INTO ServiceStaff(staff_id, service_id) VALUES (?, ?)",
        (valueList[0], valueList[1])
    )
    con.commit()


#### Select alls ####
def select_all_guest():
    cursor.execute("SELECT * FROM Guest")
    print("Guest:", cursor.fetchall())
def select_all_room():
    cursor.execute("SELECT * FROM Room")
    print("Room:",cursor.fetchall())
def select_all_booking():
    cursor.execute("SELECT * FROM Booking")
    print("Booking:",cursor.fetchall())
def select_all_payment():
    cursor.execute("SELECT * FROM Payment")
    print("Payment:",cursor.fetchall())
def select_all_service():
    cursor.execute("SELECT * FROM Service")
    print("Service:", cursor.fetchall())
def select_all_staff():
    cursor.execute("SELECT * FROM Staff")
    print("Staff:",cursor.fetchall())
def select_all_servicestaff():
    cursor.execute("SELECT * FROM ServiceStaff")
    print("ServiceStaff:",cursor.fetchall())



def drop_tables():
    cursor.executescript('''
        DROP TABLE Guest;
        DROP TABLE Room;
        DROP TABLE Booking;
        DROP TABLE Payment;
        DROP TABLE Service;
        DROP TABLE Staff;
        DROP TABLE ServiceStaff
        ''')
    con.commit()
 
if __name__ == "__main__":
    create_db()
    select_all_guest()
    select_all_room()
    select_all_booking()
    select_all_payment()
    select_all_service()
    select_all_staff()
    select_all_servicestaff()
    
    insert_guest(["GuestName","GuestNumber","GuestEmail","Password!"])
    insert_room([414,"RoomType",5.12])
    insert_booking([1,414])
    insert_payment([1,"Method",5.10])
    insert_service([1,"Request"])
    insert_staff(["StaffName", "StaffEmail", "StaffPass!"])
    insert_servicestaff([1,1])

    print("~~~~~~")
    
    select_all_guest()
    select_all_room()
    select_all_booking()
    select_all_payment()
    select_all_service()
    select_all_staff()
    select_all_servicestaff()
    
    drop_tables()
    
    con.close()
    
