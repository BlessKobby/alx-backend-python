import sqlite3
import aiosqlite # type: ignore
import asyncio

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

# Async functions for fetching data asynchronously
async def async_fetch_users(db_name):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users(db_name):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    db_name = "example.db"

    # Setup database (if not already set up)
    async with aiosqlite.connect(db_name) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [("Alice", 30), ("Bob", 20), ("Charlie", 45), ("Dave", 50)])
        await db.commit()

    # Fetch data concurrently
    results_users, results_older_users = await asyncio.gather(
        async_fetch_users(db_name),
        async_fetch_older_users(db_name)
    )

    print("All Users:")
    for user in results_users:
        print(user)

    print("\nUsers older than 40:")
    for user in results_older_users:
        print(user)

# Run the async fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
