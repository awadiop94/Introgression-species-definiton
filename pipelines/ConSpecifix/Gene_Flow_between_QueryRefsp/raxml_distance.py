#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

# Get species from command-line argument
sp = sys.argv[-1]
species = [sp]

for sp in species:
    tag = sp.replace("/", "_")
    concat_file = project_root / sp / "core_genome" / "concat_names.fa"
    distance_file = project_root / sp / "core_genome" / "distances.dist"

    # Run RAxML
    os.system(f"/proj/bobaylab/users/adiop2/standard-RAxML-master/raxmlHPC -f x -p 12345 -s {concat_file} -m GTRGAMMA -n {tag} -T 12")

    # Move output distances file
    os.system(f"mv RAxML_distances.{tag} {distance_file}")

    # Optionally remove other RAxML intermediate files
    # os.system("rm RA*")
