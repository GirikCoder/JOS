import speech_recognition as sr
import whisper
import os

def listen_and_Trans():
    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 2.0

    print("Loading the Brain")
    model = whisper.load_model("base")
    print("Model Loaded")

    with sr.Microphone() as source:
        print("\nListening ...")
        audio_data = recognizer.listen(source)
        print("Transcribing")

        with open("temp.wav", "wb") as f:
            f.write(audio_data.get_wav_data())

    result = model.transcribe("temp.wav")
    text = result["text"]

    print(f"You said: {text.strip()}")

    if os.path.exists("temp.wav"):
        os.remove("temp.wav")

    return text

if __name__ == "__main__":
    listen_and_Trans()