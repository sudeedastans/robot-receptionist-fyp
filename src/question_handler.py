
import re
from data.robot_database import get_room

STAFF_NAMES = [
    "Jen Joe",
    "Ahmad Lotfi",
    "Jen Dan",
    "Dash Tan"
]
def understand_question(question):
    text = question.lower().strip()
    #check ıf the vısıtor wants to end the conservation
    if "thank you" in text or "goodbye" in text:
        return "goodbye", None
    # Check which staff member is mentioned
    staff_name = None
    for name in STAFF_NAMES:
        if name.lower() in text:
            staff_name = name
            break
    #check ıf the vısıtor wants to an appointment
    if "appointment" in text or "book" in text:
        return "booking", staff_name

    #check ıf the vısıtor asks about a room
    room = re.search(r"\bmae\s*(\d{3})\b",text)
    if room:
        room_code = "MAE" + room.group(1)
        return "room", room_code
    #check ıf the vısıtor asks about staff
    if staff_name:
        return "staff", staff_name

    #question not undertood
    return "unknown",None


# Understands the visitor's question and retrieves room information.
def handle_question(question):

    if not question:
        return "Could you repeat your question?"

    # Searches for room codes such as MAE305 within the question.
    # re.IGNORECASE = ignores uppercase and lowercase differences.
    room_match = re.search(r"\bMAE\s*\d{3}\b", question, re.IGNORECASE)

    if room_match:
        # group = retrieves the matched room code
        # upper = converts letters to uppercase
        # replace = removes spaces
        room_code = room_match.group().upper().replace(" ", "")

        room = get_room(room_code)

        if room is not None:
            return f"{room[0]} is on floor {room[1]}. {room[3]}"

        return f"Sorry, I could not find room {room_code}."

    return "Sorry, I could not understand your question."


if __name__ == "__main__":
    question = "Where is MAE305?"
    answer = handle_question(question)
    print("Robot:", answer)
    print(understand_question("Where is MAE305?"))
    print(understand_question("Where is Jen Joe?"))
    print(understand_question("I want to book an appointment with Ahmad Lotfi"))
    print(understand_question("Thank you"))
    print(understand_question("aa you"))


