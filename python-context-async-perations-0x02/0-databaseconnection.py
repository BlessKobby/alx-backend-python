import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """Establishes the database connection and returns the cursor."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes the database connection, committing if necessary."""
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        if self.connection:
            self.connection.commit()
            self.connection.close()

# Usage example:
def main():
    db_name = "example.db"

    # Setup database (if not already set up)
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.executemany("INSERT INTO users (name) VALUES (?)", [("Alice",), ("Bob",), ("Charlie",)])
        conn.commit()

    # Use the custom context manager to query the database
    with DatabaseConnection(db_name) as db_cursor:
        db_cursor.execute("SELECT * FROM users")
        results = db_cursor.fetchall()
        print("Query Results:")
        for row in results:
            print(row)

if __name__ == "__main__":
    main()
