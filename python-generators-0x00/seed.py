import mysql.connector
import uuid
import csv
from mysql.connector import Error
from typing import Dict, List

def connect_db():
    """Connects to MySQL server"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Server: {e}")
        return None

def create_database(connection):
    """Creates database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """Connects to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection):
    """Creates user_data table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX idx_user_id (user_id)
            )
        """)
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, filename):
    """Inserts data into user_data table"""
    try:
        cursor = connection.cursor()
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            
            for row in csv_reader:
                # Updated indices to match CSV column order
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (row[0], row[1], row[2], row[3]))  # Use existing UUID from CSV
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")

def get_users() -> List[Dict]:
    """Get users from the existing database"""
    users = []
    with open("user_data.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert age to integer since CSV stores everything as strings
            row['age'] = int(row['age'])
            users.append(row)
    return users

def stream_users_in_batches(batch_size: int):
    """Generator function that yields batches of users"""
    users = get_users()
    for i in range(0, len(users), batch_size):
        yield users[i:i + batch_size]

def batch_processing(batch_size: int):
    """Generator function that processes batches and filters users over 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user

def main():
    # Connect to MySQL server
    connection = connect_db()
    if connection is None:
        return

    # Create database
    create_database(connection)
    connection.close()

    # Connect to ALX_prodev database
    db_connection = connect_to_prodev()
    if db_connection is None:
        return

    # Create table
    create_table(db_connection)

    # Read and insert data from CSV
    try:
        insert_data(db_connection, 'user_data.csv')
    except FileNotFoundError:
        print("user_data.csv file not found")
    finally:
        db_connection.close()

if __name__ == "__main__":
    main() 