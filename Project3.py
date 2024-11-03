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

mycursor.execute("Create database if not exists restaurant_db")
mycursor.execute("use restaurant_db")
mycursor.execute("Create table if not exists login(username varchar(25) not null, password varchar(25))")
mycursor.execute("Create table if not exists menu(item_code int not null, item_name varchar(50) not null, price int not null, available int not null)")
mycursor.execute("Create table if not exists orders(order_id int auto_increment primary key, item_code int, quantity int, total_price int, order_time timestamp default current_timestamp)")

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
          RESTAURANT MANAGEMENT SYSTEM
    _____________________________
    """)
    print("""
    1. Admin
    2. Customer
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
                1. Add New Menu Item
                2. Update Menu Item Price/Availability
                3. Delete Menu Item
                4. Display All Menu Items
                5. Change Password
                6. Log Out
                """)
                admin_choice = int(input("Enter your choice: "))
                
                if admin_choice == 1:
                    item_code = int(input("Enter Item Code: "))
                    item_name = input("Enter Item Name: ")
                    price = int(input("Enter Item Price: "))
                    available = int(input("Enter Availability (1 for available, 0 for not): "))
                    
                    mycursor.execute(f"INSERT INTO menu VALUES({item_code}, '{item_name}', {price}, {available})")
                    mydb.commit()
                    print("Menu Item Added Successfully!")
                
                elif admin_choice == 2:
                    item_code = int(input("Enter Item Code: "))
                    price = int(input("Enter new Price: "))
                    availability = int(input("Enter new Availability (1 for available, 0 for not): "))
                    mycursor.execute(f"UPDATE menu SET price = {price}, available = {availability} WHERE item_code = {item_code}")
                    mydb.commit()
                    print("Menu Item Updated Successfully!")
                    
                elif admin_choice == 3:
                    item_code = int(input("Enter Item Code to delete: "))
                    mycursor.execute(f"DELETE FROM menu WHERE item_code = {item_code}")
                    mydb.commit()
                    print("Menu Item Deleted Successfully!")
                
                elif admin_choice == 4:
                    print("_____________Restaurant Menu_____________")
                    mycursor.execute("SELECT * FROM menu")
                    for item in mycursor:
                        print(item)
                
                elif admin_choice == 5:
                    old_password = input("Enter old Password: ")
                    mycursor.execute("SELECT * FROM login")
                    for i in mycursor:
                        username, passwd = i
                    if old_password == passwd:
                        new_password = input("Enter new Password: ")
                        mycursor.execute(f"UPDATE login SET password = '{new_password}'")
                        mydb.commit()
                        print("Password Updated Successfully!")
                    else:
                        print("Incorrect old password!")
                
                elif admin_choice == 6:
                    break
                
                loop = input("Press [y/Y] to stay in Admin Mode: ")
        else:
            print("Wrong Password!")

    elif ch == 2:
        print("Welcome, Customer!")
        print("""
        1. View Menu
        2. Place Order
        3. Exit
        """)
        customer_choice = int(input("Enter your choice: "))
        
        if customer_choice == 1:
            print("Available Menu Items:")
            mycursor.execute("SELECT * FROM menu WHERE available = 1")
            for item in mycursor:
                print(item)
        
        elif customer_choice == 2:
            item_code = int(input("Enter Item Code: "))
            quantity = int(input("Enter Quantity: "))
            mycursor.execute(f"SELECT price FROM menu WHERE item_code = {item_code} AND available = 1")
            result = mycursor.fetchone()
            
            if result:
                price = result[0]
                total_price = price * quantity
                mycursor.execute(f"INSERT INTO orders(item_code, quantity, total_price) VALUES({item_code}, {quantity}, {total_price})")
                mydb.commit()
                print(f"Order Placed! Total amount to pay: {total_price}")
            else:
                print("Item not available.")
        else:
            break
    
    elif ch == 3:
        print("Exiting Restaurant Management System...")
        break
