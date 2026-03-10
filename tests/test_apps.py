"""
Test script for OPEN_APP and CLOSE_APP — no mic/voice needed.
Opens Notepad, waits 3 seconds, closes it. Then tests a fake app.
"""
import time
from hands import JarvisHands

hands = JarvisHands()

# --- TEST 1: Open Notepad ---
print("=" * 50)
print("[TEST 1] Open 'notepad'")
print("=" * 50)
success, message = hands.open_app(["notepad"])
print(f"  Success: {success}")
print(f"  Message: {message}")

# Wait 3 seconds so you can see Notepad open
print("\n  (Waiting 3 seconds so you can see it...)\n")
time.sleep(3)

# --- TEST 2: Close Notepad ---
print("=" * 50)
print("[TEST 2] Close 'notepad'")
print("=" * 50)
success2, message2 = hands.close_app(["notepad"])
print(f"  Success: {success2}")
print(f"  Message: {message2}")

# --- TEST 3: Open a fake app ---
print("\n" + "=" * 50)
print("[TEST 3] Open 'fakeapp' (should fail gracefully)")
print("=" * 50)
success3, message3 = hands.open_app(["fakeapp"])
print(f"  Success: {success3}")
print(f"  Message: {message3}")

# --- TEST 4: Close an app that isn't running ---
print("\n" + "=" * 50)
print("[TEST 4] Close 'calculator' (not running, should fail gracefully)")
print("=" * 50)
success4, message4 = hands.close_app(["calculator"])
print(f"  Success: {success4}")
print(f"  Message: {message4}")

print("\n" + "=" * 50)
print("All tests complete.")
print("=" * 50)
