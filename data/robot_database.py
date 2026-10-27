import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent / "robot.db"
def create_database():
    connection = sqlite3.connect(DB_PATH)
    #cursor sends sql commands
    cursor = connection.cursor()
    #foreign key will use thats implemented it
    cursor.execute("PRAGMA foreign_keys = ON")
    #creats rooms table [ AUTOINCREMENT gives special id for each room]
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_code TEXT UNIQUE NOT NULL,
        floor INTEGER NOT NULL,
        room_type TEXT,
        directions TEXT)
        """)
    # creats STAFF table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT UNIQUE NOT NULL,
        role TEXT,
        room_id INTEGER,
        FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
        """)
    connection.commit()
    connection.close()
    print("Database created succesfully.")
#method for add room information
def add_room(room_code,floor,room_type, directions):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO rooms (room_code,floor,room_type, directions)
        VALUES (?,?,?,?)
        """,(room_code,floor,room_type, directions))
    connection.commit()
    connection.close()
#method for add staff
def add_staff(full_name,role,room_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO staff (full_name,role,room_id)
    VALUES (?,?,?,?)
    """,(full_name,role,room_id))
    connection.commit()
    connection.close()
if __name__ == "__main__":
    create_database()
