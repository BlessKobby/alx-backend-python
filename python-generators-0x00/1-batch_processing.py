#!/usr/bin/python3
"""Module for streaming and processing user data in batches"""
from typing import Dict, List
import csv
import os
import sqlite3


def get_users() -> List[Dict]:
    """Get users from the existing database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    
    users = []
    for row in cursor.fetchall():
        # Convert row to dictionary
        user = {
            'id': row[0],
            'name': row[1],
            'age': row[2],
            'email': row[3]
        }
        users.append(user)
    
    conn.close()
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
