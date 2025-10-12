#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

problem = []
sample = {}

# Read sample.txt
for sp in species:
    sample[sp] = []
    try:
        with open(project_root / sp / "core_genome" / "sample.txt", "r") as f:
            for l in f:
                sample[sp].append(l.strip())
    except IOError:
        problem.append(sp)
        continue

# Read key.txt
key = {}
for sp in species:
    try:
        with open(project_root / sp / "core_genome" / "key.txt", "r") as f:
            lines = f.readlines()
            if len(lines) == 0:
                problem.append(sp)
                continue
            for l in lines:
                a = l.strip().split(' ')
                key[sp] = 'direct' if float(a[0]) < float(a[1]) else 'reverse'
                print(sp, a, key[sp])
    except IOError:
        problem.append(sp)
        continue

# Remove problematic species
for sp in problem:
    print(sp)
    try:
        species.remove(sp)
    except ValueError:
        pass

# Main processing
euk = []
print("*********")
for sp in species:
    print(sp)
    liste = []
    with open(project_root / sp / "core_genome" / "distrib.txt", "r") as f:
        for l in f:
            a = l.strip().split('\t')
            liste.append(a[0])

    vector = []
    try:
        with open(project_root / sp / "core_genome" / "vector.txt", "r") as f:
            for l in f:
                a = l.strip().split('\t')
                vector.append(a[0])
    except IOError:
        species.remove(sp)
        continue

    low, high = [], []
    for i, subset in enumerate(liste):
        strains_subset = subset.split(';')
        tag = vector[i]
        if key[sp] == "direct":
            if tag == "1":
                low.extend(strains_subset)
            elif tag == "2":
                high.extend(strains_subset)
        else:
            if tag == "2":
                low.extend(strains_subset)
            elif tag == "1":
                high.extend(strains_subset)

    TOT = len(low) + len(high)
    with open(project_root / sp / 'core_genome' / 'kmeans.txt', 'w') as h:
        h.write(f'tot\t{len(low)}\t{round(100*len(low)/float(TOT),1)}\t{len(high)}\t{round(100*len(high)/float(TOT),1)}\n')
        for st in sample[sp]:
            L = low.count(st)
            H = high.count(st)
            tot = L + H
            try:
                h.write(f'{st}\t{L}\t{round(100*L/float(tot),1)}\t{H}\t{round(100*H/float(tot),1)}\n')
            except ZeroDivisionError:
                print("PROBLEM", st, L, tot)
