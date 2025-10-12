#!/usr/bin/env python3
import os
import sys
import datetime
import time
from pathlib import Path

ts = time.time()

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

# Open main output file
h = open(project_root / sp / "core_genome" / "criterion.txt", "w")

# Open stats file to append
critInfoFD = open(project_root / sp / "core_genome" / "crit_stats.txt", "a")
critInfoFD.write(f'Member of {sp} according to Exclusion Criterion*: ')

for sp in species:
    kick = []
    keep = []
    tag = "no"
    try:
        sample = open(project_root / sp / "core_genome" / "sample.txt", "r")
        removal = open(project_root / sp / "core_genome" / "for_removal.txt", "r")

        for l in removal:
            kick.append(l.strip())

        for l in sample:
            strain = l.strip()
            if strain not in kick:
                keep.append(strain)

        sample.close()
        removal.close()

    except Exception as e:
        print(str(e))
        continue

# Prepare header
header = f"""Conspecifix Results:

\tCompleted on: {datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}

\tFor more information about our process, please visit our website at
\t\thttps://www.conspecifix.com
\tor take a look at our github
\t\thttps://github.com/Bobay-Ochman

\tExclusion Criterion defined in Bobay & Ochman, GBE 2017

The following strains are members of the species:
"""
h.write(header)
h.write('\n'.join(keep) + '\n\n')

# Write remaining strains if any
if tag == "no":
    h.write("All strains were determined to be a member of the species\n")
else:
    h.write("The following strains were determined to NOT be a member of the species:\n")
    h.write('\n'.join(kick) + '\n')

h.truncate()
h.close()

# Update crit_stats.txt
critInfoFD.write('no' if tag == "yes" else 'yes')
critInfoFD.write('\n\n*Please refer to Bobay & Ochman, GBE 2017')
critInfoFD.close()
