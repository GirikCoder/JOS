import time
from hands import JarvisHands

def run_complex_test():
    print("="*50)
    print("🌐 WEB_SEARCH COMPLEXITY STRESS TEST")
    print("="*50)
    
    hands = JarvisHands()
    
    # A list of dictionaries containing complex test scenarios
    test_cases = [
        {
            "desc": "Standard YouTube Search",
            "entities": ["python tutorials"],
            "text": "search youtube for python tutorials"
        },
        {
            "desc": "Standard Google Search",
            "entities": ["weather in tokyo"],
            "text": "look up the weather in tokyo"
        },
        {
            "desc": "URL Encoding (Special Characters)",
            "entities": ["c++ pointers & references!"],
            "text": "google c++ pointers & references!"
        },
        {
            "desc": "YouTube Fallback (Using the word 'video')",
            "entities": ["funny cats"],
            "text": "find a video of funny cats"
        },
        {
            "desc": "Long Query String",
            "entities": ["how to fix list index out of range in python"],
            "text": "search the web for how to fix list index out of range in python"
        },
        {
            "desc": "Safety Check (Empty Entity List)",
            "entities": [],
            "text": "search google"
        }
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] Testing: {case['desc']}")
        print(f"Input Text: '{case['text']}'")
        print(f"Entities: {case['entities']}")
        
        # Execute the search
        success, msg = hands.web_search(case["entities"], case["text"])
        
        if success:
            print(f"✅ [PASS] - {msg}")
        else:
            print(f"❌ [FAIL] - {msg}")
            
        # Wait 3 seconds before opening the next tab so we don't overwhelm the browser
        if i < len(test_cases):
            time.sleep(3)

    print("\n" + "="*50)
    print("Test Sequence Complete. Please check your browser tabs.")
    print ("Test Completed")
    print("="*50)

if __name__ == "__main__":
    run_complex_test()