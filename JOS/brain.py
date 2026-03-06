import whisper
import warnings
import os
import torch
import string  # New import to handle punctuation removal

# --- CONFIGURATION ---
FILENAME = "voice_input.wav"
MODEL_TYPE = "small"  

# Filter warnings
warnings.filterwarnings("ignore")

print(f"[BRAIN] 🧠 Loading AI Model ('{MODEL_TYPE}')...")
try:
    model = whisper.load_model(MODEL_TYPE)
except Exception as e:
    print(f"\n❌ ERROR: Could not download model.\nError: {e}")
    exit()

def transcribe():
    """
    Returns clean, lowercase, punctuation-free text.
    """
    if not os.path.exists(FILENAME):
        return None

    # Load audio
    audio = whisper.load_audio(FILENAME)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Decode
    options = whisper.DecodingOptions(
        fp16=False,
        language="en", 
        temperature=0.0, 
        beam_size=5, 
        without_timestamps=True
    )
    
    try:
        result = model.decode(mel, options)
    except Exception as e:
        print(f"[BRAIN] ❌ Error: {e}")
        return None

    if result.no_speech_prob > 0.4:
        return None

    text = result.text.strip()
    
    # --- CRITICAL FIX: CLEANING ---
    # 1. Lowercase everything ("Jarvis" -> "jarvis")
    text = text.lower()
    
    # 2. Remove Punctuation ("jarvis?" -> "jarvis")
    # This removes ., ?, !, etc.
    text = text.translate(str.maketrans('', '', string.punctuation))
   
    hallucinations = [
        "thank you", "thanks for watching", "subscribe", 
        "copyright", "amara", "sightseeing", "you", "silence"
    ]
    
    if not text or len(text) < 2:
        return None
        
    for h in hallucinations:
        if text.startswith(h):
            return None
            
    return text

if __name__ == "__main__":
    print(transcribe())