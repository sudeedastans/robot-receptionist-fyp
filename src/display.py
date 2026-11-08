import tkinter as tk
from data.robot_database import get_room, get_staff, get_available_slots,book_appointment,get_booking_details
from pathlib import Path
from src.question_handler import understand_question
# Colour palette
BG = "#0E192B"
CARD = "#1B2B45"
WHITE = "#FFFFFF"
MUTED = "#A9BCD0"
BLUE = "#43C6F5"
PURPLE = "#9968F5"
YELLOW = "#F2BD63"

# Fictional room positions for each floor
FLOOR_MAP_POSITIONS = {
    1: {
        "MAE103": (12, 18, 122, 72),
        "MAE104": (12, 84, 122, 138),
        "MAE105": (12, 150, 122, 204)
    },

    2: {
        "MAE203": (12, 18, 122, 72),
        "MAE204": (12, 84, 122, 138),
        "MAE205": (12, 150, 122, 204)
    },

    3: {
        "MAE302": (12, 30, 122, 95),
        "MAE303": (12, 115, 122, 180),
        "MAE304": (178, 30, 288, 95),
        "MAE305": (178, 115, 288, 180)
    }
}


class RobotDisplay:

    def __init__(self):

        # Main window
        self.root = tk.Tk()
        self.root.title("Robot Receptionist")
        self.root.geometry("1024x600")
        self.root.configure(bg=BG)

        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=40, pady=(20, 12))

        tk.Label(
            header,
            text="ROBOT RECEPTIONIST",
            font=("Arial", 16, "bold"),
            fg=WHITE,
            bg=BG
        ).pack(side="left")

        self.status_label = tk.Label(
            header,
            font=("Arial", 12, "bold"),
            fg=BLUE,
            bg=BG
        )
        self.status_label.pack(side="right")

        # Main card
        self.card = tk.Frame(self.root, bg=CARD)
        self.card.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0, 10)
        )

        # Standard screen
        self.standard_view = tk.Frame(self.card, bg=CARD)

        self.title_label = tk.Label(
            self.standard_view,
            font=("Arial", 46, "bold"),
            fg=WHITE,
            bg=CARD
        )
        self.title_label.pack(pady=(105, 15))

        self.subtitle_label = tk.Label(
            self.standard_view,
            font=("Arial", 25),
            fg=WHITE,
            bg=CARD
        )
        self.subtitle_label.pack(pady=10)

        self.info_label = tk.Label(
            self.standard_view,
            font=("Arial", 16),
            fg=MUTED,
            bg=CARD,
            wraplength=800,
            justify="center"
        )
        self.info_label.pack(pady=20)

        # Room information screen
        self.room_view = tk.Frame(self.card, bg=CARD)

        # RIGHT SIDE: MINI MAP
        self.map_frame = tk.Frame(self.room_view, bg=CARD)
        self.map_frame.pack(
            side="right",
            padx=(25, 0),
            anchor="n"
        )

        self.map_title_label = tk.Label(
            self.map_frame,
            font=("Arial", 17, "bold"),
            fg=WHITE,
            bg=CARD
        )
        self.map_title_label.pack(pady=(0, 15))

        self.map_canvas = tk.Canvas(
            self.map_frame,
            width=300,
            height=225,
            bg="#EAF2FC",
            highlightthickness=0
        )
        self.map_canvas.pack()

        self.map_note_label = tk.Label(
            self.map_frame,
            text="Blue = selected room",
            font=("Arial", 12),
            fg=MUTED,
            bg=CARD
        )
        self.map_note_label.pack(pady=12)

        # LEFT SIDE: ROOM INFORMATION
        self.room_text_frame = tk.Frame(
            self.room_view,
            bg=CARD
        )
        self.room_text_frame.pack(
            side="left",
            fill="both",
            expand=True,
            anchor="n"
        )

        self.section_label =tk.Label(
            self.room_text_frame,
            text="ROOM INFORMATION",
            font=("Arial", 13, "bold"),
            fg=MUTED,
            bg=CARD
        )
        self.section_label.pack(anchor="w", pady=(0, 15))

        self.room_code_label = tk.Label(
            self.room_text_frame,
            font=("Arial", 38, "bold"),
            fg=WHITE,
            bg=CARD
        )
        self.room_code_label.pack(anchor="w")

        # Staff contact information container
        self.staff_contact_frame = tk.Frame(
            self.room_text_frame,
            bg=CARD
        )

        # Staff photo
        self.staff_photo_label = tk.Label(
            self.staff_contact_frame,
            text="No photo",
            font=("Arial", 12),
            fg=MUTED,
            bg="#29405C",
            padx=15,
            pady=25
        )
        self.staff_photo_label.pack(
            side="left",
            padx=(0, 15)
        )

        # Staff email
        self.staff_email_label = tk.Label(
            self.staff_contact_frame,
            font=("Arial", 14),
            fg=BLUE,
            bg=CARD,
            wraplength=250,
            justify="left"
        )
        self.staff_email_label.pack(side="left")

        # Keep a reference to the photo
        self.staff_photo = None

        self.floor_label = tk.Label(
            self.room_text_frame,
            font=("Arial", 22, "bold"),
            fg=BLUE,
            bg=CARD
        )
        self.floor_label.pack(anchor="w", pady=(5, 25))

        self.type_heading_label=tk.Label(
            self.room_text_frame,
            text="ROOM TYPE",
            font=("Arial", 12, "bold"),
            fg=MUTED,
            bg=CARD
        )
        self.type_heading_label.pack(anchor="w")

        self.room_type_label = tk.Label(
            self.room_text_frame,
            font=("Arial", 18),
            fg=WHITE,
            bg=CARD
        )
        self.room_type_label.pack(
            anchor="w",
            pady=(5, 25)
        )

        tk.Label(
            self.room_text_frame,
            text="DIRECTIONS",
            font=("Arial", 12, "bold"),
            fg=BLUE,
            bg=CARD
        ).pack(anchor="w")

        self.directions_label = tk.Label(
            self.room_text_frame,
            font=("Arial", 17),
            fg=WHITE,
            bg=CARD,
            wraplength=430,
            justify="left"
        )
        self.directions_label.pack(
            anchor="w",
            pady=(8, 0)
        )
        #Appointment booking screen
        self.booking_view = tk.Frame(self.card, bg=CARD)
        self.booking_title = tk.Label(
            self.booking_view,
            text ="Available Appointments",
            font = ("Arial",28,"bold"),
            fg= WHITE,
            bg=CARD
        )
        self.booking_title.pack(pady=(20,10))
        self.booking_staff_label = tk.Label(
            self.booking_view,
            font= ("Arial",18),
            fg= BLUE,
            bg=CARD
        )
        self.booking_staff_label.pack(pady=10)
        #Container for appointment dates
        self.slots_frame = tk.Frame(
            self.booking_view,
            bg=CARD
        )
        self.slots_frame.pack(pady=10)

        # Information message for booking screen
        self.booking_note = tk.Label(
            self.booking_view,
            font=("Arial", 14),
            fg=MUTED,
            bg=CARD
        )
        self.booking_note.pack(pady=10)

        # Booking variables
        self.current_staff = None
        self.available_slots = []
        self.pending_slot = None

        # Warning message
        self.warning_label = tk.Label(
            self.root,
            text=(
                "Robot Receptionist may make mistakes. "
                "Please verify important information."
            ),
            font=("Arial", 11),
            fg=MUTED,
            bg=BG
        )
        self.warning_label.pack(pady=(0, 12))

        self.root.bind(
            "u",
            lambda e: self.handle_question("Where is the library?")
        )

        self.root.bind(
            "g",
            lambda e: self.handle_question("Thank you")
        )
        self.root.bind("a", lambda e: self.select_booking_slot(0))
        self.root.bind("0", lambda e: self.show_booking_slots())
        self.root.bind("1", lambda e: self.show_welcome())
        self.root.bind("2", lambda e: self.show_listening())
        self.root.bind("3", lambda e: self.show_thinking())

        self.root.bind("4", lambda e: self.show_room_from_db("MAE305"))
        self.root.bind("6", lambda e: self.show_room_from_db("MAE204"))
        self.root.bind("7", lambda e: self.show_room_from_db("MAE104"))
        # Confirm appointment
        self.root.bind("y", lambda e: self.confirm_booking())

        # Go back without booking
        self.root.bind("n", lambda e: self.cancel_booking_selection())
        self.root.bind(
            "5",
            lambda e: self.show_staff_from_db("Jen Joe")
        )

        self.root.bind(
            "8",
            lambda e: self.show_staff_from_db("Jen Dan")
        )

        self.root.bind(
            "9",
            lambda e: self.show_staff_from_db("Dash Tan")
        )
        self.root.bind(
            "<Escape>",
            lambda e: self.root.destroy()
        )

        self.show_welcome()

    # Updates the standard screen
    def update_screen(self, title, subtitle, info, status, colour):
        self.booking_view.pack_forget()
        self.room_view.pack_forget()
        self.standard_view.pack(
            fill="both",
            expand=True
        )

        self.title_label.config(text=title)
        self.subtitle_label.config(text=subtitle)
        self.info_label.config(text=info)

        self.status_label.config(
            text=status,
            fg=colour
        )

    # Welcome screen
    def show_welcome(self):
        self.update_screen(
            "Hello!",
            "How can I help you?",
            "Ask about rooms, staff offices or appointments.",
            "WAITING FOR VISITOR",
            BLUE
        )

    # Listening screen
    def show_listening(self):
        self.update_screen(
            "Listening...",
            "Please ask your question",
            "I'm listening to your request.",
            "LISTENING",
            PURPLE
        )

    # Thinking screen
    def show_thinking(self):
        self.update_screen(
            "Thinking...",
            "Finding information",
            "Please wait while I process your question.",
            "PROCESSING",
            YELLOW
        )


    # Displays room information
    def show_room_info(self, room_code, floor, room_type, directions):
        self.booking_view.pack_forget()
        room_code = room_code.strip().upper()

        # Hide staff photo and email
        self.staff_contact_frame.pack_forget()

        # Reset headings for Room Information
        self.section_label.config(text="ROOM INFORMATION")
        self.type_heading_label.config(text="ROOM TYPE")

        # Reset font sizes
        self.room_code_label.config(font=("Arial", 38, "bold"))
        self.floor_label.config(font=("Arial", 22, "bold"))

        # Hide standard screen
        self.standard_view.pack_forget()

        # Show room information
        self.room_view.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        # Update room details
        self.room_code_label.config(text=room_code)
        self.floor_label.config(text=f"Floor {floor}")
        self.room_type_label.config(text=room_type)
        self.directions_label.config(text=directions)

        # Update mini map
        self.map_title_label.config(text=f"Floor {floor} - Mini Map")
        self.draw_mini_map(room_code, floor)

        self.status_label.config(text="ROOM FOUND", fg=BLUE)
    def show_room_from_db(self,room_code):
        #get room information from SQLite
        room = get_room(room_code)
        #check whether the room exists
        if room is None:
            self.update_screen(
                "Room Not Found",
                "Sorry, I couldn't find this room.",
                "Please try another room number.",
                "NOT FOUND",
                YELLOW
            )
            return
        # Display room information and mini map
        self.show_room_info(*room)

    # Displays staff information
    def show_staff_info(
        self, name, role, room_code, floor,
        directions, email, photo_path
    ):

        # Reuse room information layout and mini map
        self.show_room_info(
            room_code,
            floor,
            "Staff Room",
            directions
        )

        # Update labels for staff information
        self.section_label.config(text="STAFF INFORMATION")

        self.room_code_label.config(
            text=name,
            font=("Arial", 28, "bold")
        )

        self.floor_label.config(
            text=f"Office {room_code} | Floor {floor}",
            font=("Arial", 18, "bold")
        )

        self.type_heading_label.config(text="ROLE")
        self.room_type_label.config(text=role)

        self.status_label.config(
            text="STAFF FOUND",
            fg=BLUE
        )

        self.map_note_label.config(
            text="Blue = selected office"
        )

        # Display staff email
        self.staff_email_label.config(
            text=email or "Email not available"
        )

        # Clear previous photo
        self.staff_photo = None

        # Load staff photo
        if photo_path:
            image_path = (
                Path(__file__).resolve().parent.parent
                / photo_path
            )

            if image_path.is_file():
                try:
                    photo = tk.PhotoImage(
                        file=str(image_path)
                    )

                    factor = max(
                        1,
                        (max(photo.width(), photo.height()) + 95) // 96
                    )

                    self.staff_photo = photo.subsample(
                        factor, factor
                    )

                except tk.TclError:
                    self.staff_photo = None

        # Display photo or placeholder
        if self.staff_photo is not None:
            self.staff_photo_label.config(
                image=self.staff_photo,
                text=""
            )
        else:
            self.staff_photo_label.config(
                image="",
                text="No photo"
            )

        # Display contact details under the name
        self.staff_contact_frame.pack(
            before=self.floor_label,
            anchor="w",
            pady=(8, 15)
        )

    # Retrieves staff information from SQLite
    def show_staff_from_db(self, full_name):

        staff = get_staff(full_name)

        if staff is None:
            self.current_staff = None
            self.update_screen(
                "Staff Not Found",
                "Sorry, I couldn't find this staff member.",
                "Please try another name.",
                "NOT FOUND",
                YELLOW
            )
            return

        self.current_staff = staff[0]

        self.show_staff_info(*staff)

    # Draws the mini map
    def draw_mini_map(self, room_code, floor):

        self.map_canvas.delete("all")

        # Draw corridor
        self.map_canvas.create_rectangle(
            122, 18, 178, 204,
            fill="#D1E2EF",
            outline=""
        )

        self.map_canvas.create_text(
            150, 110,
            text="CORRIDOR",
            angle=90,
            font=("Arial", 10, "bold"),
            fill="#52677E"
        )

        # Get rooms for the requested floor
        rooms = FLOOR_MAP_POSITIONS.get(floor, {})

        # Draw each room
        for code, coordinates in rooms.items():

            x1, y1, x2, y2 = coordinates

            selected = code == room_code

            colour = BLUE if selected else WHITE

            self.map_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=colour,
                outline="#315270",
                width=2 if selected else 1
            )

            self.map_canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=code,
                font=("Arial", 11, "bold"),
                fill=BG
            )

        # Show a message if the room has no map position
        if room_code not in rooms:
            self.map_note_label.config(
                text="Room location is not mapped yet."
            )
        else:
            self.map_note_label.config(
                text="Blue = selected room"
            )
    #Connect question understanding to Tkinter screens
    def handle_question(self,question):
        #understand the visitors questions
        intent, value = understand_question(question)

        #room enquiry
        if intent == "room":
            self.show_room_from_db(value)
        #staff enquiry
        if intent == "staff":
            self.show_staff_from_db(value)
        #appointment booking
        elif intent == "booking":
            if value is not None:
                self.show_staff_from_db(value)
                if self.current_staff is not None:
                    self.show_booking_slots()
            else:
                self.update_screen(
                    "Staff Required",
                    "Who would you like to meet?"
                    "Please mention a staff member's name."
                    "INFORMATION REQUIRED",
                    YELLOW
                )
        #End conservation
        elif intent == "goodbye":
            self.current_staff =None
            self.update_screen(
                "Goodbye!",
                "Have a great day!",
                "Thank you!",
                "SESSION ENDED",
                BLUE
            )
        #question not understood
        else:
            self.update_screen(
                "Sorry!",
                "I didn't understand your question.",
                "Please try asking again.",
                "NOT UNDERSTOOD",
                YELLOW
            )

    def run(self):
        self.root.mainloop()



    def show_booking_slots(self):

        if self.current_staff is None:
            return

        # Get available appointments from SQLite
        self.available_slots = get_available_slots(
            self.current_staff
        )

        self.pending_slot = None

        # Hide other screens
        self.standard_view.pack_forget()
        self.room_view.pack_forget()

        # Show booking screen
        self.booking_view.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        self.booking_title.config(
            text="Available Appointments"
        )

        self.booking_staff_label.config(
            text=f"Staff: {self.current_staff}"
        )

        # Clear previous labels
        for widget in self.slots_frame.winfo_children():
            widget.destroy()

        if not self.available_slots:
            tk.Label(
                self.slots_frame,
                text="No available appointments.",
                font=("Arial", 18),
                fg=WHITE,
                bg=CARD
            ).pack(pady=20)

            self.booking_note.config(
                text="No appointments available for this staff member."
            )
            return

        # Display appointment dates
        for slot_id, slot_time in self.available_slots:

            tk.Label(
                self.slots_frame,
                text=slot_time,
                font=("Arial", 20),
                fg=WHITE,
                bg="#29405C",
                width=35,
                pady=10
            ).pack(pady=5)

        self.booking_note.config(
            text="Press A to select the first available appointment."
        )

        self.status_label.config(
            text="APPOINTMENTS",
            fg=BLUE
        )
    def select_booking_slot(self, index):

        # Only work when booking screen is visible
        if not self.booking_view.winfo_ismapped():
            return

        if not self.available_slots:
            return

        if self.pending_slot is not None:
            return

        # Select the first available appointment
        self.pending_slot = self.available_slots[index]

        slot_id, slot_time = self.pending_slot

        # Clear appointment list
        for widget in self.slots_frame.winfo_children():
            widget.destroy()

        self.booking_title.config(
            text="Confirm Appointment"
        )

        tk.Label(
            self.slots_frame,
            text=f"{self.current_staff}\n\n{slot_time}",
            font=("Arial", 25, "bold"),
            fg=WHITE,
            bg=CARD,
            justify="center"
        ).pack(pady=60)

        self.booking_note.config(
            text="Press Y to confirm or N to go back."
        )

        self.status_label.config(
            text="CONFIRM BOOKING",
            fg=YELLOW
        )
    def confirm_booking(self):

        if self.pending_slot is None:
            return

        slot_id, slot_time = self.pending_slot

        # Save appointment to SQLite
        reference = book_appointment(slot_id)

        if reference is None:
            self.show_booking_slots()
            self.booking_note.config(
                text="Booking failed. Please try another appointment."
            )
            return

        # Get confirmation details
        details = get_booking_details(reference)

        self.pending_slot = None

        # Clear old screen content
        for widget in self.slots_frame.winfo_children():
            widget.destroy()

        self.booking_title.config(
            text="Appointment Confirmed!"
        )

        if details:
            ref, name, email, office, floor, date = details

            message = (
                f"Booking Number: {ref}\n\n"
                f"Staff: {name}\n"
                f"Email: {email or 'Not available'}\n"
                f"Office: {office or 'Not available'}\n"
                f"Floor: {floor}\n"
                f"Date & Time: {date}"
            )
        else:
            message = f"Booking Number: {reference}"

        tk.Label(
            self.slots_frame,
            text=message,
            font=("Arial", 19),
            fg=WHITE,
            bg=CARD,
            justify="left",
            wraplength=750
        ).pack(pady=30)

        self.booking_note.config(
            text="Please keep your booking number."
        )

        self.status_label.config(
            text="BOOKING CONFIRMED",
            fg=BLUE
        )
    def cancel_booking_selection(self):

        if self.pending_slot is not None:
            self.show_booking_slots()


if __name__ == "__main__":
    display = RobotDisplay()
    display.run()
