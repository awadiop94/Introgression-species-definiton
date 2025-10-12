import sys
from pathlib import Path

# --------------------------
# Detect project root dynamically
project_root = Path(__file__).resolve().parents[2]

# Species from command line
SP = sys.argv[-1]
species_dir = project_root / SP
core_dir = species_dir / "core_genome"

# --------------------------
# Read genome classification and ANI clusters
classification = {}
ANI = {}
genome_csv = species_dir / "ANI_results/BSCgenome_clusters.csv"

with genome_csv.open("r") as f:
    for l in f:
        a = l.strip().split(",")
        st, sp = a[0], a[1]
        classification[st] = sp
        ANI.setdefault(sp, []).append(st)

# --------------------------
# Function to process an outgroup
def process_outgroup(outgroup: str):
    og_dir = core_dir / outgroup
    files = [f for f in og_dir.iterdir() if f.is_file()]
    
    print(f"Reading trees for {outgroup}")
    
    # Build names and real_name dictionaries
    names = {}
    real_name = {}
    for tree_file in files:
        if tree_file.suffix == ".tree" and tree_file.name.startswith("fam"):
            names_file = og_dir / f"names{tree_file.name.split('fam')[1]}.txt"
            if not names_file.exists():
                continue
            with names_file.open("r") as f:
                for l in f:
                    a = l.strip().split("\t")
                    file_key = "renamed" + tree_file.name.split("fam")[1]
                    file_key = file_key.split(".tree")[0] + ".txt"
                    names.setdefault(file_key, {})
                    real_name.setdefault(file_key, {})
                    st, short = a[-1], a[2]
                    names[file_key][st] = short
                    real_name[file_key][short] = st
    print("names dictionary built")
    
    # Load distances
    print("Loading distances")
    dist = {}
    for matrix_file in files:
        if matrix_file.name.startswith("distance_"):
            tree_key = matrix_file.name.split("distance_")[1].split(".tree")[0] + ".txt"
            dist[tree_key] = {}
            with matrix_file.open("r") as f:
                vector = [x for x in f.readline().strip().split() if x]
                for i, l in enumerate(f):
                    short1 = vector[i]
                    dist[tree_key].setdefault(short1, {})
                    values = [x for x in l.strip().split() if x]
                    for j, val_str in enumerate(values):
                        try:
                            val = float(val_str)
                        except ValueError:
                            continue
                        short2 = vector[j]
                        dist[tree_key][short1][short2] = val
                        dist[tree_key].setdefault(short2, {})[short1] = val
    print("Distances loaded")
    
    # Verification output
    verification_file = og_dir / f"verificationBSC_{1 if outgroup=='outgroup1' else 2}.txt"
    with verification_file.open("w") as h:
        for file_key in names:
            tmp, number = {}, {}
            for sp in ANI:
                tmp[sp] = []
                number[sp] = 0
                for st in ANI[sp]:
                    if st in names[file_key]:
                        tmp[sp].append(names[file_key][st])
                        parent = classification[st]
                        number[parent] += 1
            
            MIN, MAX = {}, {}
            storage = {}
            for spi in number:
                storage[spi] = ""
                MIN[spi], MAX[spi] = 1000000, 0
                file_path = og_dir / file_key
                with file_path.open("r") as f:
                    for l in f:
                        chain = l.strip().split("\t")[1]
                        compteur = {sp_: 0 for sp_ in number}
                        for short in chain.split("-"):
                            st = real_name[file_key][short]
                            sp_ = classification[st]
                            compteur[sp_] += 1
                        if compteur[spi] > MAX[spi]:
                            MAX[spi] = int(compteur[spi])
                            MIN[spi] = 1000000
                        elif compteur[spi] == MAX[spi]:
                            if len(chain.split("-")) < MIN[spi]:
                                MAX[spi] = int(compteur[spi])
                                MIN[spi] = int(len(chain.split("-")))
                                storage[spi] = chain.split("-")
            
            # Load roots
            roots_file = og_dir / f"roots_{file_key.split('.tree')[0]}"
            roots = []
            if roots_file.exists():
                with roots_file.open("r") as f:
                    for l in f:
                        st = l.strip()
                        for sp in tmp:
                            if st in tmp[sp] and sp not in roots:
                                roots.append(sp)
            
            # Compare distances for introgression
            for spi in storage:
                box = storage[spi]
                strain_tank, tank = [], []
                for short in box:
                    st = real_name[file_key][short]
                    sp_ = classification[st]
                    if sp_ != spi:
                        tank.append(sp_)
                        strain_tank.append(st)
                
                if tank and spi not in roots and file_key in dist:
                    small_in, small_out = [], []
                    for short1 in box:
                        st1 = real_name[file_key][short1]
                        sp1 = classification[st1]
                        for short2 in box:
                            st2 = real_name[file_key][short2]
                            sp2 = classification[st2]
                            if sp1 == spi or sp2 == spi:
                                if sp1 == sp2:
                                    small_in.append(dist[file_key][short1][short2])
                                else:
                                    small_out.append(dist[file_key][short1][short2])
                    if small_in:
                        result = "not_introgression" if max(small_in) <= min(small_out) else "introgression"
                        print(result, file_key, spi, len(tank), list(set(tank)), max(small_in), "<", min(small_out), "?")
                        h.write(f"{result}\t{file_key}\t{spi}\t{len(tank)}\t{'_'.join(tank)}\t{' '.join(strain_tank)}\n")
                    else:
                        print("EMPTY", file_key, spi, len(tank), list(set(tank)), small_in, "<", small_out, "?")
                elif file_key not in dist:
                    print(file_key, "MISSING")


# --------------------------
# Process both outgroups
for og in ["outgroup1", "outgroup2"]:
    process_outgroup(og)
