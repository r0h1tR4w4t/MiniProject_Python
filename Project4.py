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

mycursor.execute("Create database if not exists hospital_db")
mycursor.execute("use hospital_db")
mycursor.execute("Create table if not exists login(username varchar(25) not null, password varchar(25))")
mycursor.execute("Create table if not exists patients(patient_id int auto_increment primary key, name varchar(50), age int, gender varchar(10), disease varchar(50), doctor_assigned varchar(50))")
mycursor.execute("Create table if not exists doctors(doctor_id int auto_increment primary key, doctor_name varchar(50), specialty varchar(50))")

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
          HOSPITAL MANAGEMENT SYSTEM
    _____________________________
    """)
    print("""
    1. Admin
    2. Doctor
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
                1. Add New Patient
                2. Add New Doctor
                3. Update Patient Info
                4. Display All Patients
                5. Display All Doctors
                6. Change Password
                7. Log Out
                """)
                admin_choice = int(input("Enter your choice: "))
                
                if admin_choice == 1:
                    name = input("Enter Patient Name: ")
                    age = int(input("Enter Age: "))
                    gender = input("Enter Gender: ")
                    disease = input("Enter Disease: ")
                    doctor_assigned = input("Enter Doctor Assigned: ")
                    
                    mycursor.execute(f"INSERT INTO patients(name, age, gender, disease, doctor_assigned) VALUES('{name}', {age}, '{gender}', '{disease}', '{doctor_assigned}')")
                    mydb.commit()
                    print("Patient Added Successfully!")
                
                elif admin_choice == 2:
                    doctor_name = input("Enter Doctor Name: ")
                    specialty = input("Enter Doctor Specialty: ")
                    mycursor.execute(f"INSERT INTO doctors(doctor_name, specialty) VALUES('{doctor_name}', '{specialty}')")
                    mydb.commit()
                    print("Doctor Added Successfully!")
                    
                elif admin_choice == 3:
                    patient_id = int(input("Enter Patient ID: "))
                    new_disease = input("Enter New Disease: ")
                    mycursor.execute(f"UPDATE patients SET disease = '{new_disease}' WHERE patient_id = {patient_id}")
                    mydb.commit()
                    print("Patient Info Updated Successfully!")
                
                elif admin_choice == 4:
                    print("_____________All Patients_____________")
                    mycursor.execute("SELECT * FROM patients")
                    for patient in mycursor:
                        print(patient)
                
                elif admin_choice == 5:
                    print("_____________All Doctors_____________")
                    mycursor.execute("SELECT * FROM doctors")
                    for doctor in mycursor:
                        print(doctor)
                
                elif admin_choice == 6:
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
                
                elif admin_choice == 7:
                    break
                
                loop = input("Press [y/Y] to stay in Admin Mode: ")
        else:
            print("Wrong Password!")

    elif ch == 2:
        print("Welcome, Doctor!")
        print("""
        1. View All Patients
        2. Exit
        """)
        doctor_choice = int(input("Enter your choice: "))
        
        if doctor_choice == 1:
            print("List of Patients:")
            mycursor.execute("SELECT * FROM patients")
            for patient in mycursor:
                print(patient)
        else:
            break
    
    elif ch == 3:
        print("Exiting Hospital Management System...")
        break
