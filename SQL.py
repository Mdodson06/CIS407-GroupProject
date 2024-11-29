import sqlite3
from tkinter import *
from datetime import datetime
cursor = ''
con = ''
####Bug check for later: If a guest uses the same exact name, contact, and
    #password, will anything break? bc some calls to find stuff through that
    #Update: guest_signup checks if there would be a duplicate contact/pass;
    #if there would be, it returns -1 and refuses to INSERT the new one
    #Else, it INSERTs and returns "Success"
    #TO DO: Protect Staff in the same way?
####NOTE: Could improve payment?
    #BookingID just holds the 

def create_db():
    global con
    global cursor
    con = sqlite3.connect("Hotel.db")
    cursor = con.cursor()
    cursor.executescript(
        '''
        CREATE TABLE IF NOT EXISTS Guest(
            guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_info TEXT NOT NULL,
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
            check_in_date DATETIME NOT NULL,
            check_out_date DATETIME NOT NULL,
            total_cost DOUBLE(8,2) NOT NULL,            
            FOREIGN KEY(guest_id) REFERENCES Guest(guest_id),
            FOREIGN KEY(room_number) REFERENCES Room(room_id)
            );

    CREATE TABLE IF NOT EXISTS Payment(
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            payment_method TEXT,
            card_number TEXT,
            transaction_amount DOUBLE(8,2) NOT NULL,
            FOREIGN KEY (booking_id) REFERENCES Booking(booking_id)
            );
    CREATE TABLE IF NOT EXISTS ServiceType(
            servicetype_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            cost DOUBLE(8,2) NOT NULL
            );
    CREATE TABLE IF NOT EXISTS ServiceRequest(
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            servicetype_id INTEGER NOT NULL,
            requested_datetime DATETIME NOT NULL,
            FOREIGN KEY(booking_id) REFERENCES Booking(booking_id),
            FOREIGN KEY(servicetype_id) REFERENCES ServiceType(servicetype_id)
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
            filled_datetime DATETIME NOT NULL,
            FOREIGN KEY(staff_id) REFERENCES Staff(staff_id),
            FOREIGN KEY(service_id) REFERENCES Service(service_id)
            );   
        '''
        )
    con.commit()

#### Inserts ####
    ####Will be deleted once everything is done#### 
def insert_guest(valueList):
    cursor.execute(
        "INSERT INTO Guest(name, contact_info, password) VALUES (?,?,?)",
        valueList
    )
def insert_room(valueList):
    cursor.execute(
        "INSERT INTO Room(room_number, type, price) VALUES (?, ?, ?)",
        valueList
    )
    con.commit()  
def insert_booking(valueList):
    cursor.execute(
        "INSERT INTO Booking(guest_id, room_number,total_cost,check_in_date,check_out_date) VALUES (?, ?, ?, ?, ?)",
        valueList
    )    
    con.commit()
def insert_payment(valueList):
    cursor.execute(
        "INSERT INTO Payment(booking_id, payment_method, transaction_amount) VALUES (?, ?, ?)",
        valueList
    )
def insert_servicetype(valueList):
    cursor.execute(
        "INSERT INTO ServiceType(type,cost) VALUES (?,?)",
        valueList
    )
def insert_servicerequest(valueList):
    cursor.execute(
        "INSERT INTO ServiceRequest(booking_id,servicetype_id,requested_datetime) VALUES (?,?,?)",
        valueList
    )
    con.commit()  
def insert_staff(valueList):
    cursor.execute(
        "INSERT INTO Staff(name, email, password) VALUES (?, ?, ?)",
        valueList
    )
    con.commit()
def insert_servicestaff(valueList):
    cursor.execute(
        "INSERT INTO ServiceStaff(staff_id, service_id,filled_datetime) VALUES (?, ?,?)",
        valueList
    )
    con.commit()


#### Select alls ####
    ####Will be deleted once everything is done####
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
def select_all_servicetype():
    cursor.execute("SELECT * FROM ServiceType")
    print("ServiceType:", cursor.fetchall())
