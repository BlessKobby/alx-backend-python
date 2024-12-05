#!/usr/bin/python3
"""Module for streaming and processing user data in batches"""
from typing import Dict, List
import csv
import os


def get_users() -> List[Dict]:
    """Get users from the existing database"""
    # Get the directory where the script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "user_data.csv")
    
    users = []
    try:
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert age to integer since CSV stores everything as strings
                row['age'] = int(row['age'])
                users.append(row)
        return users
    except FileNotFoundError:
        raise FileNotFoundError(f"Database file not found at: {csv_path}")


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
