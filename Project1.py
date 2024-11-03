import mysql.connector

""" 
        © [2024] [Rohit Rawat]. All rights reserved.

This source code is the property of [Rohit Rawat] and is protected by copyright law and international treaties. Unauthorized reproduction, distribution, or modification of this code or any of its components is strictly prohibited.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
2. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

"""

mydb = mysql.connector.connect(host="localhost",user="root",passwd="root")
mycursor = mydb.cursor()

mycursor.execute("Create database if not exists sales_IMS")
mycursor.execute("use sales_IMS")
mycursor.execute("Create table if not exists login(username varchar(25) not null,password varchar(25))")

mycursor.execute("create table if not exists purchase(odate date not null , name varchar(25) not null , pcode int not null, amount int not null)")
mycursor.execute("create table if not exists stock(pcode int not null , pname varchar(25) not null , quantity int not null, price int not null)")

mycursor.execute("alter table login modify password varchar(25) not null")

mydb.commit()


z = 0
mycursor.execute("select * from login")
for i in mycursor:
    z+=1

if z == 0:
    mycursor.execute("insert into login values('admin','ng')")
    mydb.commit()


while True:
    print("""
    ________________________________________________________________________________________________
                          WELCOME TO SALES AND INVENTORY MANAGEMENT SYSTEM 
    ________________________________________________________________________________________________
      """)
    print(""" 
          
    1. Admin
    2. Customer
    3. Exit
    """)
    ch = int(input("Enter your choice : "))

    if ch == 1:
        passs = input("Enter Password :  ")
        mycursor.execute("select * from login")
        for i in mycursor:
            username , password = i
    
        if(passs ==  password):
            print(" WELCOME :) ")
            loop = 'y'
            while loop == 'y' or loop == 'Y':
                print(""" 
                1. Add New Item
                2. Update Price 
                3. Delete Item
                4. Display all Items
                5. Change password
                6. Log Out
                """)
            
                ch_a = int(input("Enter your choice : "))
                if ch_a == 1:
                    loop1 = 'y'
                    while loop1 == 'y' or loop1 == 'Y':
                        pcode = int(input("Enter Product Code : "))
                        pname = input("Enter Procut Name : ")
                        quantity = int(input("Enter product quantity : "))
                        price =  int(input("Enter product price : "))

                        mycursor.execute("insert into stock values('"+str(pcode)+"' , '"+pname+"' , '"+str(quantity)+"','"+str(price)+"')")
                        mydb.commit()
                        print("Record Inserted Successfully")
                        loop1 = input("Press [y/Y] to enter more items :  ")
                elif ch_a == 2:
                    
                    loop2 = 'y'
                    while loop2 == 'Y' or loop2 == 'y':
                        pcode = int(input("Enter Product code : "))
                        new_price = int(input("Enter new Price : "))

                        mycursor.execute("update stock set price= '"+str(new_price)+"'   where pcode = '"+str(pcode)+"'" )
                        mydb.commit()
                        loop2 = input("Press [Y/y] to change price of any other item : ")   
                
                elif ch_a == 3:
                    loop3 = 'y'

                    while loop == 'y' or loop == 'Y':
                        pcode = int(input("Enter Pcode : "))
                        mycursor.execute("delete from stock where pcode = '"+str(pcode)+"' ")
                        mydb.commit()
                        loop3 = print("Press [y/Y] to enter More data : ")

                elif ch_a == 4:
                    print("_____________Stock Details_______________")
                    print("[Pcode , Item , Quantity , Price]")
                    mycursor.execute("select * from stock")

                    for i in mycursor:
                        p_code , I_tem , Q_uantity , P_rice = i
                        print("[" , p_code , I_tem, Q_uantity, P_rice, "]")
                elif ch_a == 5: 
                    old_pass = input("Enter old Password : ")
                    mycursor.execute("select * from login")

                    for i in mycursor:
                        username,password = i

                    if(old_pass == password):
                        new_pass = input("Enter new Password : ")
                        mycursor.execute("update login set password = '" +new_pass+"' ")
                        mydb.commit()
                        print("Updated Successfully")
                    else:
                        print("Wrong Password !")
                else:
                    print()
                    print("Exiting Admin Mode ...................")
                    print("Done")
                    print()
                    break
                loop = input("Press [y/Y] to stay in Admin Mode : ")
        else:
            print("Wrong Password :)")

    elif ch == 2:
        

        loop = 'y'

        while loop == 'y' or loop == 'Y':
            print("WELCOME")
            print("""
            1. Items Basket
            2. Exit 
            """)

            ch = int(input("Enter your choice : "))

            if ch ==  1:
                loop1 = 'y'
                while loop1 == 'y' or loop1 == 'Y':
                    print("_____________Items Avilable_______________")
                    print("[Pcode , Item , Quantity , Price]")
                    mycursor.execute("select * from stock")

                    for i in mycursor:
                        p_code , I_tem , Q_uantity , P_rice = i
                        print("[" , p_code , I_tem, Q_uantity, P_rice, "]")

                    print()
                    name = input("Enter Your Name : ")
                    pcode = int(input("Enter Product Code : "))
                    quantity = int(input("Enter Product quantity : "))

                    mycursor.execute("select * from stock where pcode = '"+str(pcode)+"' ")

                    for i in mycursor:
                        t_code,t_name,t_quan,t_price = i
                    amount = t_price * quantity
                    net_quan = t_quan - quantity 
                    mycursor.execute(" update stock set quantity= '"+str(net_quan)+"' where pcode= '"+str(pcode)+"' ")   
                    mydb.commit()
                    mycursor.execute("insert into purchase values(now() , '"+name+"' , '"+str(pcode)+"' , '"+str(amount)+"') ")
                    mydb.commit()
                    print("The total amount to be paid is  : ", amount)

                    loop1 = input("Press [y/Y] to enter more items : ")
            else :
                break

            loop = input("Press [y/Y] to stay in Customer Mode : ")

    
    elif ch == 3:
        print()
        print("Exiting Sales and Inventoy Management System ................. ")
        print("Done")
        break


