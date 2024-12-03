import sqlite3
from tkinter import *
from datetime import datetime
cursor = ''
con = ''

##### Create and drop tables #####
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
            servicerequest_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            servicerequest_id INTEGER NOT NULL,
            filled_datetime DATETIME NOT NULL,
            FOREIGN KEY(staff_id) REFERENCES Staff(staff_id),
            FOREIGN KEY(servicerequest_id) REFERENCES ServiceRequest(serviceRequest_id)
            );   
        '''
        )
    con.commit()

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

##### Create/Update/Delete rooms and services #####
def insert_room(room_number, rtype, price):
    query = "INSERT INTO Room(room_number, type, price) VALUES (?, ?, ?)"
    queryNeeds = [room_number,rtype,price]
    cursor.execute(query,queryNeeds)
    con.commit()
    
def insert_servicetype(stype,cost):
    query = "INSERT INTO ServiceType(type,cost) VALUES (?,?)"
    queryNeeds = [stype,cost]
    cursor.execute(query,queryNeeds)
    con.commit()

def update_room(room_number, rtype="NA",cost=-1):
    #If they try to update nothing just ignore
    if(rtype == "NA" and cost == -1):
        return
    query = "UPDATE Room SET "
    queryNeeds = []
    if(rtype != "NA"):
        query+= "type=?"
        queryNeeds.append(rtype)
    if(cost != -1):
        if(len(queryNeeds) > 0):
            query+= ", "
        query+= "price=? "
        queryNeeds.append(cost)
    queryNeeds.append(room_number)
    query += "WHERE room_number=?"
    cursor.execute(query,queryNeeds)
    con.commit()
    return

def update_servicetype(servicetype_id, rtype="NA",cost=-1):
    if (rtype=="NA" and cost == -1):
        return
    query = "UPDATE ServiceType SET "
    queryNeeds = []
    if(rtype != "NA"):
        query+= "type=? "
        queryNeeds.append(rtype)
    if(cost != -1):
        if(len(queryNeeds) > 0):
            query+= ", "
        query+= "cost=? "
        queryNeeds.append(cost)
    queryNeeds.append(servicetype_id)
    query += " WHERE servicetype_id=?;"
    cursor.execute(query,queryNeeds)
    con.commit()
    return

def delete_room(room_number):
    query = "DELETE FROM Room WHERE room_number=?"
    queryNeeds = [room_number]
    cursor.execute(query,queryNeeds)
    con.commit()
    return

def delete_servicetype(servicetype_id):
    query = "DELETE FROM ServiceType WHERE servicetype_id=?"
    queryNeeds = [servicetype_id]
    cursor.execute(query,queryNeeds)
    con.commit()
    return

##### Searches #####

def get_all_staff():
    query = "SELECT * FROM Staff"
    cursor.execute(query)
    con.commit()
    return cursor.fetchall()

def get_available_rooms(room_number=-1,checkInDate="NA", checkOutDate="NA", cost=99999,roomType="NA"):
    query = "SELECT * FROM Room WHERE "
    queryNeeds = []
    #Lets booking use to make sure the room is truly free
    #NOTE: Does not have failsafe against not including a checkin/out, required in book_room
    if(room_number!=-1):
        query+= "room_number=? AND "
        queryNeeds.append(room_number)
    query+="price<=?"
    queryNeeds.append(cost)

    #Check if they have a requested room type 
    if(roomType != "NA"):
        query += " AND type=?"
        queryNeeds.append(roomType)

    #Shows everything if either check_in_date or check_out_date is left blank
    if(checkInDate != "NA" and checkOutDate != "NA"):
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
    check = cursor.fetchall()
    #print("Check:",check)
    return check

def get_servicetype(stype=-1):
    if(stype == -1):
        query = "SELECT * FROM ServiceType"
        cursor.execute(query)
        con.commit()
        return (cursor.fetchall())
    else:
        query = "SELECT servicetype_id FROM ServiceType WHERE type=?"
        queryNeeds = [stype]
        cursor.execute(query,queryNeeds)
        con.commit()
        return cursor.fetchall()
    

#11/27/24 NOTE: removed need to get the datetime
def get_bookingID(guestID, roomNumber):
    query = '''SELECT * FROM Booking WHERE guest_id=? AND room_number=?
    '''
    queryNeeds = [guestID,roomNumber]
    cursor.execute(query,queryNeeds)
    con.commit()
    return cursor.fetchall()

def get_unfilled_requests():
    #fix serviceQuery to WHERE NOT EXISTS later
    serviceQuery = '''
