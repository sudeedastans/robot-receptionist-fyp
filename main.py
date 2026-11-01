import src.speech as speech
import src.vision as vision

# defines what the robot should do when a new visitor is detected.
# the robot greets the visitor and then listens for a spoken question.
def handle_visitor():
    print("Visitor detected!")

    speech.greet()

    question = speech.listen()

    if question is not None:
        print("Visitor question:", question)

#starts the robot and activates visitor monitoring
def main():
    print("Robot Receptionist is ready!")

    vision.watch_for_visitors(handle_visitor)

#runs the main program only when this file is executed directly.
if __name__ == "__main__":
    main()