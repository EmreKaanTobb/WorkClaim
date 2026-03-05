# tech_comparisons/postgresql_vs_sqlite.py

# SQLite Approach
# SQLite is easy to set up locally, but it locks the entire database during writes
# Since WorkClaim will have multiple students and teachers trying to reserve facilities at the same time, this will cause database bottlenecks and crashes.
import sqlite3

def test_sqlite():
    conn = sqlite3.connect('workclaim_test.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS facilities (id INTEGER, name TEXT)''')
    print("SQLite connection successful, but not suitable for concurrent reservations.")
    conn.close()

test_sqlite()


# PostgreSQL Approach (Our Choice)
# We chose PostgreSQL because it handles high concurrency perfectly. 
# It is essential for our Role-Based Access Control (RBAC) and priority booking handling without locking the database.
import psycopg2

def test_postgresql():
    try:
        # Example connection parameters for just now
        conn = psycopg2.connect(
            dbname="workclaim_db", 
            user="postgres", 
            password="password", 
            host="localhost"
        )
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS facilities (id SERIAL PRIMARY KEY, name VARCHAR(255))''')
        print("PostgreSQL connection successful. Ready for high concurrency.")
        conn.close()
    except Exception as e:
        print("PostgreSQL requires a running server, but this is the architecture we will use:", e)

test_postgresql()
