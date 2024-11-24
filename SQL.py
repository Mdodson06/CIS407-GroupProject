import sqlite3
from tkinter import *
cursor = ''
con = ''

def create_db():
    #TO DO: Finish CREATES, make DateTimes NOT NULL
    #currently not set to NOT NULL because I don't know how to insert a DateTime :>
    #Not tested past big space in executescript 
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
            check_in_date DATETIME ,
            check_out_date DATETIME 
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
            request_datetime DATETIME
            );
    CREATE TABLE IF NOT EXISTS Staff(
            staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
            );
    CREATE TABLE IF NOT EXISTS ServiceStaff(
            Servicestaff_id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER NOT NULL,
            service_id TEXT NOT NULL,
            filled_datetime DATETIME
            );
    

    
        
        '''
        )
    con.commit()
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
def select_all_guest():
    cursor.execute("SELECT * FROM Guest")
    print("Guest:", cursor.fetchall())
def select_all_room():
    cursor.execute("SELECT * FROM Room")
    print("Room:",cursor.fetchall())
def select_all_booking():
    cursor.execute("SELECT * FROM Booking")
    print("Booking:",cursor.fetchall())


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
    print("Hello World!")
    create_db()
    
    select_all_guest()
    insert_guest(["GuestName","GuestNumber","GuestEmail","Password!"])
    insert_room([414,"RoomType",5.12])
    insert_booking([1,414])
    select_all_guest()
    select_all_room()
    select_all_booking()
    drop_tables()
    
    con.close()
    
