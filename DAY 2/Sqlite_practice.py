import sqlite3

connection = sqlite3.connect('employee.db')
cur=connection.cursor()

## Create
cur.execute("CREATE TABLE IF NOT EXISTS EMPLOYEES(ID INTEGER PRIMARY KEY,NAME VARCHAR(120),AGE INT NOT NULL, DEPARTMENT VARCHAR(120),SALARY INT NOT NULL)")
cur.execute("INSERT INTO EMPLOYEES(NAME,AGE,DEPARTMENT,SALARY) VALUES('John Doe',30,'IT',50000)")
cur.execute("INSERT INTO EMPLOYEES(NAME,AGE,DEPARTMENT,SALARY) VALUES('Jane Smith',25,'HR',45000)")
cur.execute("INSERT INTO EMPLOYEES(NAME,AGE,DEPARTMENT,SALARY) VALUES('Emily Davis',35,'Finance',60000)")
cur.execute("INSERT INTO EMPLOYEES(NAME,AGE,DEPARTMENT,SALARY) VALUES('Michael Brown',28,'IT',55000)")
cur.execute("INSERT INTO EMPLOYEES(NAME,AGE,DEPARTMENT,SALARY) VALUES('Sarah Wilson',32,'HR',48000)")
connection.commit()

print("ALL THE EMPLOYEES WORKS IN IT DEPARTEMENT")
cur.execute("SELECT * FROM EMPLOYEES WHERE DEPARTMENT='IT'")
results=cur.fetchall()
print(results)
connection.commit()
print("\n")

## Update 
cur.execute("UPDATE EMPLOYEES SET SALARY= SALARY +5000 WHERE DEPARTMENT='HR'")
connection.commit()
print("\n")

## Read
print("SALARY INCREASED BY 5000 FOR HR DEPARTMENT")
cur.execute("SELECT SALARY FROM EMPLOYEES WHERE DEPARTMENT='HR'")
Updated_salary=cur.fetchall()
print("Updated Salary for HR Departement:", Updated_salary)
print("\n")
cur.execute("SELECT DEPARTMENT, AVG(SALARY) FROM EMPLOYEES GROUP BY DEPARTMENT")
avg_salaries=cur.fetchall()
print("\n")
print("AVERAGE SALARIES BY DEPARTMENTS:")
print(avg_salaries)


## Delete 
print("\n")
print("DELETING EMPLOYEES IN FINANCE DEPARTMENT")
cur.execute("DELETE FROM EMPLOYEES WHERE DEPARTMENT='Finance'")
connection.commit()

cur.execute("SELECT * FROM EMPLOYEES")
remaining_employees=cur.fetchall()
print("Remaining Employees:", remaining_employees)

## Close the connection
connection.close()