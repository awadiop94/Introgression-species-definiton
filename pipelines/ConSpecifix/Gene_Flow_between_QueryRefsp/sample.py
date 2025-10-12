import os
import sys
import random
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

# Collect strains
strains = {}
for sp in species:
    strains[sp] = []
    try:
        names_file = project_root / sp / 'core_genome' / 'names.txt'
        with open(names_file, 'r') as f:
            for l in f:
                strains[sp].append(l.strip('\n').split('\t')[0])
    except IOError:
        pass

# Read distances
dist = {}
for sp in species:
    dist[sp] = {}
    try:
        dist_file = project_root / sp / 'core_genome' / 'distances.dist'
        with open(dist_file, 'r') as f:
            for l in f:
                a = l.strip("\n").split("\t")
                st1, st2 = a[0].strip().split(" ")
                dist[sp].setdefault(st1, {})
                dist[sp].setdefault(st2, {})
                dist[sp][st1][st2] = float(a[1])
                dist[sp][st2][st1] = float(a[1])
    except IOError:
        pass

# Remove identical genomes
exclusion = []
for sp in species:
    for st in exclusion:
        if st in strains[sp]:
            strains[sp].remove(st)

# Initialize clusters
cluster = {}
for sp in species:
    sub = list(dist[sp].keys())
    cluster[sp] = list(sub)

# Write sample.txt
for sp in species:
    sample_file = project_root / sp / 'core_genome' / 'sample.txt'
    with open(sample_file, 'w') as h:
        for st in sub:
            h.write(st + "\n")

# Generate random families
for sp in species:
    families_file = project_root / sp / 'core_genome' / 'families.txt'
    h = open(families_file, "w")
    familles = []
    combin = {}
    i = 4
    while i <= len(sub):
        toto = 0
        print(i)
        combin[i] = []
        reservoire = []
        j = 1
        limit = i**2
        while j <= 100:
            tmp = []
            for truc in range(i):
                st = random.choice(sub)
                while st in tmp:
                    st = random.choice(sub)
                tmp.append(st)
            tmp.sort()
            subset = ";".join(tmp)
            if subset not in combin[i]:
                toto += 1
                print(i, ' ', toto)
                combin[i].append(subset)
                familles.append(subset)
                h.write(f"{i}\t{subset}\n")
                j += 1
            elif subset not in reservoire:
                reservoire.append(subset)
                if len(reservoire) == len(combin[i]):
                    print('OK')
                    break
        i += 2
    h.close()
