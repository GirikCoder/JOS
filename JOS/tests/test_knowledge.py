import time
from hands import JarvisHands

def run_test():
    print("="*50)
    print("[KNOWLEDGE] PIPELINE DIAGNOSTIC TEST")
    print("="*50)
    
    hands = JarvisHands()
    
    # 3. Test a successful query: hands.ask_wikipedia(["Nikola Tesla"])
    print("\nAttempting to query 'Nikola Tesla' (Standard Request)...")
    success_tesla, msg_tesla = hands.ask_wikipedia(["Nikola Tesla"])
    if success_tesla:
        print(f"[PASS] - {msg_tesla}")
    else:
        print(f"[FAIL] - {msg_tesla}")
        
    time.sleep(2)
    
    # 4. Test a Disambiguation Error: hands.ask_wikipedia(["Mercury"])
    print("\nAttempting to query 'Mercury' (Disambiguation Expected)...")
    success_apple, msg_apple = hands.ask_wikipedia(["Mercury"])
    # A successful catch of disambiguation returns False success but handled string.
    if success_apple is False and "too broad" in msg_apple.lower():
        print(f"[PASS] - Successfully caught Disambiguation: {msg_apple}")
    else:
        print(f"[FAIL] - Did not catch properly: {msg_apple}")
        
    time.sleep(2)
    
    # 5. Test a Page Error: hands.ask_wikipedia(["alksdjfalkjsdf"])
    print("\nAttempting to query 'alksdjfalkjsdf' (PageError Expected)...")
    success_page, msg_page = hands.ask_wikipedia(["alksdjfalkjsdf"])
    if success_page is False and ("records matching" in msg_page.lower() or "find" in msg_page.lower()):
        print(f"[PASS] - Successfully caught PageError: {msg_page}")
    else:
        print(f"[FAIL] - Did not catch properly: {msg_page}")
        
    print("\n" + "="*50)
    print("Test Sequence Complete.")
    print("="*50)

if __name__ == "__main__":
    run_test()
