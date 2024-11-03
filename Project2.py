import mysql.connector

""" 
        © [2024] [Rohit Rawat]. All rights reserved.

This source code is the property of [Rohit Rawat] and is protected by copyright law and international treaties. Unauthorized reproduction, distribution, or modification of this code or any of its components is strictly prohibited.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
2. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

"""

mydb = mysql.connector.connect(host="localhost", user="root", passwd="root")
mycursor = mydb.cursor()

mycursor.execute("Create database if not exists library_db")
mycursor.execute("use library_db")
mycursor.execute("Create table if not exists login(username varchar(25) not null, password varchar(25))")
mycursor.execute("Create table if not exists books(book_id int not null, title varchar(50) not null, author varchar(50), available int not null)")

mycursor.execute("alter table login modify password varchar(25) not null")
mydb.commit()

z = 0
mycursor.execute("select * from login")
for i in mycursor:
    z += 1

if z == 0:
    mycursor.execute("insert into login values('admin', 'admin')")
    mydb.commit()

while True:
    print("""
    _____________________________
          LIBRARY MANAGEMENT SYSTEM
    _____________________________
    """)
    print("""
    1. Admin
    2. Member
    3. Exit
    """)
    ch = int(input("Enter your choice: "))

    if ch == 1:
        password = input("Enter Password: ")
        mycursor.execute("select * from login")
        for i in mycursor:
            username, passwd = i

        if password == passwd:
            print("Welcome, Admin!")
            loop = 'y'
            while loop == 'y' or loop == 'Y':
                print("""
                1. Add New Book
                2. Update Book Availability
                3. Delete Book
                4. Display All Books
                5. Change Password
                6. Log Out
                """)
                admin_choice = int(input("Enter your choice: "))

                
                if admin_choice == 1:
                    book_id = int(input("Enter Book ID: "))
                    title = input("Enter Book Title: ")
                    author = input("Enter Book Author: ")
                    available = int(input("Enter Availability (1 for available, 0 for not): "))
                    
                    mycursor.execute(f"INSERT INTO books VALUES({book_id}, '{title}', '{author}', {available})")
                    mydb.commit()
                    print("Book Added Successfully!")
                
                elif admin_choice == 2:
                    book_id = int(input("Enter Book ID: "))
                    availability = int(input("Enter new Availability (1 for available, 0 for not): "))
                    mycursor.execute(f"UPDATE books SET available = {availability} WHERE book_id = {book_id}")
                    mydb.commit()
                    print("Book availability updated.")
                    
                elif admin_choice == 3:
                    book_id = int(input("Enter Book ID to delete: "))
                    mycursor.execute(f"DELETE FROM books WHERE book_id = {book_id}")
                    mydb.commit()
                    print("Book deleted.")
                
                elif admin_choice == 4:
                    print("_____________Library Books_____________")
                    mycursor.execute("SELECT * FROM books")
                    for book in mycursor:
                        print(book)
                
                elif admin_choice == 5:
                    old_password = input("Enter old Password: ")
                    mycursor.execute("SELECT * FROM login")
                    for i in mycursor:
                        username, passwd = i
                    if old_password == passwd:
                        new_password = input("Enter new Password: ")
                        mycursor.execute(f"UPDATE login SET password = '{new_password}'")
                        mydb.commit()
                        print("Password updated successfully.")
                    else:
                        print("Incorrect old password!")
                
                elif admin_choice == 6:
                    break
                
                loop = input("Press [y/Y] to stay in Admin Mode: ")
        else:
            print("Wrong Password!")

    elif ch == 2:
        print("Welcome, Member!")
        print("""
        1. View Available Books
        2. Borrow Book
        3. Return Book
        """)
        member_choice = int(input("Enter your choice: "))
        
        if member_choice == 1:
            mycursor.execute("SELECT * FROM books WHERE available = 1")
            print("Available Books:")
            for book in mycursor:
                print(book)
        
        elif member_choice == 2:
            book_id = int(input("Enter Book ID to borrow: "))
            mycursor.execute(f"SELECT * FROM books WHERE book_id = {book_id} AND available = 1")
            if mycursor.fetchone():
                mycursor.execute(f"UPDATE books SET available = 0 WHERE book_id = {book_id}")
                mydb.commit()
                print("Book borrowed successfully.")
            else:
                print("Book is not available.")
        
        elif member_choice == 3:
            book_id = int(input("Enter Book ID to return: "))
            mycursor.execute(f"UPDATE books SET available = 1 WHERE book_id = {book_id}")
            mydb.commit()
            print("Book returned successfully.")
        
        else:
            print("Invalid Choice!")
    
    elif ch == 3:
        print("Exiting Library Management System...")
        break
