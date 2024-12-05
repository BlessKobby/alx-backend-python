#!/usr/bin/python3
"""Module for lazy pagination of user data"""
import sqlite3


def paginate_users(page_size: int, offset: int = 0) -> list:
    """Fetch a page of users from the database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM users LIMIT ? OFFSET ?",
        (page_size, offset)
    )
    results = cursor.fetchall()
    
    conn.close()
    return results


def lazy_paginate(page_size: int):
    """Generator that yields one user at a time from each page"""
    page = paginate_users(page_size, 0)  # Only fetch first page at offset 0
    for user in page:
        yield user


# Example usage:
if __name__ == "__main__":
    # Get users one at a time from the first page
    for user in lazy_paginate(2):
        print("User:", user)