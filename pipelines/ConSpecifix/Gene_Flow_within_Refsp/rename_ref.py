#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

for sp in species:
    sp_dir = project_root / sp / "core_genome"
    try:
        with open(sp_dir / "concat.fa", "r") as f, open(sp_dir / "names.txt", "w") as g:
            for l in f:
                if l.startswith(">"):
                    st = l.strip()[1:]  # remove leading ">" and trailing newline
                    print(st)
                    g.write(st + "\n")
    except IOError:
        pass
