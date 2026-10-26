import subprocess
import speech_recognition as sr
import whisper
import tempfile
import os

# Loads the local Whisper model once when the module starts.
model = whisper.load_model("base.en")

# greets the visitor using macos text-to-speech system.
def greet():
    print("Hello")
    subprocess.run(["say","Hello how can I help you"])

#records the visitors speech and converts it to text using local whisper.
def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)

        #create a temporary WAV file for the recorded audio.
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete= False
        )as temp_audio:
            temp_audio.write(audio.get_wav_data())
            audio_path = temp_audio.name
        #transcribe the audio locally using whisper
        result = model.transcribe(
            audio_path,
            language= "en",
            fp16 = False
        )
        #extract and clean the recognised text.
        text = result ["text"].strip().lower()
        print("Vistior said: ",text)

        #delete the temporary audio file.
        os.remove(audio_path)

        return text
    except sr.WaitTimeoutError:
        print("No speech detected")
        return None
    except sr.UnknownValueError:
        print("Could not understand speech")
        return None
    except sr.RequestError:
        print("Speech recognition service unavailable")
        return None


#allows thıs file to be tested independently from the main program.
if __name__ == "__main__":
    greet()
    question = listen()
    print("Recognised question:", question)