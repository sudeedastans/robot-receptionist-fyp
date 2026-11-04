import sqlite3
from pathlib import Path
import secrets

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
#Same 30 appointment times for every staff member
MAY_APPOINTMENTS = [
    "2027-05-03 10:00",
    "2027-05-04 10:00",
    "2027-05-05 10:00",
    "2027-05-06 10:00",
    "2027-05-07 10:00"
]
def setup_appointments():
    with sqlite3.connect(DB_PATH) as conn:
        #stores available appointment times
        conn.execute("""
            CREATE TABLE IF NOT EXISTS appointment_slots(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER NOT NULL,
                slot_time TEXT NOT NULL,
                FOREIGN KEY (staff_id) REFERENCES staff(id),
                UNIQUE(staff_id, slot_time)
                )""")
        #stores confirmed bookings
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_reference TEXT UNIQUE NOT NULL,
                slot_id INTEGER NOT NULL,
                visitor_name TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Confirmed',
                booked_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (slot_id) REFERENCES appointment_slots(id)
                )""")

        # Prevent two confirmed bookings for one slot
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            unique_confirmed_slot
            ON bookings(slot_id)
            WHERE status = 'Confirmed'
        """)
        # Get all staff IDs
        staff_ids = conn.execute(
            "SELECT id FROM staff"
        ).fetchall()
        # Add the same five appointments for each staff member
        for staff in staff_ids:
            staff_id = staff[0]

            for date in MAY_APPOINTMENTS:
                conn.execute("""
                            INSERT OR IGNORE INTO appointment_slots
                            (staff_id, slot_time)
                            VALUES (?, ?)
                        """, (staff_id, date))
#COLLATE NOCASE = BUYUK KUCUK HARF FARKINI GORMEZDEN GEL
def get_available_slots(staff_name):
    with sqlite3.connect(DB_PATH) as conn:

        slots = conn.execute("""
            SELECT appointment_slots.id, appointment_slots.slot_time
            FROM appointment_slots
            JOIN staff ON appointment_slots.staff_id = staff.id
            WHERE staff.full_name = ? COLLATE NOCASE
              AND appointment_slots.slot_time IN (?, ?, ?, ?, ?)
              AND NOT EXISTS (
                  SELECT 1 FROM bookings
                  WHERE bookings.slot_id = appointment_slots.id
                    AND bookings.status = 'Confirmed'
              )
            ORDER BY appointment_slots.slot_time
        """, (staff_name, *MAY_APPOINTMENTS)).fetchall()

        return slots

def book_appointment(slot_id):

    # Generate a booking reference
    reference = "RR-" + secrets.token_hex(4).upper()

    with sqlite3.connect(DB_PATH) as conn:

        # Check if the selected slot exists
        slot = conn.execute("""
            SELECT slot_time
            FROM appointment_slots
            WHERE id = ?
        """, (slot_id,)).fetchone()

        if slot is None or slot[0] not in MAY_APPOINTMENTS:
            return None

        # Save the booking
        try:
            conn.execute("""
                INSERT INTO bookings
                (booking_reference, slot_id, visitor_name)
                VALUES (?, ?, ?)
            """, (reference, slot_id, "Demo Visitor"))

            return reference

        except sqlite3.IntegrityError:
            return None

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
    setup_appointments()
    print("Appointment slots created successfully!")
    print(get_available_slots("Jen Joe"))
    slots = get_available_slots("Jen Joe")

