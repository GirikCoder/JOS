import os
from mouth import JarvisMouth
import time

def test_tts_blocking():
    print("Testing pre-execution speech...")
    mouth = JarvisMouth()
    mouth.speak("Do you want to open notepad?")
    
    print("Simulating user saying yes...")
    time.sleep(1)
    
    print("Executing os.startfile...")
    try:
        os.startfile("notepad.exe")
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")
        
    print("Testing post-execution speech...")
    mouth.speak("Notepad opened.")
    print("Finished.")

if __name__ == "__main__":
    test_tts_blocking()
