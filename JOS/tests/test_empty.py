import os
from mouth import JarvisMouth

def test_empty():
    mouth = JarvisMouth()
    mouth.speak("Testing empty strings...")
    
    msg = ""
    mouth.speak(msg)
    
    mouth.speak("Testing lists...")
    msg2 = ["notepad"]
    mouth.speak(str(msg2))
    
    mouth.speak("Done.")

if __name__ == "__main__":
    test_empty()
