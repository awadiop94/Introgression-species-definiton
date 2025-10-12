#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

for sp in species:
    distrib_file = project_root / sp / 'core_genome' / 'distrib.txt'
    rm_file = project_root / sp / 'core_genome' / 'rm1.txt'

    print(sp)
    dico = {}

    try:
        f = open(rm_file, 'r')
    except FileNotFoundError:
        print('Major problem! Can\'t open rm1.txt')
        continue

    k = open(distrib_file, 'w')
    for l in f:
        a = l.strip('\n').split('\t')
        strains = a[0].split(';')
        mark = "with" if "out" in strains else "without"
        nb = len(strains)
        r, m = float(a[1]), float(a[2])  # pull the rm ratio
        if m > 0:
            rm = r / m
            k.write(f"{a[0]}\t{rm}\t{mark}\n")

    f.close()
    k.close()
