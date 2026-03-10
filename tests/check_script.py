import understanding
import time


TEST_CASES = [
    "put the financial report in the backup folder",   # Failed because of 'i' in financial
    "send the file to d drive",                        # Failed because of 'i' in file/drive
    "open google chrome",                              # Failed because proper noun
    "transfer my resume to the documents folder",      # Standard test
    "move it to the secret folder"                     # 'it' should be removed, 'secret folder' kept
]

print("\n" + "="*50)
print(" 🧪  INSTANT LOGIC TEST (No Mic Needed)")
print("="*50 + "\n")

for cmd in TEST_CASES:
    print(f"🔹 Input: '{cmd}'")
    
    start = time.time()
    result = understanding.understand_command(cmd)
    end = time.time()
    
    if result:
        print(f"   ✅ PASSED ({result['confidence']})")
        print(f"   ├─ Intent:   {result['intent']}")
        print(f"   └─ Entities: {result['entities']}") # Check if 'file' or 'drive' appears here
    else:
        print(f"   ❌ FAILED (Ignored)")
    
    print("-" * 50)