def select_all_servicerequest():
    cursor.execute("SELECT * FROM ServiceRequest")
    print("ServiceRequest:", cursor.fetchall())    
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
        DROP TABLE ServiceType;
        DROP TABLE ServiceRequest;
        DROP TABLE Staff;
        DROP TABLE ServiceStaff
        ''')
    con.commit()


#### Sign up and log ins ####
def staff_signup(name, email, password):
    query = "INSERT INTO Staff(name, email, password) VALUES (?, ?, ?)"
    queryNeeds = [name,email,password]
    cursor.execute(query,queryNeeds)
    con.commit()
    return

def staff_login(email,password):
    query = "SELECT staff_id FROM Staff WHERE email=? AND password=?"
    queryNeeds = [email,password]
    cursor.execute(query,queryNeeds)
    con.commit()
    return cursor.fetchall()    

def guest_signup(guestName, contact, password):
    duplicate_check = guest_login(contact, password)
    if (duplicate_check != []):
        return -1
    query = "INSERT INTO Guest(name, contact_info, password) VALUES (?, ?, ?)"
    queryNeeds = [guestName,contact,password]
    cursor.execute(query,queryNeeds)
    con.commit()
    return "Success"

def guest_login(contactInfo,password):
    query = "SELECT guest_id FROM Guest WHERE contact_info=? AND password=?"
    queryNeeds = [contactInfo,password]
    cursor.execute(query,queryNeeds)
    con.commit()
    return cursor.fetchall()

#### Booking process ####

def get_available_rooms(checkInDate, checkOutDate, cost=0,roomType="NA"):
    queryNeeds = [cost]
    query = "SELECT * FROM Room WHERE price=?"
    #Check if they have a requested room type
    if(roomType != "NA"):
        query += " AND type=?"
        queryNeeds.append(roomType)

    #Concatting the a subquery checking
        #if the room is available during that timeframe
    query += '''AND room_number NOT IN(
            SELECT room_number FROM Booking WHERE
            check_in_date BETWEEN ? AND ?
            OR check_out_date BETWEEN ? AND ?
        )'''
    queryNeeds.append(checkInDate)
    queryNeeds.append(checkOutDate)
    queryNeeds.append(checkInDate)
    queryNeeds.append(checkOutDate)
  
    cursor.execute(query, queryNeeds)
    con.commit()
    return cursor.fetchall()

#Gets all info from UI textboxes and does calls needed to INSERT into Guest and Booking
def book_room(guestName, guestContact, guestPassword, roomNumber, checkin, checkout):
    cursor.execute('''SELECT * FROM Booking WHERE
            room_number=? AND
            check_in_date BETWEEN ? AND ?
            OR check_out_date BETWEEN ? AND ?''',[roomNumber,checkin,checkout,checkin,checkout])
    con.commit()
    query = cursor.fetchall()
    #immediately exits if the room is already booked for those dates 
    if (query != []):
        return -1

    #run guest_signup and if it returns -1 there's a duplicate
    if (guest_signup(guestName, guestContact, guestPassword) == -1):
        return -1

    guestID = guest_login(guestContact, guestPassword)[0][0]
    cursor.execute("SELECT price FROM Room WHERE room_number=?",[roomNumber])
    con.commit()
    price = cursor.fetchall()[0][0]
    
    #Actual booking query
    cursor.execute('''INSERT INTO Booking(
        guest_id,room_number, check_in_date, check_out_date,total_cost)
        VALUES(?,?,?,?,?)''',[guestID,roomNumber,checkin,checkout,price])
    con.commit()
    return "Success"

#NOTE: Wait
#If you have a guestID and roomNumber
#The datetime doesn't matter?
#guestID unique for every booking
#maybe?
#Idk it's 2am 
def get_bookingID(guestID, roomNumber, datetimePt):
    query = '''SELECT * FROM Booking WHERE guest_id=? AND room_number=?
    AND check_in_date < ?
    AND check_out_date > ?
    '''
    queryNeeds = [guestID,roomNumber,datetimePt,datetimePt]
    cursor.execute(query,queryNeeds)
    con.commit()
    return cursor.fetchall()

#### Services #### 

#returns -1 if the guest does not have permission to request to the given room
#Uses current datetime to check if their Booking is still active
#So won't work for any dates that have passed or haven't come yet
def request_service(guestID, roomNumber, servicetype_id):
    query = "INSERT INTO ServiceRequest(booking_id, servicetype_id, requested_datetime) VALUES (?,?, ?)"
    queryNeeds = []
    bookingID = get_bookingID(guestID, roomNumber, datetime.now())
    if (bookingID == []):
        return -1
    #Because tied to guestID won't return multiple
    else:
        bookingID = bookingID[0][0]
    queryNeeds.append(bookingID)
    queryNeeds.append(servicetype_id)
    queryNeeds.append(datetime.now())

    cursor.execute(query,queryNeeds)
    con.commit()
    return

#TO DO: join servicetype so the actual text is given 
def get_unfilled_requests():
    #fix serviceQuery to WHERE NOT EXISTS later
    serviceQuery = '''
SELECT ServiceRequest.servicerequest_id, Guest.name,
    Booking.room_number, ServiceRequest.servicetype_id,
    ServiceRequest.requested_datetime
FROM Service
INNER JOIN Booking
    ON ServiceRequest.booking_id = Booking.booking_id
