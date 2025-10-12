#!/usr/bin/env python3
import sys
import os
import random
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

# Get species from command line
sp = sys.argv[-1]
species = [sp]

consensus = {}
spectrum = {"A": ["C", "G", "T"],
            "C": ["A", "G", "T"],
            "G": ["A", "C", "T"],
            "T": ["A", "C", "G"]}
alpha = ["A", "C", "G", "T"]
within, between = {}, {}

for sp in species:
    consensus[sp] = ""
    differences = 0
    within[sp] = {i: 0 for i in range(5)}
    between[sp] = {i: 0 for i in range(5)}

    # Read sequences
    seq_file = project_root / sp / "core_genome/concat_names.fa"
    tmp = {}
    with open(seq_file, "r") as f:
        for l in f:
            if l.startswith(">"):
                st = l.strip(">").strip()
                tmp[st] = []
            else:
                tmp[st].append(l.strip())

    seq = {st: "".join(tmp[st]) for st in tmp}
    short = list(seq.keys())
    short.remove("out")  # Exclude outgroup

    length = len(seq[list(seq.keys())[0]])
    i = 0
    while i < length:
        tmp_col = [seq[st][i] for st in short]
        poly = list(set(tmp_col))
        for x in ["-", "N", "K", "R", "S", "T", "W", "Y"]:
            if x in poly:
                poly.remove(x)
        nb = len(poly)
        within[sp][nb] += 1

        # Compare to outgroup
        poly.append(seq["out"][i])
        poly = list(set(poly))
        for x in ["-", "N", "K", "R", "S", "T", "W", "Y"]:
            if x in poly:
                poly.remove(x)
        nb = len(poly)
        between[sp][nb] += 1

        # Build consensus
        NB = 0
        memo = ""
        for N in alpha:
            number = tmp_col.count(N)
            if number > NB:
                NB = number
                memo = N
        if memo == "":
            consensus[sp] += "-"
        else:
            consensus[sp] += memo
        if seq["out"][i] != memo and seq["out"][i] != "-":
            differences += 1
        i += 1

    print(f"{sp} statistics:")
    for j in within[sp]:
        print(sp, j, within[sp][j], between[sp][j])

    # Select random mutation positions
    positions = list(range(length))
    bag = {}
    i = 0
    while i < differences:
        tag = "no"
        while tag == "no":
            pos = random.choice(positions)
            if pos in bag or consensus[sp][pos] == "-":
                continue
            bag[pos] = "y"
            tag = "ok"
        i += 1
    print ("consensus= ", len(consensus[sp]))
    print ("sequences= ", len(seq[st]))
    print ("differences= ",differences)
    print ("bag= ",len(bag.keys()))
    # Write fake sequences
    fake = ""
    for i, N in enumerate(consensus[sp]):
        if i in bag:
            fake += random.choice(spectrum[N])
        else:
            fake += N

    fake_file = project_root / sp / "core_genome/fake.fa"
    with open(fake_file, "w") as h:
        for st in short:
            h.write(f">{st}\n{seq[st]}\n")
        h.write(f">fake\n{fake}\n")

    print(f"Finished writing fake sequences for {sp}")
