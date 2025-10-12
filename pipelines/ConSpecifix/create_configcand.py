#!/usr/bin/env python3
import sys
from pathlib import Path
import yaml

# Dynamically detect project root (two levels up from this script)
project_root = Path(__file__).resolve().parents[2]

# Get species from command line
sp = sys.argv[-1]

# Path to species directory
sp_dir = project_root / sp

# Build the todo dictionary from genome_clusters.csv
todo = {}
genome_csv = sp_dir / "ANI_results/genome_clusters.csv"
with open(genome_csv, "r") as f:
    for line in f:
        a = line.strip().split(",")
        if "genome" not in a[0]:
            file, sp1 = a[0], a[1]
            todo.setdefault(sp1, []).append(file)

# Select reference clusters with >= 15 genomes
valid_refs = {ref for ref, genomes in todo.items() if len(genomes) >= 15}

# Path to runner.txt
runner_file = sp_dir / "runner.txt"

# Build ref -> candidate clusters dictionary
ref_to_cands = {}
with open(runner_file, "r") as f:
    for line in f:
        a = line.strip().split("\t")
        if len(a) < 2:
            continue
        ref, cand = a[0], a[1]
        if ref not in valid_refs:
            continue
        ref_to_cands.setdefault(ref, [])
        if cand not in ref_to_cands[ref]:
            ref_to_cands[ref].append(cand)

# Write configcand.yaml to project root
out_file = project_root / "configcand.yaml"
with open(out_file, "w") as f:
    yaml.dump(ref_to_cands, f, default_flow_style=False, sort_keys=False)

print(f"Wrote {out_file}")
