import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

for sp in species:
    Values = []

    distrib_path = project_root / sp / "core_genome" / "distrib.txt"
    topcand_path = project_root / sp / "core_genome" / "topcand.txt"
    mean_path = project_root / sp / "core_genome" / "mean_hm_cand.txt"

    # Read distrib.txt and collect "out" values
    with open(distrib_path, "r") as f, open(topcand_path, "w") as h:
        for l in f:
            a = l.strip("\n").split("\t")
            if a[0].endswith("out"):
                hm = float(a[1])
                Values.append(hm)
                h.write(l)

    # Compute mean of Values and write to file
    with open(mean_path, "w") as g:
        if Values:
            M = sum(Values) / len(Values)
            g.write(str(M) + "\n")
