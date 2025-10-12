#!/usr/bin/env python3
import sys
from pathlib import Path

# Dynamically detect project root (two levels up from this script)
project_root = Path(__file__).resolve().parents[2]

# Get species from command line
sp = sys.argv[-1]
sp_dir = project_root / sp

# Build todo dictionary from genome_clusters.csv
todo = {}
genome_csv = sp_dir / "ANI_results/genome_clusters.csv"
with open(genome_csv, "r") as f:
    for line in f:
        a = line.strip().split(",")
        if "genome" not in a[0]:
            file, sp1 = a[0], a[1]
            todo.setdefault(sp1, []).append(file)

# Write configref.yaml in project root
config_file = project_root / "configref.yaml"
with open(config_file, "w") as f:
    f.write("dirname:\n")
    for sp1, files in todo.items():
        if len(files) >= 15:
            f.write(f" - {sp1}\n")
            # Create ReferenceDatabase directories
            ref_dir = sp_dir / "Gene_Flow/ReferenceDatabase" / sp1
            ref_dir.mkdir(parents=True, exist_ok=True)
            # Write path_to_genome_list.txt
            genome_list_file = ref_dir / "path_to_genome_list.txt"
            with open(genome_list_file, "w") as h:
                for file in files:
                    h.write(f"{file}\n")
