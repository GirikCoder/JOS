import understanding

def run_tests():
    test_cases = [
        # Explicit NLP diagnostic tests for OPEN_ITEM capability
        {"input": "open the folder named gggg", "expected_intent": "OPEN_ITEM", "expected_entities": ["gggg"]},
        {"input": "open the file called budget", "expected_intent": "OPEN_ITEM", "expected_entities": ["budget"]},
        {"input": "open chrome", "expected_intent": "OPEN_APP", "expected_entities": ["chrome"]},
    ]

    all_passed = True
    print("\n" + "=" * 60)
    print(" NLP DIAGNOSTIC TEST (MANDATORY)")
    print("=" * 60)
    for case in test_cases:
        res = understanding.understand_command(case["input"])
        intent = res["intent"] if res else "None"
        entities = res["entities"] if res else []
        
        passed = (intent == case["expected_intent"]) and (entities == case["expected_entities"])
        if not passed:
            all_passed = False
            print(f"[FAIL] '{case['input']}'")
            print(f"       Expected: {case['expected_intent']} with {case['expected_entities']}")
            print(f"       Got:      {intent} with {entities}")
        else:
            print(f"[PASS] '{case['input']}' -> {intent} {entities}")
            
    if all_passed:
        print("\nAll NLP diagnostic test cases passed successfully.")
    else:
        print("\nSome NLP diagnostic test cases failed.")

if __name__ == "__main__":
    run_tests()
