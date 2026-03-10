import speech_recognition as sr
import os

# CONFIGURATION
FILENAME = "voice_input.wav"

# GLOBAL VARIABLES (To remember settings between loops)
recognizer = None
microphone = None

def init_ears():
    """
    Run this ONLY ONCE at the start.
    It sets up the microphone and calculates noise level.
    """
    global recognizer, microphone
    
    print("\n[EARS] 🎤 Initializing Microphone...")
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # SETTINGS
    recognizer.pause_threshold = 0.8   # Stop recording after 0.8s of silence
    recognizer.dynamic_energy_threshold = False # Turn OFF dynamic adjustment after calibration
    
    with microphone as source:
        print("[EARS] 👂 Calibrating Noise... (Please be quiet for 1 sec)")
        # This runs ONCE. It measures your room's silence.
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        
        raw_noise = recognizer.energy_threshold
        print(f"[EARS] 📊 Ambient Noise Detected: {raw_noise:.2f}")
        # We boost the threshold slightly to prevent random background noise triggers
        # (Current noise level + 50 buffer)
        recognizer.energy_threshold += 50
        
        print(f"[EARS] ✅ Calibrated! Threshold set to: {int(recognizer.energy_threshold)}")

def listen():
    """
    Listens immediately using the saved settings.
    No delay. No re-calibration.
    """
    # Safety check: Did you run init_ears()?
    if recognizer is None:
        print("[EARS] ❌ ERROR: You must run init_ears() first!")
        return False

    try:
        with microphone as source:
            print("\n[EARS] 👂 Listening... ", end="", flush=True)
            
            # This listens IMMEDIATELY. No waiting.
            # timeout=5 means "If no one speaks for 5s, give up" (Prevents hanging forever)
            try:
                audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("(No speech detected)")
                return False
            
            print("🛑 Got it.")
            
            # Save to WAV
            with open(FILENAME, "wb") as f:
                f.write(audio_data.get_wav_data())
            
            return True # Audio Saved

    except Exception as e:
        print(f"\n[EARS] ❌ Error: {e}")
        return False