SELECT ServiceRequest.servicerequest_id, Guest.name,
    Booking.room_number, ServiceType.type,
    ServiceRequest.requested_datetime
FROM ServiceRequest
INNER JOIN ServiceType
    ON ServiceRequest.servicetype_id = ServiceType.servicetype_id
INNER JOIN Booking
    ON ServiceRequest.booking_id = Booking.booking_id
INNER JOIN Guest
    ON Booking.guest_id = Guest.guest_id
WHERE NOT EXISTS (SELECT servicerequest_id FROM ServiceStaff)'''
    cursor.execute(serviceQuery)
    return cursor.fetchall()

#11/27/24: Updated get_guest to allow guestName to be empty; lets staff look at
#all guests in the system
def get_guest(guestName="NA",contactInfo="NA"):
    query = "SELECT guest_id,name,contact_info FROM Guest "
    queryNeeds = []
    
    #check for any fields being filled for the search
    if guestName != "NA":
        query += "WHERE name=? "
        queryNeeds.append(guestName)
    if contactInfo != "NA":
        if(queryNeeds > 0):
            query += "AND contact_info=?"
        else:
            query += "WHERE contact_info=?"
        queryNeeds.append(contactInfo)
    cursor.execute(query,queryNeeds)
    con.commit()
    return cursor.fetchall()

def get_booking(guestID=-1,guestName="NA",roomNumber="NA",checkin="NA",checkout="NA"):
    query = "SELECT * FROM Booking"
    queryNeeds = []
    queryFlag = False #makes sure "WHERE" and "AND" are correct in query
    guestNameMultiple = False
    if(guestID != -1):
        query += " WHERE guest_id=?"
        queryNeeds.append(guestID)
    elif(guestName != "NA"):
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

    cursor.execute(query,queryNeeds)
    con.commit()
    return cursor.fetchall()

##### Staff info #####
def staff_signup(name, email, password):
    duplicate_check = guest_login(email, password)
    if (duplicate_check != []):
        return -1
    query = "INSERT INTO Staff(name, email, password) VALUES (?, ?, ?)"
    queryNeeds = [name,email,password]
    cursor.execute(query,queryNeeds)
    con.commit()
    return "Success"

def staff_login(email,password):
    query = "SELECT staff_id FROM Staff WHERE email=? AND password=?"
    queryNeeds = [email,password]
    cursor.execute(query,queryNeeds)
    con.commit()
    return cursor.fetchall()

def update_staff(staff_id, name="NA",contact="NA",password="NA"):
    if (name=="NA" and contact == "NA" and password == "NA"):
        return
    query = "UPDATE Staff SET "
    queryNeeds = []
    if(name != "NA"):
        query+= "name=? "
        queryNeeds.append(name)
    if(contact != "NA"):
        if(len(queryNeeds) > 0):
            query+= ", "
        query+= "contact=? "
        queryNeeds.append(contact)
    if(password != "NA"):
        if(len(queryNeeds) > 0):
            query+= ", "
        query+= "password=? "
        queryNeeds.append(cost)
    queryNeeds.append(staff_id)
    query += " WHERE staff_id=?;"
    cursor.execute(query,queryNeeds)
    con.commit()
    return

def delete_staff(staff_id):
    query = "DELETE FROM Staff WHERE staff_id=?"
    queryNeeds = [staff_id]
    cursor.execute(query,queryNeeds)
    con.commit()
    return

##### Guests and booking #####
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

def book_room(guestID, roomNumber, checkin, checkout):
    #Failsafe - immediately exits if the room is already booked for those dates
    query = get_available_rooms(roomNumber,checkInDate=checkin,checkOutDate=checkout)
    if (query == []):
        return -1

    #Get the price of the room to start the total_cost
    cursor.execute("SELECT price FROM Room WHERE room_number=?",[roomNumber])
    con.commit()
    price = cursor.fetchall()[0][0]
    
    #Actual booking query
    cursor.execute('''INSERT INTO Booking(
        guest_id,room_number, check_in_date, check_out_date,total_cost)
        VALUES(?,?,?,?,?)''',[guestID,roomNumber,checkin,checkout,price])
    con.commit()
    return "Success"

#### Services #### 

#returns -1 if the guest does not have permission to request to the given room
#NOTE: Uses current datetime to check if their Booking is still active
#So won't work for any dates that have passed or haven't come yet
#11/28/24: current datetime check in get_bookingID was removed
#Updating request_service so that the guest has to say which bookingID specifically

def request_service(bookingID, servicetype_id):
    query = "INSERT INTO ServiceRequest(booking_id, servicetype_id, requested_datetime) VALUES (?,?, ?)"
    queryNeeds = []
    queryNeeds.append(bookingID)
    queryNeeds.append(servicetype_id)
    queryNeeds.append(datetime.now())

    cursor.execute(query,queryNeeds)
    con.commit()

    query = '''UPDATE Booking SET total_cost=total_cost+(
        SELECT cost FROM ServiceType
            WHERE servicetype_id=?
        )
        WHERE booking_id=?'''
    queryNeeds = [servicetype_id,bookingID]
    cursor.execute(query,queryNeeds)
    con.commit()
    
    return

#Uses current datetime
def fill_service(staffID, servicerequestID):
    query = "INSERT INTO ServiceStaff(staff_id, servicerequest_id, filled_datetime) VALUES (?, ?, ?)"
    queryNeeds = [staffID, servicerequestID, datetime.now()]
    cursor.execute(query,queryNeeds)
    con.commit()
    
    
#11/27/24: assume booking clicked instead of obtaining it natively
def make_payment(bookingID, amt, payment_method="",card_number=""):
    query = "UPDATE Booking SET total_cost=total_cost-? WHERE booking_id=?"
    queryNeeds = [amt,bookingID]
    cursor.execute(query,queryNeeds)
    con.commit()

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
    return

#### Check in/out ####
def check_in(booking_id):
    query = "UPDATE Booking SET check_in_date=? WHERE booking_id=?"
    queryNeeds = [datetime.now(),booking_id]

    cursor.execute(query,queryNeeds)
    con.commit()
    return

def check_out(booking_id):
    query = "UPDATE Booking SET check_out_date=? WHERE booking_id=?"
    queryNeeds = [datetime.now(),booking_id]

    cursor.execute(query,queryNeeds)
    con.commit()

#Notes:
    '''
    Don't allow Booking check_out to succeed until total_cost = 0?
    
