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
    """Generator that yields pages of users lazily"""
    offset = 0
    while True:
        # Fetch the next page of results
        results = paginate_users(page_size, offset)
        
        # If no more results, stop iteration
        if not results:
            break
            
        # Yield the current page
        yield results
        
        # Move to next page
        offset += page_size


# Example usage:
if __name__ == "__main__":
    # Get pages of 2 users at a time
    for page in lazy_paginate(2):
        print("Page of users:", page)