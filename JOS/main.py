import ears
import brain
import understanding
import sys
from hands import JarvisHands
from mouth import JarvisMouth

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
    mouth = JarvisMouth()

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
                    mouth.speak("Online. I'm listening.")
                else:
                    pass 
            
            # --- STATE 2: CONFIRMATION MODE ---
            elif pending_action is not None:
                if any(word in text for word in ["yes", "proceed", "okay", "do it","sure"]):
                    intent = pending_action['intent']
                    entities = pending_action['entities']

                    if intent == "EXIT":
                        mouth.speak("Goodbye, Sir.")
                        mouth.wait_until_done()
                        sys.exit()

                    elif intent == "MOVE_FILE":
                        print(f">>> EXECUTE: MOVE_FILE")
                        print(f"    Entities: {entities}")
                        success, message = hands.move_file(entities)
                        if success:
                            mouth.speak(message)
                        else:
                            mouth.speak(f"Failed. {message}")

                    elif intent == "OPEN_APP":
                        print(f">>> EXECUTE: OPEN_APP")
                        print(f"    Entities: {entities}")
                        success, message = hands.open_app(entities)
                        if success:
                            mouth.speak(message)
                        else:
                            mouth.speak(f"Failed. {message}")

                    elif intent == "OPEN_ITEM":
                        print(f">>> EXECUTE: OPEN_ITEM")
                        print(f"    Entities: {entities}")
                        success, message = hands.open_item(entities)
                        if success:
                            mouth.speak(message)
                        else:
                            mouth.speak(f"Failed. {message}")

                    elif intent == "CLOSE_APP":
                        print(f">>> EXECUTE: CLOSE_APP")
                        print(f"    Entities: {entities}")
                        success, message = hands.close_app(entities)
                        if success:
                            mouth.speak(message)
                        else:
                            mouth.speak(f"Failed. {message}")

                    elif intent == "CREATE_ITEM":
                        print(f">>> EXECUTE: CREATE_ITEM")
                        print(f"    Entities: {entities}")
                        success, message = hands.create_item(entities)
                        if success:
                            mouth.speak(message)
                        else:
                            mouth.speak(f"Failed. {message}")

                    elif intent == "DELETE_ITEM":
                        print(f">>> EXECUTE: DELETE_ITEM")
                        print(f"    Entities: {entities}")
                        success, message = hands.delete_item(entities)
                        if success:
                            mouth.speak(message)
                        else:
                            mouth.speak(f"Failed. {message}")

                    elif intent == "SYSTEM_CONTROL":
                        print(f">>> EXECUTE: SYSTEM_CONTROL")
                        print(f"    Entities: {entities}")
                        success, message = hands.system_control(entities)
                        if success:
                            mouth.speak(message)
                        else:
                            mouth.speak(f"Failed. {message}")

                    else:
                        mouth.speak(f"I know the intent is {intent}, but I can't execute it yet.")

                    pending_action = None
                    
                elif any(word in text for word in ["no", "cancel", "stop", "abort","wait","don't"]):
                    mouth.speak("Cancelled. What else?")
                    pending_action = None
                
                else:
                    mouth.speak("Please say 'Yes' to proceed or 'No' to cancel.")

            # --- STATE 3: AWAKE ---
            else:
                # 1. CRITICAL COMMANDS (Override NLP)
                # We check these FIRST so they never fail.
                if "go to sleep" in text:
                    is_awake = False
                    mouth.speak("Sleeping.")
                    mouth.wait_until_done()
                    continue
                if any(word in text for word in ["stop listening", "go to sleep"]):
                    is_awake = False
                    mouth.speak("Sleeping.")
                    mouth.wait_until_done()
                    continue

                if any(word in text for word in ["exit", "shut down", "shutdown", "power off"]):
                    mouth.speak("Goodbye.")
                    mouth.wait_until_done()
                    sys.exit()

                # 2. NLP ANALYSIS
                analysis = understanding.understand_command(text)
                
                if analysis:
                    intent = analysis['intent']
                    confidence = analysis['confidence']
                    entities = analysis['entities']
                    
                    print(f"    (Debug: Intent={intent}, Conf={confidence})")

                    # DANGEROUS COMMANDS -> REQUIRE CONFIRMATION
                    if intent in ["MOVE_FILE", "OPEN_APP", "CLOSE_APP", "CREATE_ITEM", "DELETE_ITEM", "SYSTEM_CONTROL", "EXIT", "OPEN_ITEM"]:
                        if intent == "EXIT":
                            mouth.speak("Do you want to shut down the system?")
                        elif intent == "SYSTEM_CONTROL":
                            setting = " ".join([str(e) for e in entities])
                            mouth.speak(f"Do you want to adjust the system {setting}? Yes or no?")
                        elif intent == "OPEN_APP":
                            app_name = " ".join([str(e) for e in entities])
                            if app_name:
                                mouth.speak(f"Do you want to open {app_name}?")
                            else:
                                mouth.speak("Do you want to open the app?")
                        elif intent == "OPEN_ITEM":
                            item_name = " ".join([str(e) for e in entities])
                            if item_name:
                                mouth.speak(f"Do you want to open {item_name}?")
                            else:
                                mouth.speak("Do you want to open the item?")
                        elif intent == "CLOSE_APP":
                            app_name = " ".join([str(e) for e in entities])
                            if app_name:
                                mouth.speak(f"Do you want to close {app_name}?")
                            else:
                                mouth.speak("Do you want to close the app?")
                        elif intent == "CREATE_ITEM":
                            item_name = " ".join([str(e) for e in entities])
                            if item_name:
                                mouth.speak(f"Do you want to create {item_name}?")
                            else:
                                mouth.speak("Do you want to create the item?")
                        elif intent == "DELETE_ITEM":
                            item_name = " ".join([str(e) for e in entities])
                            if item_name:
                                mouth.speak(f"Do you want to delete {item_name}?")
                            else:
                                mouth.speak("Do you want to delete the item?")
                        elif intent == "MOVE_FILE":
                            if len(entities) >= 2:
                                mouth.speak(f"Do you want to move {entities[0]} to {entities[1]}?")
                            elif len(entities) == 1:
                                mouth.speak(f"Do you want to move {entities[0]}?")
                            else:
                                mouth.speak("Do you want to move the file?")
                        else:
                            mouth.speak(f"You want to {intent}. Correct?")
                        pending_action = analysis 
                    else:
                        mouth.speak("I understood the intent, but I don't know how to execute it yet.")
                
                # 3. FALLBACK (If NLP failed)
                else:
                    # PREVIOUSLY: print("Done.")  <-- THIS WAS THE BUG
                    # NOW: Be honest.
                    mouth.speak("I didn't understand that command. Can you rephrase?")

            # 4. WAIT FOR SPEECH TO FINISH
            # CRITICAL: Prevent the microphone from cutting off Jarvis mid-sentence
            mouth.wait_until_done()

if __name__ == "__main__":
    main_system()