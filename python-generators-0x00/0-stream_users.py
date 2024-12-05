#!/usr/bin/env python3
"""Module for streaming user data from database"""
import mysql.connector
from typing import Generator, Tuple, Any


def stream_users() -> Generator[Tuple[Any, ...], None, None]:
    """
    Generator function that yields one row at a time from user_data table
    Returns: Generator yielding tuples containing user data
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        
        # Yield one row at a time
        for row in cursor:
            yield row
            
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close() 