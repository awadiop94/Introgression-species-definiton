import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]

# --- Step 1: Parse equivalence relations ---
parent = {}

def find(x):
    # union-find "find" with path compression
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x, y):
    # union two sets
    xroot, yroot = find(x), find(y)
    if xroot != yroot:
        # choose lexicographically smaller as representative
        if xroot < yroot:
            parent[yroot] = xroot
        else:
            parent[xroot] = yroot

# Initialize parent dictionary from gene_flow_result_summary.txt
summary_file = project_root / sp / "Gene_Flow" / "QueryDatabase" / "gene_flow_result_summary.txt"
with open(summary_file, "r") as f:
    f_header = f.readline().strip()
    for l in f:
        a = l.strip().split('\t')
        sp1, sp2, relation = a[0], a[1], a[7]

        # ensure all seen clusters have parents
        if sp1 not in parent:
            parent[sp1] = sp1
        if sp2 not in parent:
            parent[sp2] = sp2

        # if clusters are the same, union them
        if relation == "same":
            union(sp1, sp2)

# Compress paths: map each cluster → its representative
cluster_map = {c: find(c) for c in parent}

# --- Step 3: Apply mapping to genome clusters ---
parsed_genomes = set()
output_file = project_root / sp / "ANI_results" / "BSCgenome_clusters.csv"
input_file = project_root / sp / "ANI_results" / "genome_clusters.csv"

with open(output_file, "w") as g, open(input_file, "r") as h:
    h_header = h.readline().strip()
    print(h_header, file=g)

    for l in h:
        a = l.strip().split(',')
        genome, cluster = a[0], a[1]

        if genome in parsed_genomes:
            sys.exit(f"Error: genome ID {genome} is already in the list.")
        parsed_genomes.add(genome)

        # Replace cluster by its representative if in equivalence mapping
        if cluster in cluster_map:
            a[1] = cluster_map[cluster]

        print(','.join(a), file=g)
