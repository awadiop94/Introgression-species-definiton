#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

def run(cmd):
    """Run a shell command, print it, and check for errors."""
    print(f"\n[Running] {cmd}\n")
    subprocess.run(cmd, shell=True, check=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_gene_flow_refsp.py <results_dir>")
        sys.exit(1)

    results_dir = sys.argv[1]
    prefix_path = Path(__file__).resolve().parents[3]

    # Ensure results directory exists
    os.makedirs(results_dir, exist_ok=True)

    # === Gene flow pipeline steps ===
    run(f"python pipelines/ConSpecifix/Gene_Flow_within_Refsp/raxml_distance.py {results_dir}")
    run(f"python pipelines/ConSpecifix/Gene_Flow_within_Refsp/rename_ref.py {results_dir}")
    run(f"python pipelines/ConSpecifix/Gene_Flow_within_Refsp/sample.py {results_dir}")
    run(f"python pipelines/ConSpecifix/Gene_Flow_within_Refsp/prog2.py {results_dir} --prefix_path {prefix_path}")
    run(f"python pipelines/ConSpecifix/Gene_Flow_within_Refsp/distrib.py {results_dir}")
    run(f"python pipelines/ConSpecifix/Gene_Flow_within_Refsp/make_distrib_graph.py {results_dir}")
    run(f"python pipelines/ConSpecifix/Gene_Flow_within_Refsp/split_kmean.py {results_dir}")
    run(f"python pipelines/ConSpecifix/Gene_Flow_within_Refsp/make_kmeans_graph.py {results_dir}")
    run(f"python pipelines/ConSpecifix/Gene_Flow_within_Refsp/criterion.py {results_dir}")

    print("\n✅ ANI cluster analysis completed successfully!\n")

if __name__ == "__main__":
    main()
