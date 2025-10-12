#!/usr/bin/env python3
import subprocess
import sys
import os

def run(cmd):
    """Run a shell command, print it, and check for errors."""
    print(f"\n[Running] {cmd}\n")
    subprocess.run(cmd, shell=True, check=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_Querydb.py <results_dir>")
        sys.exit(1)

    results_dir = sys.argv[1]

    # Ensure results directory exists
    os.makedirs(results_dir, exist_ok=True)

    # === Gene flow pipeline steps ===
    run(f"python pipelines/ConSpecifix/create_candidate_db.py {results_dir}")
    run(f"python pipelines/ConSpecifix/create_configcand.py {results_dir}")

    print("\n✅ ANI cluster analysis completed successfully!\n")

if __name__ == "__main__":
    main()
