import math
import os
import sys
from pathlib import Path

# --- Statistical functions ---
def mean(echantillon):
    return float(sum(echantillon)) / float(len(echantillon))

def stat_variance(echantillon):
    n = float(len(echantillon))
    mq = mean(echantillon) ** 2
    s = sum(x**2 for x in echantillon)
    return s / n - mq

def stat_ecart_type(echantillon):
    return math.sqrt(stat_variance(echantillon))

def median(echantillon):
    echantillon.sort()
    size = len(echantillon)
    if size % 2 == 0:
        return float(echantillon[size // 2 - 1] + echantillon[size // 2]) / 2
    else:
        return echantillon[size // 2]

def ninetyfive(echantillon):
    echantillon.sort()
    i95 = int(len(echantillon) * 95 / 100) - 1
    return echantillon[i95]

def five(echantillon):
    echantillon.sort()
    i5 = int(len(echantillon) * 5 / 100) - 1
    return echantillon[i5]

# --- Dynamic project root ---
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

dico = {}
liste = {}

for sp in species:
    print(sp)
    dico[sp] = {}
    liste[sp] = []
    input_file = project_root / sp / 'rm1.txt'

    try:
        with open(input_file, "r") as f:
            for l in f:
                a = l.strip("\n").split("\t")
                subset = a[0]
                strains = subset.split(";")
                nb = len(strains)
                if nb > 3 and float(a[2]) > 0:
                    rm = float(a[1]) / float(a[2])
                    if nb in dico[sp]:
                        dico[sp][nb].append(rm)
                    else:
                        dico[sp][nb] = [rm]
                        liste[sp].append(nb)
    except IOError:
        print(f"Cannot open {input_file}")
        continue

    liste[sp].sort()
    output_file = project_root / sp / 'graph.txt'
    with open(output_file, "w") as h:
        h.write("Nb\tMean\tMedian\tSD\n")
        for nb in liste[sp]:
            h.write(f"{nb}\t{mean(dico[sp][nb])}\t{median(dico[sp][nb])}\t{stat_ecart_type(dico[sp][nb])}\n")
