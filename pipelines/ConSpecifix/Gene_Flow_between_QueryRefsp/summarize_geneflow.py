#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]

def read_single_float(file_path, split_char=None, idx=-1):
    """Read the last value of the first (or only) line in a file."""
    with open(file_path) as f:
        line = f.readline().strip()
        if split_char:
            parts = line.split(split_char)
            return float(parts[idx])
        return float(line)

# Read runner file and collect unique folders to process
todo = []
runner_file = project_root / sp / "runner.txt"
with open(runner_file) as f:
    for line in f:
        folder = "/".join(line.strip().split("\t")[:2])
        if folder not in todo:
            todo.append(folder)

# Process each folder
for folder in todo:
    sp1, sp2 = folder.split("/")
    query_core_dir = project_root / sp / "Gene_Flow" / "QueryDatabase" / sp1 / sp2 / "core_genome"

    if not (project_root / sp / "Gene_Flow" / "QueryDatabase" / sp1).exists():
        continue

    # Read all required files
    try:
        hmcand = read_single_float(query_core_dir / "mean_hm_cand.txt")
        hmref = read_single_float(query_core_dir / "mean_hm_ref.txt")
        hmfake = read_single_float(query_core_dir / "mean_hm_fake.txt", split_char="\t", idx=1)
        pv_candfake = read_single_float(query_core_dir / "double_test.txt", split_char=" ", idx=1)
    except FileNotFoundError:
        continue

    # Compute normalized value
    hmnorm = (hmcand - hmfake) / (hmref - hmfake) if hmref != hmfake else 0
    mark = (
        "same"
        if hmnorm > 0.2 and hmcand > hmfake and hmcand >= hmref and hmref > hmfake and pv_candfake < 1e-4
        else "diff"
    )

    # Write per-folder result
    result_file = query_core_dir / "hmnorm_result.txt"
    with open(result_file, "w") as f:
        f.write("ANI-sp1\tANI-sp2\thmref\thmcand\thmfake\thmnorm\tpv_candfake\tBSCsp-class\n")
        f.write(f"{sp1}\t{sp2}\t{hmref}\t{hmcand}\t{hmfake}\t{hmnorm}\t{pv_candfake}\t{mark}\n")
