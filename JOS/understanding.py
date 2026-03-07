import spacy

print("[NLP] Loading Language Model (en_core_web_md)...")
nlp = spacy.load("en_core_web_md")

# =============================================================================
# STRICT KEYWORD RULES (Primary Pass)
# These catch unambiguous commands BEFORE cosine similarity runs.
# Each rule: list of trigger keywords -> forced intent
# =============================================================================
KEYWORD_RULES = [
    # (keywords_list, forced_intent)
    # Order matters: more specific phrases FIRST
    (["open file", "open folder", "open document", "find folder", "folder named", "file named", "document named", "folder called", "file called", "document called"], "OPEN_ITEM"),
    (["open ", "launch ", "start ", "run "],                       "OPEN_APP"),
    (["close ", "quit ", "terminate ", "kill "],                    "CLOSE_APP"),
    (["create ", "make ", "build "],                               "CREATE_ITEM"),
    (["delete ", "remove ", "erase ", "trash "],                    "DELETE_ITEM"),
    (["move ", "transfer ", "put ", "shift ", "send ", "relocate "], "MOVE_FILE"),
    (["volume", "mute", "unmute", "sound", "brightness", "dim", "screen"], "SYSTEM_CONTROL"),
]

# =============================================================================
# VECTOR ANCHORS (Secondary Pass / Fallback)
# Only used when strict keywords don't match.
# Stripped of ambiguous verbs to prevent overlap.
# =============================================================================
INTENTS = {
    "MOVE_FILE":       nlp("relocate file transfer document shift place organize send migrate destination folder"),
    "OPEN_APP":        nlp("open launch start application program software execute"),
    "CLOSE_APP":       nlp("close quit terminate end process kill task shut down window application"),
    "CREATE_ITEM":     nlp("create new folder make file add document generate build directory"),
    "DELETE_ITEM":     nlp("delete file remove folder destroy erase trash discard wipe purge"),
    "OPEN_ITEM":       nlp("open file find folder show document read text locate directory"),
    "SYSTEM_CONTROL":  nlp("volume brightness wifi sleep mute screen display sound audio power"),
    "EXIT":            nlp("end session goodbye bye good night see you later power off shut down system"),
}

# =============================================================================
# ACTION WORDS to strip from entity noun chunks
# =============================================================================
ACTION_WORDS = [
    "open ", "close ", "launch ", "start ", "run ", "play ",
    "stop ", "kill ", "exit ", "terminate ", "shut ", "quit ",
    "move ", "put ", "send ", "transfer ", "shift ",
    "increase ", "decrease ", "turn ", "set ", "change ",
    "create ", "make ", "new ", "add ", "generate ", "build ",
    "delete ", "remove ", "destroy ", "erase ", "trash ", "find ",
    "folder ", "file ", "document ", "named ", "called "
]


def _extract_entities(doc):
    """
    Shared entity extraction used by BOTH keyword and vector paths.
    Pulls noun chunks and proper nouns, strips determiners and action verbs.
    """
    entities = []

    for chunk in doc.noun_chunks:
        text = chunk.text.lower().strip()

        # Skip pronouns and wake word
        if text in ["jarvis", "i", "it", "me", "he", "she", "they", "them"]:
            continue

        # Clean determiners and leak words iteratively to handle nesting (e.g. "open the folder named")
        changed = True
        while changed:
            changed = False
            for prefix in ["the ", "a ", "an ", "my "] + ACTION_WORDS:
                if text.startswith(prefix):
                    text = text[len(prefix):].strip()
                    changed = True
                elif text == prefix.strip():
                    text = ""
                    changed = True

        if text:
            entities.append(text)

    # Fallback for Proper Nouns (like "Google Chrome")
    # Filter out action verbs that spaCy sometimes tags as NOUN/PROPN
    action_stems = {
        "open", "close", "launch", "start", "run", "play",
        "stop", "kill", "exit", "terminate", "shut", "quit",
        "move", "put", "send", "transfer", "shift", "relocate",
        "create", "make", "new", "add", "generate", "build",
        "delete", "remove", "destroy", "erase", "trash", "find",
        "folder", "file", "document", "named", "called"
    }
    for token in doc:
        if token.pos_ in ["PROPN", "NOUN"] and not token.is_stop:
            word = token.text.lower()
            if word in action_stems:
                continue
            if word not in " ".join(str(e) for e in entities):
                entities.append(word)

    # Extract numerical digits for hardware levels
    for token in doc:
        if token.like_num or token.pos_ == "NUM":
            if token.text.isdigit():
                num = int(token.text)
                if num not in entities:
                    entities.append(num)
            else:
                word = token.text.lower()
                if word not in " ".join(str(e) for e in entities):
                    entities.append(word)

    return entities


