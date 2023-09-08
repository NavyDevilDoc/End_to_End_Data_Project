import sqlite3

def create_db_and_table(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Experimental_Data_Capture (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 temperature REAL,
                 pressure REAL,
                 humidity REAL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()


def sample_data(db_name, sample_size):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM Experimental_Data_Capture ORDER BY RANDOM() LIMIT {sample_size}")
        return c.fetchall()


if __name__ == '__main__':
    # Testing the function
    print("Creating test database...")
    create_db_and_table("test_database.db")
    print("Database created successfully!")