import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

for sp in species:
    values = []

    rm1_path = project_root / sp / "core_genome" / "rm1.txt"
    topref_path = project_root / sp / "core_genome" / "topref.txt"
    mean_path = project_root / sp / "core_genome" / "mean_hm_ref.txt"

    # Read rm1.txt and collect entries not ending with 'out' and with >=12 strains
    with open(rm1_path, "r") as f, open(topref_path, "w") as h:
        for l in f:
            a = l.strip("\n").split("\t")
            if not a[0].endswith("out"):
                nb = a[0].count(";") + 1
                if nb >= 12:
                    hm = float(a[3])
                    values.append(hm)
                    h.write(l)

    # Compute mean of values and write to file
    with open(mean_path, "w") as g:
        if values:
            M = sum(values) / len(values)
            g.write(str(M) + "\n")
