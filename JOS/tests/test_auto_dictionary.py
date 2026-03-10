"""
Automated App Dictionary Test — Opens and closes each safe app.
Only tests lightweight/native Windows apps to avoid CPU overload.
"""
import time
from hands import JarvisHands

hands = JarvisHands()

# Only lightweight native Windows apps that can be safely opened AND closed
# Excluded: explorer (taskkill kills Windows shell), cmd (kills the test runner itself)
SAFE_APPS = ["notepad", "calculator", "paint", "settings", "browser", "whatsapp"]

passed = 0
failed = 0
results = []

print("\n" + "=" * 60)
print("  JOS APP DICTIONARY - AUTOMATED TEST SUITE")
print("  Testing: Open -> Wait 5s -> Close -> Wait 2s")
print("=" * 60)

for app in SAFE_APPS:
    print(f"\n{'—' * 60}")
    print(f"  [{SAFE_APPS.index(app) + 1}/{len(SAFE_APPS)}] Testing: '{app}'")
    print(f"{'—' * 60}")

    # --- OPEN ---
    open_success, open_msg = hands.open_app([app])
    print(f"  OPEN:  {open_msg}")

    if not open_success:
        print(f"  SKIP:  Could not open '{app}', skipping close test.")
        failed += 1
        results.append((app, "FAIL", open_msg))
        continue

    # --- WAIT: Let user visually verify the app opened ---
    print(f"  WAIT:  Holding for 5 seconds...")
    time.sleep(5)

    # --- CLOSE ---
    close_success, close_msg = hands.close_app([app])
    print(f"  CLOSE: {close_msg}")

    if close_success:
        passed += 1
        results.append((app, "PASS", "Opened and closed successfully."))
    else:
        # App opened but failed to close — still counts as partial pass
        failed += 1
        results.append((app, "PARTIAL", f"Opened OK, close failed: {close_msg}"))

    # --- COOLDOWN: Let OS clean up before next app ---
    print(f"  COOL:  Waiting 2 seconds before next app...")
    time.sleep(2)

# =============================================================================
# SUMMARY REPORT
# =============================================================================
print("\n\n" + "=" * 60)
print("  FINAL REPORT")
print("=" * 60)
print(f"  Total Apps Tested:  {len(SAFE_APPS)}")
print(f"  Passed:             {passed}")
print(f"  Failed:             {failed}")
print(f"  Success Rate:       {(passed / len(SAFE_APPS)) * 100:.0f}%")
print("=" * 60)

for app, status, msg in results:
    icon = "+" if status == "PASS" else "~" if status == "PARTIAL" else "X"
    print(f"  [{icon}] {app:<15} {status:<10} {msg}")

print("=" * 60)
