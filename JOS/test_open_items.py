import os
import time
from hands import JarvisHands
from pathlib import Path

def run_test():
    print("Testing open_item capability...")
    hands = JarvisHands()
    
    # 3. Programmatically create a dummy file and folder
    # Document folder
    doc_dir = hands.safe_zones["documents"]
    desktop_dir = hands.safe_zones["desktop"]
    
    dummy_file = doc_dir / "jarvis_find_test.txt"
    dummy_folder = desktop_dir / "jarvis_folder_test"
    
    try:
        dummy_file.touch(exist_ok=True)
        if not dummy_folder.exists():
            os.makedirs(dummy_folder)
        print(f"Created dummy file: {dummy_file}")
        print(f"Created dummy folder: {dummy_folder}")
    except Exception as e:
        print(f"Failed to create dummy test files: {e}")
        return

    # 4. Call hands.open_item(["jarvis_find_test"])
    print("\nAttempting to open dummy file 'jarvis_find_test'...")
    success_file, msg_file = hands.open_item(["jarvis_find_test"])
    if success_file:
        print(f"[PASS] - {msg_file}")
    else:
        print(f"[FAIL] - file - {msg_file}")
        
    # 5. time.sleep(3) for visualization
    time.sleep(3)
    
    # 6. Call hands.open_item(["jarvis_folder_test"])
    print("\nAttempting to open dummy folder 'jarvis_folder_test'...")
    success_folder, msg_folder = hands.open_item(["jarvis_folder_test"])
    if success_folder:
        print(f"[PASS] - {msg_folder}")
    else:
        print(f"[FAIL] - folder - {msg_folder}")
        
    # 7. time.sleep(3) for visualization
    time.sleep(3)
    
    # 8. Clean up
    print("\nCleaning up dummy files...")
    if dummy_file.exists():
        os.remove(dummy_file)
    if dummy_folder.exists():
        import shutil
        shutil.rmtree(dummy_folder)
    print("Cleanup complete.")

if __name__ == "__main__":
    run_test()
