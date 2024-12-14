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

class ExecuteQuery:
    def __init__(self, db_name, query, params):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None

    def __enter__(self):
        """Establishes the database connection, executes the query, and returns the results."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes the database connection."""
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        if self.connection:
            self.connection.close()

# Usage example:
def main():
    db_name = "example.db"

    # Setup database (if not already set up)
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [("Alice", 30), ("Bob", 20), ("Charlie", 35)])
        conn.commit()

    # Use the custom context manager to execute a query
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery(db_name, query, param) as results:
        print("Query Results:")
        for row in results:
            print(row)

if __name__ == "__main__":
    main()
