from mouth import JarvisMouth

def test_speech():
    print("[SYSTEM] Starting audio diagnostic...")
    mouth = JarvisMouth()
    
    phrases = [
        "System audio initialized successfully.",
        "I am ready to assist you, sir. What would you like to do today?",
        "Warning: Attempting to move a file that already exists."
    ]
    
    for phrase in phrases:
        mouth.speak(phrase)
        
    print("PASS: Audio diagnostic complete.")

if __name__ == "__main__":
    test_speech()
