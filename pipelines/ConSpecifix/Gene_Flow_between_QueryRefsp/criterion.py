#!/usr/bin/env python3
import os
import sys
import datetime
import time
from pathlib import Path

ts = time.time()

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

# Get species from command line
sp_name = sys.argv[-1]
species = [sp_name]

# Open criterion output file
criterion_file = project_root / sp_name / "criterion.txt"
h = open(criterion_file, "w")

crit_stats_file = project_root / sp_name / "crit_stats.txt"
critInfoFD = open(crit_stats_file, "a")
critInfoFD.write(f'Member of {sp_name} according to Exclusion Criterion*: ')

for sp in species:
    kick = []
    keep = []
    tag = "no"
    try:
        sample_file = project_root / sp / "sample.txt"
        removal_file = project_root / sp / "for_removal.txt"
        with open(removal_file, "r") as removal:
            for l in removal:
                kick.append(l.strip())
        with open(sample_file, "r") as sample:
            for l in sample:
                strain = l.strip()
                if strain not in kick:
                    keep.append(strain)
    except Exception as e:
        print(str(e))
        continue

header = f"Conspecifix Results:\n\n\tCompleted on: {datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
header += """\tFor more information about our process, please visit our website at
\thttps://www.conspecifix.com
\tor take a look at our github
\thttps://github.com/Bobay-Ochman

\tExclusion Criterion defined in Bobay & Ochman, GBE 2017
"""

header += "\nThe following strains are members of the species:\n"

h.write(header)
h.write('\n'.join(keep) + '\n\n')

if tag == "no":
    h.write("All strains were determined to be a member of the species")
else:
    h.write("The following strains were determined to NOT be a member of the species:\n")
    h.write('\n'.join(kick) + '\n')

h.truncate()
h.close()

if tag == "yes":  # Tag is if something got excluded
    critInfoFD.write('no')  # so if it did, we write "no"t a member of the species
else:
    critInfoFD.write('yes')

critInfoFD.write('\n\n*Please refer to Bobay & Ochman, GBE 2017')
critInfoFD.close()