11/28/24: Should be handled now by getting bookingID from UI before request
    ***Handling of same guest_id getting the same room at different times
        Especially for get_bookingID for services -- currently charges for every
        Booking the guest has the same room
    
    Once UI ready:
    Connection notes:
        likely can delete get_bookingID (get_booking, get_bookingID, guest_login)
        SUM(total_costs) BY guest_id w/ for loop
    Test if check-in will cause errors -- uses current datetime
        which can make demo go weird even if it would work in the real world
    Test if allows them to request service if they're not checked in
    '''

if __name__ == "__main__":
    create_db()
    drop_tables()
    create_db()
    #Inserted prior:
    insert_room(101,"Single",100)
    insert_room(102,"Single",100.00)
    insert_room(103,"Single",100.00)
    insert_room(201,"Double",150.00)
    insert_room(202,"Double",150.00)
    insert_room(203,"Suite",200.00)

    guest_signup("user1","user1@contact.com","12345")

    staff_signup("admin","admin@contact.com","12345")

    insert_servicetype("Repair TV",10.00)
    insert_servicetype("Room service",30.00)
    insert_servicetype("Clean room",42.00)
    insert_servicetype("Laundry",12.00)
    print("Unfilled requests:",get_unfilled_requests())

    

    '''create_db()
    
    #TESTING: 
    drop_tables()
    create_db()
    insert_room(111,"RoomType",5.12)
    insert_room(414,"RoomType2",100.00)
    insert_room(000,"RoomType2",4400.00)
    
    print("All rooms:",get_available_rooms())
    update_room(414,cost=500)
    print("Updated cost:",get_available_rooms())
    delete_room(000)
    print("Deleted room:",get_available_rooms())

    print("~~~~~~")

    insert_servicetype("Service name",10.00)
    insert_servicetype("Service2 name",30.00)
    insert_servicetype("Service3 name",42.00)

    print("All services:",get_servicetype(),"\n")
    update_servicetype(1,rtype="newname",cost=2)
    print("Updated cost:",get_servicetype(),"\n")
    delete_servicetype(1)
    print("Deleted service:",get_servicetype(),"\n")

    print("~~~~~~")
    
    staff_signup("Staffanie","staffanie123@gmail.com","Sup3rC001!")
    staff_signup("Harold", "hardworker1@gmail.com","password")
    staff_signup("Rodger", "srodger@yahoo.com","LhKgaDdFsaJ86321!")
    
    print("All staff:",get_all_staff(),"\n")
    update_staff(1,name="JJJJJJJJJJJ")
    print("Updated name:",get_all_staff(),"\n")
    delete_staff(2)
    print("Deleted staff:",get_all_staff(),"\n")

    print("~~~~~~")    
    
    print("Getting Rooms....")
    print("\tAny cost:",get_available_rooms(checkInDate="1962-04-20 12:00:00 pm",checkOutDate="1962-04-31 12:00:00 am"))
    print("\tToo cheap:",get_available_rooms(checkInDate="1962-04-20 12:00:00 pm",checkOutDate="1962-04-31 12:00:00 am",cost=0))
    print("\tMid cost:",get_available_rooms(checkInDate="1962-04-20 12:00:00 pm",checkOutDate="1962-04-31 12:00:00 am",cost=50))

    guest_signup("TeeheeGuest","T H E   V O I D", "puppy:D")
    guest_signup("SeriousGrr","Business@gmail.com","I<3Formality.")
    print("All guests:",get_guest())
    print("\tGuest lookup:",get_guest("TeeheeGuest"))
    book_room(guest_login("T H E   V O I D", "puppy:D")[0][0],111,"1962-04-20 12:00:00 pm","1963-04-20 12:00:00 pm")
    print("Bookings:",get_booking())

    print("Getting Rooms....")
    print("\tAny cost:",get_available_rooms(checkInDate="1962-04-20 12:00:00 pm",checkOutDate="1962-04-31 12:00:00 am"))
    print("\tToo cheap:",get_available_rooms(checkInDate="1962-04-20 12:00:00 pm",checkOutDate="1962-04-31 12:00:00 am",cost=0))
    print("\tMid cost:",get_available_rooms(checkInDate="1962-04-20 12:00:00 pm",checkOutDate="1962-04-31 12:00:00 am",cost=50))

    print("Book attempt:",book_room(guest_login("T H E   V O I D", "puppy:D")[0][0],111,"1964-04-20 12:00:00 pm","1965-04-20 12:00:00 pm"))
    print("\nAll Bookings:",get_booking())
    print("Get available:",get_available_rooms(checkInDate="1964-04-20 12:00:00 pm",checkOutDate="1965-04-20 12:00:00 pm"))
    print("Bad book attempt:",book_room(guest_login("Business@gmail.com","I<3Formality.")[0][0],111,"1964-04-20 12:00:00 pm","1965-04-20 12:00:00 pm"))
    print("Valid book attempt:",book_room(guest_login("Business@gmail.com","I<3Formality.")[0][0],414,"1964-04-20 12:00:00 pm","1965-04-20 12:00:00 pm"))

    print("\nSilly booking:",guest_login("T H E   V O I D", "puppy:D"))
    print("Business booking:",guest_login("Business@gmail.com","I<3Formality."))

    print("\nAll Bookings:",get_booking())
    print("\nGet all bookings:",get_booking())
    print("\tGet booking by name:",get_booking(guestName="TeeheeGuest"))
    print("\tGet booking by ID:",get_booking(guestID=1))
    
    print("~~~~~")

    print("Look for guest:",get_booking(guestName="TeeheeGuest"))
    check_in(1)
    print("Guest checked in:",get_booking())

    print("~~~~~")

    print(guest_login("T H E   V O I D", "puppy:D"))
    print("Services offered:",get_servicetype())
    request_service(1,2)
    print("Updated booking:", get_booking(1))

    print("~~~~~")
    
    print(staff_login("staffanie123@gmail.com","Sup3rC001!"))
    print("Unfilled requests:",get_unfilled_requests())
    fill_service(1,1)
    #NOTE: No current way to directly view all servicestaff, but not necessary
    print(get_unfilled_requests())
    
    print("~~~~~")
    print("\tAll charges:",get_booking())
    print("\tID charges:",get_booking(1))

    make_payment(1, 1.00)
    print("\tPaid:",get_booking(1))

    check_out(1)
    print("\tChecked out:",get_booking(1))
    
    drop_tables()'''
    con.close()
    
