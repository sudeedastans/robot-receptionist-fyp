import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent / "robot.db"
# Creates the rooms and staff tables if they do not exist.
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
# Adds a new room to the database.
def add_room(room_code,floor,room_type, directions):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO rooms (room_code,floor,room_type, directions)
        VALUES (?,?,?,?)
        """,(room_code,floor,room_type, directions))
    connection.commit()
    connection.close()
#method for add staff
def add_staff(full_name,role,room_code):
    room_id = get_room_id(room_code)
    if room_id is None:
        print(f"Room {room_code} does not exist.")
        return
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO  staff (full_name,role,room_id)
    VALUES (?,?,?)
    """,(full_name,role,room_id))
    connection.commit()
    connection.close()
# Finds the room ID using its room code.
def get_room_id(room_code):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id FROM rooms WHERE room_code = ?",
        (room_code,)
    )
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    return None
# Retrieves room details using the room code.
def get_room(room_code):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT room_code, floor, room_type, directions
        FROM rooms
        WHERE room_code = ?
    """, (room_code,))

    result = cursor.fetchone()
    connection.close()
    return result
# Finds staff information and office location using JOIN.

def get_staff(full_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            staff.full_name,
            staff.role,
            rooms.room_code,
            rooms.floor,
            rooms.directions,
            staff.email,
            staff.photo_path
        FROM staff
        JOIN rooms ON staff.room_id = rooms.id
        WHERE staff.full_name = ? COLLATE NOCASE
    """, (full_name,))

    staff = cursor.fetchone()
    conn.close()

    return staff
def add_staff_contact_columns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check existing columns
    cursor.execute("PRAGMA table_info(staff)")
    columns = [row[1] for row in cursor.fetchall()]

    # Add email column if it does not exist
    if "email" not in columns:
        cursor.execute(
            "ALTER TABLE staff ADD COLUMN email TEXT"
        )

    # Add photo path column if it does not exist
    if "photo_path" not in columns:
        cursor.execute(
            "ALTER TABLE staff ADD COLUMN photo_path TEXT"
        )

    conn.commit()
    conn.close()

def update_staff_contact(staff_id, email, photo_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE staff
        SET email = ?, photo_path = ?
        WHERE id = ?
    """, (email, photo_path, staff_id))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    add_staff_contact_columns()
    add_staff('Jen Joe', 'Lecturer', 'MAE305')
    add_staff('Ahmad Lotfi', 'Lecturer', 'MAE304')
    add_staff('Jen Dan', 'Lecturer', 'MAE303')
    add_staff('Dash Tan', 'Lecturer', 'MAE302')
    add_room('MAE305', 3, 'Staff room', 'Go to the third floor. Turn right. The room is the third door.')
    add_room('MAE304', 3, 'Staff Room', 'Go to the third floor and turn right.')
    add_room('MAE303', 3, 'Staff Room', 'Go to the third floor and turn left.')
    add_room('MAE302', 3, 'Staff Room', 'Go to the third floor and turn left.')
    add_room('MAE103', 1, 'Classroom', 'Go to the first floor and turn left.')
    add_room('MAE104', 1, 'Classroom', 'Go to the first floor and turn left.')
    add_room('MAE105', 1, 'Classroom', 'Go to the first floor and continue straight.')
    add_room('MAE203', 2, 'Laboratory', 'Go to the second floor and turn left.')
    add_room('MAE204', 2, 'Laboratory', 'Go to the second floor and turn left.')
    add_room('MAE205', 2, 'Laboratory', 'Go to the second floor and continue straight.')
    # Fictional contact information for testing
    update_staff_contact(
        1,
        "jen.joe@example.com",
        "assets/staff/jen_joe.jpeg"
    )

    update_staff_contact(
        3,
        "ahmad@example.com",
        "assets/staff/ahmad_lotfi.jpeg"
    )

    update_staff_contact(
        4,
        "jen.dan@example.com",
        "assets/staff/jen_dan.png"
    )

    update_staff_contact(
        5,
        "dash.tan@example.com",
        "assets/staff/dash_tan.jpeg"
    )
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            "UPDATE staff SET photo_path = ? WHERE id = ?",
            [
                ("assets/staff/jen_joe.png", 1),
                ("assets/staff/ahmad_lotfi.png", 3),
                ("assets/staff/jen_dan.png", 4),
                ("assets/staff/dash_tan.png", 5)
            ]
        )
    print("Data added successfully.")

