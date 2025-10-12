import os
import sys
import yaml

path = "/nas/longleaf/home/adiop2/Bioinformatic_tool_awa/"

sp = sys.argv[-1]

todo={}

f=open(path + sp + "/ANI_results/genome_clusters.csv", "r" )
for l in f:
	a=l.strip("\n").split(",")
	if "genome" not in a[0]:
		file = a[0]
		sp1 = a[1]
		if sp1 not in todo:
			todo[sp1] = [file]
		else:

			todo[sp1].append(file)

f.close()

# Load the todo dict that you already built earlier in your script
# Select reference clusters with >= 15 genomes
valid_refs = {ref for ref, genomes in todo.items() if len(genomes) >= 15}

runner_file = os.path.join(path, sp, "runner.txt")

# Dictionary to hold ref -> list of candidate clusters
ref_to_cands = {}

with open(runner_file, "r") as f:
    for line in f:
        a = line.strip().split("\t")
        if len(a) < 2:
            continue
        ref, cand = a[0], a[1]

        # Only keep ref clusters that passed the >=15 filter
        if ref not in valid_refs:
            continue

        if ref not in ref_to_cands:
            ref_to_cands[ref] = []
        if cand not in ref_to_cands[ref]:
            ref_to_cands[ref].append(cand)

# Write configcand.yaml
out_file = os.path.join(path, "configcand.yaml")
with open(out_file, "w") as f:
    yaml.dump(ref_to_cands, f, default_flow_style=False, sort_keys=False)

print(f"Wrote {out_file}")
