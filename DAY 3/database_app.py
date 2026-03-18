import sqlite3

con=sqlite3.connect("students.db")
cur=con.cursor()

## create table

cur.execute("CREATE TABLE IF NOT EXISTS STUDENTS(ID INT PRIMARY KEY,NAME VARCHAR(123),AGE INT NOT NULL, GENDER VARCHAR(50))")
con.commit()

## insert data 
def insert():
    n=int(input("enter the total number of records you want to insert:"))
    name=input("enter your name:")
    age=int(input("enetr your age:"))
    gender=input("enetr your gender:")
    for i in range(n):
        cur.execute("INSERT INTO STUDENTS(NAME,AGE,GENDER) VALUES(?,?,?)",(name,age,gender))
        con.commit()
    return "data inserted successfully"

## read data
def read():
    cur.execute("SELECT * FROM STUDENTS")
    data=cur.fetchall()
    print("ID\tNAME\tAGE\tGENDER")
    for row in data:
        print(row[0],"\t",row[1],"\t",row[2],"\t",row[3])
    con.commit()

## update data
def update():
    id=int(input("enter ID"))
    name=input("updated name:")
    age=int(input("updated age:"))
    gender=input("updated gender:")
    cur.execute("UPDATE STUDENTS SET NAME=?,AGE=?,GENDER=? WHERE ID=?",(name,age,gender,id))
    con.commit()
    
    return "data updated successfully"

## DELETE DATA
def delete():
    id=int(input("enetr the ID to delete:"))
    cur.execute("DELETE FROM STUDENTS WHERE ID=?",(id,))
    con.commit()
    return "data deleted successfuly"



while True:

    print("Enter your choice:")
    print("1. Insert data, 2. Read data, 3. Update data, 4. Delete data, 5.Stop")
    ch=int(input())

    match ch:
        case 1:print(insert())
        case 2:print(read())
        case 3:print(update())
        case 4:print(delete()) 
        case 5:con.close(); break
        case _:print("Invalid choice")

