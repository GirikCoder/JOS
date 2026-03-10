"""
Automated Hardware Diagnostic Test for JOS
Verifies Volume and Brightness controls using pycaw and screen-brightness-control.
"""
import time
from hands import JarvisHands

hands = JarvisHands()

print("\n" + "=" * 60)
print("  JOS SYSTEM CONTROL - HARDWARE DIAGNOSTIC")
print("=" * 60)

commands = [
    ("Mute the system", ["volume", "mute"]),
    ("Unmute the system", ["volume", "unmute"]),
    ("Set volume to 30%", ["volume", 30]),
    ("Set volume to 70%", ["volume", 70]),
    ("Set screen brightness to 50%", ["brightness", 50]),
    ("Set screen brightness to 100%", ["brightness", 100])
]

for description, entities in commands:
    print(f"\n--- Testing: {description} ---")
    print(f"  Entities: {entities}")
    success, msg = hands.system_control(entities)
    
    if success:
        print(f"  [+] PASS: {msg}")
    else:
        print(f"  [X] FAIL: {msg}")
        
    print("  (Waiting 3 seconds...)")
    time.sleep(3)

print("\n" + "=" * 60)
print("  HARDWARE TESTS COMPLETE")
print("=" * 60)
