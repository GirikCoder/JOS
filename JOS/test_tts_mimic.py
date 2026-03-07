import os
from mouth import JarvisMouth
import time

def test_tts_mimic():
    mouth = JarvisMouth()
    
    print("Testing pre-execution speech...")
    mouth.speak("Do you want to open notepad?")
    time.sleep(1)
    
    print("Simulating user saying yes...")
    print(">>> EXECUTE: OPEN_APP")
    print("Entities: ['notepad']")
    
    # Mimic hands.py logic
    success, message = mimic_open_app(['notepad'])
    
    print("hands.py returned:", success, message)
    if success:
        mouth.speak(message)
    else:
        mouth.speak(f"Failed. {message}")

def mimic_open_app(entities):
    spoken_name = "notepad"
    exe_name = "notepad.exe"
    try:
        os.startfile(exe_name)
        return True, f"{spoken_name.capitalize()} opened."
    except Exception as e:
        return False, f"Something went wrong while trying to open {spoken_name}."

if __name__ == "__main__":
    test_tts_mimic()