def understand_command(text):
    """
    Hybrid intent classification:
      Pass 1: Strict keyword matching for unambiguous commands
      Pass 2: Cosine similarity against vector anchors for nuanced phrasing
    Entity extraction runs on both paths via spaCy.
    """
    doc = nlp(text.lower())

    # =========================================================================
    # PASS 1: STRICT KEYWORD ROUTING
    # Fast, deterministic, zero ambiguity for direct commands.
    # =========================================================================
    for keywords, forced_intent in KEYWORD_RULES:
        for keyword in keywords:
            if keyword in text.lower():
                entities = _extract_entities(doc)
                
                # If SYSTEM_CONTROL, ensure key action words aren't filtered out
                if forced_intent == "SYSTEM_CONTROL":
                    sys_words = ["volume", "mute", "unmute", "sound", "brightness", "dim", "screen", "up", "down", "increase", "decrease", "reduce", "lower"]
                    for sw in sys_words:
                        if sw in text.lower() and sw not in entities:
                            entities.append(sw)
                            
                return {
                    "intent": forced_intent,
                    "entities": entities,
                    "confidence": 1.0,  # Keyword match = absolute confidence
                }

    # =========================================================================
    # PASS 2: VECTOR SIMILARITY (Fallback)
    # For commands that don't start with a clear verb.
    # e.g., "the budget report goes to documents" -> MOVE_FILE
    # =========================================================================
    clean_text = " ".join([
        token.text for token in doc
        if not token.is_stop and not token.is_punct
    ])
    clean_doc = nlp(clean_text)

    best_intent = None
    highest_score = 0.0

    for intent_name, anchor_doc in INTENTS.items():
        similarity = clean_doc.similarity(anchor_doc)
        if similarity > highest_score:
            highest_score = similarity
            best_intent = intent_name

    # Threshold Check
    if highest_score < 0.4:
        return None

    entities = _extract_entities(doc)

    return {
        "intent": best_intent,
        "entities": entities,
        "confidence": round(highest_score, 2),
    }


# =============================================================================
# SELF-TEST: Run with `python understanding.py`
# =============================================================================
if __name__ == "__main__":
    tests = [
        # OPEN_APP (keyword match)
        "open chrome",
        "open google chrome",
        "launch notepad",
        "start calculator",
        # CLOSE_APP (keyword match)
        "close notepad",
        "quit chrome",
        "terminate excel",
        # CREATE_ITEM (keyword match)
        "create a new folder called reports",
        "make a file named budget",
        # DELETE_ITEM (keyword match)
        "delete the test file",
        "remove the old folder",
        # SYSTEM_CONTROL (keyword match)
        "set volume to 50",
        "mute the sound",
        "increase screen brightness by 20",
        "dim the screen",
        # MOVE_FILE (vector fallback — no strict keyword)
        "put the financial report in the backup folder",
        "transfer my resume to documents",
        # Edge cases
        "open",
        "hello jarvis how are you",
    ]

    print("\n" + "=" * 60)
    print(" HYBRID NLP SELF-TEST")
    print("=" * 60)

    for t in tests:
        result = understand_command(t)
        if result:
            route = "KEYWORD" if result["confidence"] == 1.0 else "VECTOR"
            print(f"\n  Input:    '{t}'")
            print(f"  Route:    {route}")
            print(f"  Intent:   {result['intent']}")
            print(f"  Entities: {result['entities']}")
            print(f"  Conf:     {result['confidence']}")
        else:
            print(f"\n  Input:    '{t}'")
            print(f"  -> Below threshold, ignored.")