INNER JOIN Guest
    ON Booking.guest_id = Guest.guest_id
WHERE servicerequest_id NOT IN (SELECT servicerequest_id FROM ServiceStaff)'''
    cursor.execute(serviceQuery)
    return cursor.fetchall()

#assumes staffID and serviceID already known
#if staff logged in and they're checking off an item that was
#found with get_unfilled_requests(), should be 
#Also uses current datetime
def fill_service(staffID, servicerequestID):
    query = "INSERT INTO ServiceStaff(staff_id, servicerequest_id, filled_datetime) VALUES (?, ?, ?)"
    queryNeeds = [staffID, servicerequestID, datetime.now()]
    cursor.execute(query,queryNeeds)
    con.commit()

    query = "SELECT servicetype_id FROM ServiceRequest WHERE servicerequest_id=?"
    

    
    query = '''UPDATE Booking SET total_cost=total_cost+(
        SELECT cost FROM ServiceType
        WHERE EXISTS (
            SELECT servicetype_id FROM ServiceRequest
            WHERE servicerequest_id=?"
            )
        )'''
    queryNeeds = [cost, servicerequestID]
    cursor.execute(query,queryNeeds)
    con.commit()
    
#### Staff searches #### 
def get_guest(guestName,contactInfo="NA"):
    query = '''SELECT guest_id,name,contact_info FROM Guest WHERE name=?'''
    queryNeeds = [guestName]
    
    #check for any fields being filled for the search    
    if contactInfo != "NA":
        query += "AND contact_info=?"
        queryNeeds.append(contactInfo)
    cursor.execute(query,queryNeeds)
    con.commit()
    return cursor.fetchall()

def get_booking(guestName="NA",roomNumber="NA",checkin="NA",checkout="NA"):
    query = "SELECT * FROM Booking"
    queryNeeds = []
    queryFlag = False #makes sure "WHERE" and "AND" are correct in query
    guestNameMultiple = False
    if(guestName != "NA"):
        subquery = get_guest(guestName)
        if(len(subquery) == 0): #no need to continue if no guests under that name
           return []
        query += " WHERE (guest_id=?"
        queryNeeds.append(subquery[0][0])
        
        #allows for printing of guests with the same name
        for g in range(1, len(subquery)):
            query += " OR guest_id=?"
            queryNeeds.append(subquery[g][0])
        query +=")"
        queryFlag = True
    if(roomNumber != "NA"):
        if(queryFlag == False):
            query += " WHERE room_number=?"
            queryFlag = True
        else:
            query += " AND room_number=?"
        queryNeeds.append(roomNumber)
    if(checkin != "NA"):
        if(queryFlag == False):
            query += " WHERE check_in_date=?"
            queryFlag = True
        else:
            query += " AND check_in_date=?"
        queryNeeds.append(checkin)
    if(checkout != "NA"):
        if(queryFlag == False):
            query += " WHERE check_out_date=?"
            queryFlag = True
        else:
            query += " AND check_out_date=?"
        queryNeeds.append(checkout)

    print("Query:",query)
    print("QueryNeeds:",queryNeeds)

    cursor.execute(query,queryNeeds)
    con.commit()
    return cursor.fetchall()

#Assumes they've logged in already so guest_id obtained
#Uses current datetime to find if they're currently booked
def make_payment(guest_id, room_number, amt, payment_method="",card_number=""):
    #NOTE: do we need to make sure the date is within?
    #booking = get_bookingID(guest_id, room_number, datetime.now())
    query = "SELECT * FROM Booking WHERE guest_id=? AND room_number=?"
    queryNeeds = [guest_id,room_number]
    cursor.execute(query,queryNeeds)
    con.commit()
    booking = cursor.fetchall()

    
    if (booking == []):
        return -1
    #shouldn't be any duplicate bookings?

    #Update the total_cost in Booking
    bookingID = booking[0][0]
    query = "UPDATE Booking SET total_cost=total_cost-? WHERE booking_id=?"
    queryNeeds = [amt,bookingID]
    cursor.execute(query,queryNeeds)
    con.commit()

    #INSERT into Payment to log the transaction
    query = "INSERT INTO Payment (booking_id, transaction_amount"
    values = "VALUES(?,?"
    queryNeeds = [bookingID,amt]
    if(payment_method!=""):
        query+=", payment_method"
        values += ",?"
        queryNeeds.append(payment_method)
    if(card_number != ""):
       query+=", card_number"
       values += ",?"
       queryNeeds.append(card_number)
    query += ")" + values + ")"

    cursor.execute(query,queryNeeds)
    con.commit()

#### Check in/out ####
#NOTE: Assumes we've gotten booking_id already
def check_in(booking_id):
    query = "UPDATE Booking SET check_in_date=? WHERE booking_id=?"
    queryNeeds = [datetime.now(),booking_id]

    cursor.execute(query,queryNeeds)
    con.commit()


#NOTE: Assumes we've gotten booking_id already
def check_out(booking_id):
    query = "UPDATE Booking SET check_out_date=? WHERE booking_id=?"
    queryNeeds = [datetime.now(),booking_id]

    cursor.execute(query,queryNeeds)
    con.commit()





#Discuss tomorrow:

#Last minute TO DOs:
    #TO DO: Check in/out process? 
        #If we do want to include it explicitly, only way I can think to do it
        #is to include in Booking "real_in_date" and "real_out_date"
        #When guest comes their ID is found and the staff is able to
        #Hit a button to check them in
        #The current datetime is collected and Booking is updated
        #Same with checkout 
    #TO DO: Check out process? -- check TotalCost, delete from booking?

if __name__ == "__main__":
    
    create_db()
    drop_tables()
    create_db()
    
    '''select_all_guest()
    select_all_room()
    select_all_booking()
    select_all_payment()
    select_all_service()
    select_all_staff()
    select_all_servicestaff()
    '''
    insert_guest(["GuestName","GuestNumber","Password!"])
    insert_room([414,"RoomType",5.12])
    insert_booking([1,414,5.55,"1962-04-30 12:00:00 am","2222-04-30 12:00:00 pm"])
    insert_payment([1,"Method",5.10])
    insert_servicetype(["RequestType",4.50])
    insert_servicerequest([1,1,datetime.now()])
    insert_staff(["StaffName", "StaffEmail", "StaffPass!"])
    #insert_servicestaff([1,1,"2023-02-14 12:00:00 am"])
    
    print("~~~~~~")
    
    select_all_guest()
    select_all_room()
    select_all_booking()
    select_all_payment()
    select_all_servicetype()
    select_all_servicerequest()
    select_all_staff()
    select_all_servicestaff()
    print("~~~~~~")
    '''
    available_rooms = get_available_rooms(checkInDate="1962-04-20 12:00:00 pm",checkOutDate="1962-04-31 12:00:00 am",cost=5.12)
    print("Rooms available (Before but overlaps reserved):", available_rooms)
    available_rooms = get_available_rooms(checkInDate="1963-04-30 12:00:00 pm",checkOutDate="1969-04-29 12:00:00 am",cost=5.12)
    print("Rooms available(After but overlaps reserved):", available_rooms)
    available_rooms = get_available_rooms(checkInDate="1963-04-30 12:00:10 pm",checkOutDate="1969-04-29 12:00:00 am",cost=5.12)
    print("Rooms available (no overlap):", available_rooms)

    print("~~~~~~")
    
    print(get_bookingID(2,414))
    print("~~~~~~")
    
    request_service(1,414, "Request")

    select_all_service()
    print("~~~~~~")
    print(get_unfilled_requests())
    fill_service(1,1)
    print("~~~~~~")
    print(get_unfilled_requests())
    '''
    #insert_guest(["GuestName","22222","pst!"])

    #insert_room([111,"RoomType",5.12])
    '''#insert_booking([2,111,5.55,"1962-04-30 12:00:00 am","1963-04-30 12:00:00 pm"])
    #print(get_booking(guestName = "GuestName", roomNumber = 414))

    #print("Staff Signup:",staff_signup("Staff_","Email","Pass!"))
    #print("Staff Signup:",staff_signup("Staff2Name","eeeeemaillll","verySecurePass"))
    #print("Staff Login:",staff_login("eeeeemaillll","verySecurePassOOPS"))
    #print("Staff Login:",staff_login("eeeeemaillll","verySecurePass"))

    #print(book_room("GuestName","GuestContact","Password!",111, "2024-04-15 12:00:00 am", "2025-04-15 12:00:00 am"))
    #print(book_room("GuestName","GuestContact","Password!",111, "2026-04-15 12:00:00 am", "2027-04-15 12:00:00 am"))
    select_all_booking()
    select_all_service()
    select_all_servicestaff()
    print("~~~~")
    request_service(1,414, "sdsdfsdfsdfsdf")
    select_all_service()
    print(get_unfilled_requests())
    print("~~~~")
    fill_service(1,2,5000.13)
    select_all_booking()
    select_all_servicestaff()
    print("~~~~")
    make_payment(1, 414, 78)
    select_all_booking()

    check_in(1)
    
    select_all_booking()
    check_out(1)
    select_all_booking()
'''

    request_service(1,414,1)
    
    drop_tables()
    con.close()
    
