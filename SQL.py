import sqlite3
from tkinter import *
cursor = ''
con = ''

def create_db():
    global con
    global cursor
    con = sqlite3.connect("Contact.db")
    cursor = con.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS Contacts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT NOT NULL
            )
        '''
        )
    con.commit()
def insert_row(valueList):
    cursor.execute(
        "INSERT INTO Contacts(name, phone_number, email) VALUES (?, ?, ?)",
        (valueList[0], valueList[1], valueList[2])
    )
    con.commit()
def select_all():
    cursor.execute("SELECT * FROM Contacts")
    print(cursor.fetchall())


def drop_db():
    cursor.execute("DROP TABLE Contacts")
    con.commit()

if __name__ == "__main__":
    print("Hello World!")
    create_db()
    select_all()
    insert_row(["new name","new number","new email"])
    select_all()
    drop_db()
    con.commit()
    con.close()
    
