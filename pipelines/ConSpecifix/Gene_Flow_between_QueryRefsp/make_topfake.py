#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

# Get species name from command line
sp = sys.argv[-1]
species = [sp]

for sp in species:
    result_file = project_root / sp / "core_genome" / "result_fake.txt"
    mean_file = project_root / sp / "core_genome" / "mean_hm_fake.txt"

    with open(result_file, "r") as f, open(mean_file, "w") as h:
        line = f.readline()
        a = line.strip("\n").split("\t")
        fake = float(a[1])
        h.write(line)
