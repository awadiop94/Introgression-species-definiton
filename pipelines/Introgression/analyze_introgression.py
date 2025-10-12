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
        print("Usage: python analyze_introgression.py <results_dir>")
        sys.exit(1)

    results_dir = sys.argv[1]

    # Ensure results directory exists
    os.makedirs(results_dir, exist_ok=True)

    # === Gene flow pipeline steps ===
    run(f"python pipelines/Introgression/root1/raxml_rooted.py {results_dir}")
    run(f"python pipelines/Introgression/root2/raxml_rooted.py {results_dir}")
    run(f"python pipelines/Introgression/extract_names.py {results_dir}")
    run(f"python pipelines/Introgression/branch_length.py {results_dir}")
    run(f"python pipelines/Introgression/cophenetic.py {results_dir}")
    run(f"python pipelines/Introgression/identify.py {results_dir}")
    run(f"python pipelines/Introgression/reunite_verification.py {results_dir}")

    print("\n✅ ANI cluster analysis completed successfully!\n")

if __name__ == "__main__":
    main()
