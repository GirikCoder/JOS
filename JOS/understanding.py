import spacy

print("[NLP] 🧠 Loading Language Model (en_core_web_md)...")
nlp = spacy.load("en_core_web_md")

# INTENT ANCHORS
INTENTS = {
    "MOVE_FILE": nlp("move file transfer document cut paste shift put place keep organize send"),
    "OPEN_APP": nlp("open app start program launch software run play"),
    "CLOSE_APP": nlp("close exit stop kill terminate shut down"),
    "SYSTEM_CONTROL": nlp("volume brightness wifi sleep mute off"),
    "EXIT": nlp("end session stop listening bye goodbye shut down power off let's work tomorrow good night see you later")
}

def understand_command(text):
    doc = nlp(text.lower())
    
    # 1. INTENT (Clean text first)
    clean_text = " ".join([token.text for token in doc if not token.is_stop and not token.is_punct])
    clean_doc = nlp(clean_text)

    best_intent = None
    highest_score = 0.0
    
    for intent_name, anchor_doc in INTENTS.items():
        similarity = clean_doc.similarity(anchor_doc)
        if similarity > highest_score:
            highest_score = similarity
            best_intent = intent_name

    # Threshold Check (0.4)
    if highest_score < 0.4:
        return None

    # 2. ENTITY EXTRACTION (The Fix)
    entities = []
    
    for chunk in doc.noun_chunks:
        text = chunk.text.lower().strip()
        
        # FIX: Check EXACT word match, not substring
        # "file" contains "i", but it is NOT equal to "i". So it survives.
        if text in ["jarvis", "i", "it", "me", "he", "she", "they", "them"]:
            continue
            
        # Clean prefixes
        for prefix in ["the ", "a ", "an ", "my "]:
            if text.startswith(prefix):
                text = text[len(prefix):]
        
        if text: 
            entities.append(text)

    # Fallback for Proper Nouns (like "Google Chrome")
    for token in doc:
        if token.pos_ in ["PROPN", "NOUN"] and not token.is_stop:
            # Add if not already captured by chunks
            if token.text not in " ".join(entities):
                entities.append(token.text)

    return {
        "intent": best_intent,
        "entities": entities,
        "confidence": round(highest_score, 2)
    }
if __name__ == "__main__":
    # Test the bug fix immediately
    test = "put the financial report in the backup folder"
    print(f"Testing: '{test}'")
    print(understand_command(test))
    
    test2 = "open google chrome"
    print(f"Testing: '{test2}'")
    print(understand_command(test2))