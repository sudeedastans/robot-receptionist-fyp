
import re
from data.robot_database import get_room


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
