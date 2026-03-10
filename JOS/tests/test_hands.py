
import time
from hands import JarvisHands

hands = JarvisHands()
desktop = hands.safe_zones["desktop"]
documents = hands.safe_zones["documents"]

print("\n--- SYSTEM PATHS ---")
print(f"Desktop Path:   {desktop}")
print(f"Documents Path: {documents}\n")

# --- TEST 1: Create a folder on Desktop ---
print("=" * 50)
print("[TEST 1] Create folder 'jarvis_test_folder' on Desktop")
print("=" * 50)
success, message = hands.create_item(["jarvis_test_folder folder"])
print(f"  Success: {success}")
print(f"  Message: {message}")

# --- TEST 2: Create a file in Documents ---
print("\n" + "=" * 50)
print("[TEST 2] Create file 'jarvis_test_file' in Documents")
print("=" * 50)
success2, message2 = hands.create_item(["jarvis_test_file", "documents"])
print(f"  Success: {success2}")
print(f"  Message: {message2}")

# --- TEST 3: Try to create a duplicate (should fail) ---
print("\n" + "=" * 50)
print("[TEST 3] Create duplicate 'jarvis_test_file' in Documents (should fail)")
print("=" * 50)
success3, message3 = hands.create_item(["jarvis_test_file", "documents"])
print(f"  Success: {success3}")
print(f"  Message: {message3}")

# --- PAUSE: Let the user verify ---
print("\n" + "=" * 50)
print("[PAUSE] Check your Desktop and Documents now...")
print("  -> Desktop should have: jarvis_test_folder/")
print("  -> Documents should have: jarvis_test_file.txt")
print("=" * 50)
time.sleep(3)

# --- TEST 4: Delete the folder ---
print("\n" + "=" * 50)
print("[TEST 4] Delete 'jarvis_test_folder'")
print("=" * 50)
success4, message4 = hands.delete_item(["jarvis_test_folder"])
print(f"  Success: {success4}")
print(f"  Message: {message4}")

# --- TEST 5: Delete the file ---
print("\n" + "=" * 50)
print("[TEST 5] Delete 'jarvis_test_file'")
print("=" * 50)
success5, message5 = hands.delete_item(["jarvis_test_file"])
print(f"  Success: {success5}")

print(f"  Message: {message5}")

# --- TEST 6: Delete something that doesn't exist (should fail) ---
print("\n" + "=" * 50)
print("[TEST 6] Delete 'ghost_item' (should fail gracefully)")
print("=" * 50)
success6, message6 = hands.delete_item(["ghost_item"])
print(f"  Success: {success6}")
print(f"  Message: {message6}")

print("\n" + "=" * 50)
print("All tests complete.")
print("=" * 50)