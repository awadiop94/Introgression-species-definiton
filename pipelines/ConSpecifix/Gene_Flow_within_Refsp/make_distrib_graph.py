#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

for sp in species:
    r_script_path = project_root / sp / 'core_genome' / 'make_distrib_graph.R'
    distrib_file = project_root / sp / 'core_genome' / 'distrib.txt'
    distrib_pdf = project_root / sp / 'core_genome' / 'Distrib.pdf'
    vector_file = project_root / sp / 'core_genome' / 'vector.txt'
    key_file = project_root / sp / 'core_genome' / 'key.txt'

    with open(r_script_path, 'w') as h:
        h.write(f"tab=read.table('{distrib_file}')\n")
        h.write("toto=kmeans(tab$V2,2)\n")
        h.write(f"pdf('{distrib_pdf}')\n")
        h.write("hist(tab$V2,nclass=60)\n")
        h.write("abline(v=toto[2]$centers,col='red')\n")
        h.write("dev.off()\n")
        h.write(f"write(toto[1]$cluster,ncol=1,file='{vector_file}')\n")
        h.write(f"write(toto[2]$centers,ncol=2,file='{key_file}')\n")

# Run the generated R script
os.system(f"Rscript {r_script_path}")
