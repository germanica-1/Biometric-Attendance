import pymysql
import os

def add_employee(ID, Name):
    if not ID.isdigit():
        return False, "ID must be an integer"
    if not Name:
        return False, "Name cannot be empty"

    try:
        mydb = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = mydb.cursor()

        # Check if the ID already exists in the 'employee' table
        cursor.execute("SELECT * FROM employee WHERE ID = %s", (ID))
        if cursor.fetchone():
            return False, "ID already exists"

        # Insert into the 'employee' table using the correct column names
        cursor.execute(
            "INSERT INTO employee (ID, Name) VALUES (%s, %s)",
            (ID, Name)
        )
        mydb.commit()
        return True, "Employee added successfully!"
    
    except Exception as e:
        return False, f"Database Error: {str(e)}"

    finally:
        cursor.close()
        mydb.close()
