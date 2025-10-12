#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

# Get species from command-line argument
sp = sys.argv[-1]
species = [sp]

for sp in species:
    print(sp)
    tag = 0
    sp_path = project_root / sp
    tmp = os.listdir(sp_path)
    
    # Find genome file starting with "GC" and ending with ".fa"
    out = None
    for stuff in tmp:
        if stuff.startswith("GC") and stuff.endswith(".fa"):
            out = stuff
            tag = 1
            break
    
    if tag == 0:
        print("WARNING: No genome file has been found")
    
    try:
        concat_file = sp_path / "core_genome" / "concat.fa"
        concat_names_file = sp_path / "core_genome" / "concat_names.fa"
        names_file = sp_path / "core_genome" / "names.txt"

        with open(concat_file, 'r') as f, \
             open(concat_names_file, 'w') as h, \
             open(names_file, 'w') as g:

            nb = 0
            for l in f:
                if l.startswith('>'):
                    st = l.strip().strip('>')
                    print(st)
                    if st == out:
                        name = "out"
                    else:
                        nb += 1
                        name = "B" + str(nb)
                    h.write(f'>{name}\n')
                    g.write(f'{name}\t{st}\n')
                else:
                    h.write(l)
                    
    except IOError as e:
        print(f"Error: {e}")
        pass
