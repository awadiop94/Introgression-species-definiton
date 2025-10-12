import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

for sp in species:
    tag = sp.replace("/", "__")
    
    fake_fa_path = project_root / sp / "core_genome" / "fake.fa"
    distances_path = project_root / sp / "core_genome" / "distances_fake.dist"

    # Run RAxML
    os.system(f"/proj/bobaylab/users/adiop2/standard-RAxML-master/raxmlHPC -f x -p 12345 -s {fake_fa_path} -m GTRGAMMA -n {tag} -T 12")
    
    # Move the distances file
    os.system(f"mv RAxML_distances.{tag} {distances_path}")
