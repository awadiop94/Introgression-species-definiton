import sys
from pathlib import Path
import os

# -----------------------
# Dynamically detect project root
project_root = Path(__file__).resolve().parents[2]
# -----------------------

# Get species from command line
sp = sys.argv[-1]
species_dir = project_root / sp
core_dir = species_dir / "core_genome"

# -----------------------
# root1: outgroup1
# -----------------------
r_file1 = core_dir / "cophenetic1.R"
with open(r_file1, "w") as h:
    h.write(f"""require('ape')
require('MASS')

files = list.files('{core_dir}/outgroup1')

for (stuff in files){{
  toto = grep(".tree",c(stuff))
  if (length(toto) == 1){{
    toto2 = grep("renamed",stuff)
    if (length(toto2)==1){{
      name = paste('{core_dir}/outgroup1/',stuff,sep="")
      print(stuff)
      tree = read.tree(name)
      dist = cophenetic(tree)
      output = paste('{core_dir}/outgroup1/distance_',stuff,sep="")
      write.matrix(dist,file=output)
    }}
  }}
}}
""")

os.system(f"Rscript {r_file1}")

# -----------------------
# root2: outgroup2
# -----------------------
r_file2 = core_dir / "cophenetic2.R"
with open(r_file2, "w") as h:
    h.write(f"""require('ape')
require('MASS')

files = list.files('{core_dir}/outgroup2')

for (stuff in files){{
  toto = grep(".tree",c(stuff))
  if (length(toto) == 1){{
    toto2 = grep("renamed",stuff)
    if (length(toto2)==1){{
      name = paste('{core_dir}/outgroup2/',stuff,sep="")
      print(stuff)
      tree = read.tree(name)
      dist = cophenetic(tree)
      output = paste('{core_dir}/outgroup2/distance_',stuff,sep="")
      write.matrix(dist,file=output)
    }}
  }}
}}
""")

os.system(f"Rscript {r_file2}")
