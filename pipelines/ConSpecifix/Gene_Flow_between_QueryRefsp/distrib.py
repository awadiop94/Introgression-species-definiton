import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

for sp in species:
    output_file = project_root / sp / 'core_genome' / 'distrib.txt'
    input_file = project_root / sp / 'core_genome' / 'rm1.txt'

    print(sp)
    dico = {}

    try:
        with open(input_file, 'r') as f, open(output_file, 'w') as k:
            for l in f:
                a = l.strip('\n').split('\t')
                strains = a[0].split(';')
                mark = "with" if "out" in strains else "without"
                
                r, m = float(a[1]), float(a[2])
                if m > 0:
                    rm = r / m
                    k.write(f"{a[0]}\t{rm}\t{mark}\n")
    except FileNotFoundError:
        print(f"Major problem! Can't open {input_file}")
