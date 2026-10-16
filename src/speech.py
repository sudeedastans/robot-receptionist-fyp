import subprocess
import speech_recognition as sr
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
def greet():
    print("Hello")
    subprocess.run(["say","Hello how can I help you"])