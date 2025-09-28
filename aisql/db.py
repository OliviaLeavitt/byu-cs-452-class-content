import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
    except Error as e:
        print(f"Error connecting to database: {e}")
    return connection


def create_table(connection, create_table_sql):
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
        connection.commit()
        print("Table created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


if __name__ == "__main__":
    connection = create_connection("baking.sqlite")
    if connection:
        print("Connection worked!")
        connection.close()
