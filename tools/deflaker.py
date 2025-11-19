import subprocess
import sys
import time

# Configuration
MAX_RETRIES = 3
GRADLE_CMD = ["./gradlew", ":core-banking:test", "--rerun-tasks"]

def run_build(is_retry=False):
    """Runs the gradle build. Returns True if success, False if failed."""
    cmd = GRADLE_CMD[:]
    
    if is_retry:
        print("\n  Attempting retry with forced execution...")
        cmd.append("--rerun-tasks")

    # Run the command and capture output
    result = subprocess.run(cmd, text=True, capture_output=False)
    return result.returncode == 0

def main():
    print(f"Starting Build: {' '.join(GRADLE_CMD)}")
    
    # Initial Run
    if run_build():
        print("\n Build Passed on first try!")
        sys.exit(0)

    # If we get here, the first run failed. Start Mitigation.
    print(f"\n Build Failed! Analyzing for flakiness (Retrying {MAX_RETRIES} times)...")

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n--- Retry Attempt {attempt}/{MAX_RETRIES} ---")
        
        if run_build(is_retry=True):
            print("\n  FLAKY TEST DETECTED!")
            print("   The build failed initially but passed on retry.")
            print("   Action: Marking build as SUCCESS but logging flakiness report.")
            
            # In a real scenario, you would upload this to a dashboard (like Datadog)
            with open("flaky_report.json", "w") as f:
                f.write('{"status": "flaky", "module": "core-banking"}')
                
            sys.exit(0) # We exit 0 so the CI pipeline doesn't stop!
        
        time.sleep(1) # Cool down

    # If we get here, it failed every single time. It's a real bug.
    print("\n REAL FAILURE: Test failed consistently across all retries.")
    sys.exit(1)

if __name__ == "__main__":
    main()