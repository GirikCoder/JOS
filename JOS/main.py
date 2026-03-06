import ears
import brain
import understanding
import sys
from hands import JarvisHands

def main_system():
    # --- SETUP ---
    print("\n[SYSTEM] ⏳ Initializing Jarvis...")
    ears.init_ears()
    
    print("[SYSTEM] 🧠 Connecting Neural Pathways...") 
    
    print("\n" + "="*50)
    print("[SYSTEM] ✅ SYSTEM ONLINE.")
    print("[SYSTEM] Status: ASLEEP (Say 'Jarvis' to wake).")
    print("="*50)
    
    # STATE VARIABLES
    is_awake = False
    pending_action = None
    hands = JarvisHands()

    while True:
        # 1. LISTEN
        recorded = ears.listen()
        
        if recorded:
            # 2. TRANSCRIBE
            text = brain.transcribe()
            
            if not text:
                continue 

            print(f"\n[USER]: \"{text}\"")
            
            # --- STATE 1: ASLEEP ---
            if not is_awake:
                if "jarvis" in text:
                    is_awake = True
                    print(">>> ✅ JARVIS: Online. I'm listening.")
                else:
                    pass 
            
            # --- STATE 2: CONFIRMATION MODE ---
            elif pending_action is not None:
                if any(word in text for word in ["yes", "proceed", "okay", "do it","sure"]):
                    intent = pending_action['intent']
                    entities = pending_action['entities']

                    if intent == "EXIT":
                        print(">>> [JARVIS]: Goodbye, Sir.")
                        sys.exit()

                    elif intent == "MOVE_FILE":
                        print(f">>> EXECUTE: MOVE_FILE")
                        print(f"    Entities: {entities}")
                        success, message = hands.move_file(entities)
                        if success:
                            print(f">>> [JARVIS]: {message}")
                        else:
                            print(f">>> [JARVIS]: Failed. {message}")

                    elif intent == "OPEN_APP":
                        print(f">>> EXECUTE: OPEN_APP")
                        print(f"    Entities: {entities}")
                        success, message = hands.open_app(entities)
                        if success:
                            print(f">>> [JARVIS]: {message}")
                        else:
                            print(f">>> [JARVIS]: Failed. {message}")

                    elif intent == "CLOSE_APP":
                        print(f">>> EXECUTE: CLOSE_APP")
                        print(f"    Entities: {entities}")
                        success, message = hands.close_app(entities)
                        if success:
                            print(f">>> [JARVIS]: {message}")
                        else:
                            print(f">>> [JARVIS]: Failed. {message}")

                    elif intent == "CREATE_ITEM":
                        print(f">>> EXECUTE: CREATE_ITEM")
                        print(f"    Entities: {entities}")
                        success, message = hands.create_item(entities)
                        if success:
                            print(f">>> [JARVIS]: {message}")
                        else:
                            print(f">>> [JARVIS]: Failed. {message}")

                    elif intent == "DELETE_ITEM":
                        print(f">>> EXECUTE: DELETE_ITEM")
                        print(f"    Entities: {entities}")
                        success, message = hands.delete_item(entities)
                        if success:
                            print(f">>> [JARVIS]: {message}")
                        else:
                            print(f">>> [JARVIS]: Failed. {message}")

                    else:
                        # Placeholder for SYSTEM_CONTROL
                        print(f">>> [JARVIS]: I know the intent is {intent}, but I can't execute it yet.")

                    pending_action = None
                    
                elif any(word in text for word in ["no", "cancel", "stop", "abort","wait","don't"]):
                    print(">>> [JARVIS]: Cancelled. What else?")
                    pending_action = None
                
                else:
                    print(">>> [JARVIS]: Please say 'Yes' to proceed or 'No' to cancel.")

            # --- STATE 3: AWAKE ---
            else:
                # 1. CRITICAL COMMANDS (Override NLP)
                # We check these FIRST so they never fail.
                if "go to sleep" in text:
                    is_awake = False
                    print(">>> [JARVIS]: Sleeping.")
                    continue
                if any(word in text for word in ["stop listening", "go to sleep"]):
                    is_awake = False
                    print(">>> [JARVIS]: Sleeping.")
                    continue

                if any(word in text for word in ["exit", "shut down", "shutdown", "power off"]):
                    print(">>> [JARVIS]: Goodbye.")
                    sys.exit()

                # 2. NLP ANALYSIS
                analysis = understanding.understand_command(text)
                
                if analysis:
                    intent = analysis['intent']
                    confidence = analysis['confidence']
                    entities = analysis['entities']
                    
                    print(f"    (Debug: Intent={intent}, Conf={confidence})")

                    # DANGEROUS COMMANDS -> REQUIRE CONFIRMATION
                    if intent in ["MOVE_FILE", "OPEN_APP", "CLOSE_APP", "CREATE_ITEM", "DELETE_ITEM", "SYSTEM_CONTROL", "EXIT"]:
                        if intent == "EXIT":
                            print(">>> [JARVIS]: Do you want to shut down the system?")
                        else:
                            print(f">>> [JARVIS]: You want to {intent}: {entities}. Correct?")
                        pending_action = analysis 
                    else:
                        print(">>> [JARVIS]: I understood the intent, but I don't know how to execute it yet.")
                
                # 3. FALLBACK (If NLP failed)
                else:
                    # PREVIOUSLY: print("Done.")  <-- THIS WAS THE BUG
                    # NOW: Be honest.
                    print(">>> [JARVIS]: I didn't understand that command. Can you rephrase?")

if __name__ == "__main__":
    main_system()