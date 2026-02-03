import ears
import brain
import sys

def main_system():
    # --- STEP 0: SETUP (Run Once) ---
    print("\n[SYSTEM] ✅ Jarvis System Online.")
    
    # Initialize the ears (Calibrate noise floor)
    ears.init_ears()
    
    print("[SYSTEM] Status: ASLEEP (Waiting for 'Jarvis')...")
    
    is_awake = False
    
    while True:
        # --- STEP 1: LISTEN ---
        # Now this function is fast. It doesn't calibrate again.
        recorded = ears.listen()
        
        if recorded:
            # --- STEP 2: THINK ---
            command = brain.transcribe()
            
            # Garbage Handler
            if command is None:
                if is_awake:
                    print(">>> [JARVIS]: I didn't catch that.")
                else:
                    pass 
                continue 

            print(f"\n[USER SAYS]: {command}")
            
            # --- STEP 3: LOGIC ---
            
            # 1. ASLEEP MODE
            if not is_awake:
                if "jarvis" in command:
                    is_awake = True
                    print(">>> ✅ WAKE WORD DETECTED! <<")
                    print(">>> [JARVIS]: Online. What do you need?")
                else:
                    # Ignore commands if asleep
                    pass 
            
            # 2. AWAKE MODE
            else:
                # KILL SWITCH
                if "exit program" in command or "shut down" in command:
                    print(">>> [JARVIS]: Shutting down system. Goodbye.")
                    break
                
                # SLEEP SWITCH
                elif "go to sleep" in command or "that is all" in command:
                    is_awake = False
                    print(">>> [JARVIS]: Going to sleep.")
                    print("-" * 40)
                
                # ACTION
                else:
                    print(f">>> [JARVIS]: Working on it... (Simulated Action: {command})")
                    print(">>> [JARVIS]: Done. What's next?")

if __name__ == "__main__":
    main_system()