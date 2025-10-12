import sys
from pathlib import Path

# -----------------------
# Dynamically detect project root
# Assuming this script is in pipelines/ANI/
project_root = Path(__file__).resolve().parents[2]
# -----------------------

# Get species from command line
sp = sys.argv[-1]
species_dir = project_root / sp

# Read genome clusters
name = {}
clusters_file = species_dir / "ANI_results" / "genome_clusters.csv"
with open(clusters_file, "r") as f:
    for line in f:
        a = line.strip().split(",")
        st, ani = a[0], a[1]
        name[st] = ani

# Rename the tree tips
tree_file = species_dir / "core_genome" / "tree.nwk"
tree_rename_file = species_dir / "core_genome" / "tree_rename.nwk"

with open(tree_file, "r") as f:
    tree_newick = f.read()

# Replace names with appended ANI
for st, ani in name.items():
    tree_newick = tree_newick.replace(st, f"{st}_{ani}")

# Write the renamed tree
with open(tree_rename_file, "w") as h:
    h.write(tree_newick)

print(f"Tree renamed and saved to: {tree_rename_file}")
