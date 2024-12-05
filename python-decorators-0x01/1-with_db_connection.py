import sqlite3
import functools

def with_db_connection(func):
    """Decorator that handles database connection lifecycle"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create database connection
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function with the connection as first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Ensure connection is always closed, even if an error occurs
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)