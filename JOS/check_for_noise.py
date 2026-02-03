import speech_recognition as sr
import audioop
import sys

def list_microphones():
    print("Searching for microphones...")
    mics = sr.Microphone.list_microphone_names()
    
    print("\nAvailable Microphones:")
    print("----------------------")
    for index, name in enumerate(mics):
        print(f"ID: {index} | Name: {name}")
    print("----------------------")

def print_sound_level():
    print("Opening Microphone... (Press Ctrl+C to stop)")
        
    r = sr.Recognizer()
    
    # We open the mic just to get access to the raw data stream
    with sr.Microphone() as source:
        print("\n=== AUDIO ENERGY METER ===")
        print("Quiet Room:   0 - 100")
        print("Noisy Room:   100 - 1000")
        print("Speech:       3000 - 15000+")
        print("==========================\n")
        
        while True:
            # 1. Read a tiny chunk of audio (raw data)
            # source.stream is the raw connection to PyAudio
            buffer = source.stream.read(source.CHUNK)
            
            # 2. Calculate the 'Energy' (RMS - Root Mean Square) of that chunk
            # This number represents the "Loudness"
            energy = audioop.rms(buffer, source.SAMPLE_WIDTH)
            
            # 3. Create a visual bar for the terminal
            bars = "|" * int(energy / 500)  # One bar for every 500 energy units
            
            # 4. Print it on the same line (so it animates)
            # \r returns the cursor to the start of the line
            sys.stdout.write(f"\rEnergy: {energy:5d} {bars}")
            sys.stdout.flush()

if __name__ == "__main__":
    try:
        print_sound_level()
    except KeyboardInterrupt:
        print("\n\nStopped.")