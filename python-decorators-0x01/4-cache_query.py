import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    """Decorator that handles database connection lifecycle"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """Decorator that caches query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query', args[1] if len(args) > 1 else None)
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]
        
        # Execute the function and cache the result
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")