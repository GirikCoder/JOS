import time
from app_resolver import DynamicAppResolver
from hands import JarvisHands

def run_test():
    resolver = DynamicAppResolver()
    
    print("Building dynamic app map...")
    start_time = time.time()
    app_map = resolver.build_app_map()
    end_time = time.time()
    
    print(f"Execution time: {end_time - start_time:.4f} seconds")
    print(f"Total applications found: {len(app_map)}")
    
    apps_to_test = ["chrome", "calculator", "edge"]
    print("\nLookup Test:")
    for app in apps_to_test:
        if app in app_map:
            print(f"- {app}: {app_map[app]}")
        else:
            # Fuzzy search
            found = False
            for k in app_map.keys():
                if app in k:
                    print(f"- {app} (matched as '{k}'): {app_map[k]}")
                    found = True
                    break
            if not found:
                print(f"- {app}: NOT FOUND")
                
    print("\nTesting JarvisHands execution...")
    # Instantiate hands
    hands = JarvisHands()
    
    # Prove absolute path execution works
    print("Attempting to open calculator...")
    success, msg = hands.open_app(["calculator"])
    print(f"Result: {success} - {msg}")

if __name__ == "__main__":
    run_test()
