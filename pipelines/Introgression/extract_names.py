import sys
from pathlib import Path

# -----------------------
# Dynamically detect project root
project_root = Path(__file__).resolve().parents[2]

# Get species from command line
sp = sys.argv[-1]
core_dir = project_root / sp / "core_genome"

# Outgroups to process
outgroups = ["outgroup1", "outgroup2"]

# Symbols to detect in the tree string
symbols = [",", "(", ")", ":", ";"]

for og in outgroups:
    og_dir = core_dir / og
    for tree_file in og_dir.iterdir():
        if tree_file.suffix == ".tree" and tree_file.name.startswith("fam"):
            # Create names output file
            names_file = og_dir / f"names{tree_file.name.split('fam')[1]}.txt"

            with open(tree_file, "r") as f, open(names_file, "w") as g:
                line = f.readline().strip()
                link = {}
                bag = []
                tag = 0
                i = 1
                while i < len(line):
                    j = i - 1
                    if line[i] in symbols:
                        if tag == 1:
                            bag.append(taxa)
                            link[taxa] = souvenir + taxa
                            tag = 0
                    else:
                        if line[j] in ("(", ","):
                            souvenir = line[j]
                            taxa = line[i]
                            tag = 1
                        else:
                            taxa += line[i]
                    i += 1

                print(bag)

                memo = line
                # Rename taxa sequentially
                for nb, stuff in enumerate(bag, start=1):
                    taxa = stuff
                    if nb < 10:
                        new = f"BOZO000{nb}:"
                    elif nb < 100:
                        new = f"BOZO00{nb}:"
                    elif nb < 1000:
                        new = f"BOZO0{nb}:"
                    else:
                        new = f"BOZO{nb}:"

                    # Write mapping to names file
                    g.write(f"{og_dir}\t{tree_file.name}\t{new.strip(':')}\t{taxa}\n")

                    # Update memo for renamed tree
                    taxa_colon = taxa + ":"
                    new_prefix = link[taxa][0] + new if taxa in link else new
                    thingy = link[taxa] + ":" if taxa in link else taxa_colon
                    memo = memo.replace(thingy, new_prefix)

                print(f"Found {len(bag)} taxa in the tree")

            # Build the new renamed tree
            new_tree = ""
            tmp = ""
            tag = 0
            for L in memo:
                if L == ")":
                    tag = 1
                    tmp += L
                if tag == 0:
                    new_tree += L
                elif tag == 1:
                    if L == ":":
                        tmp += L
                        new_tree += tmp
                        tag = 0
                        tmp = ""
            new_tree += tmp
            new_tree += ";"

            renamed_tree_file = og_dir / f"renamed{tree_file.name.split('fam')[1]}"
            with open(renamed_tree_file, "w") as h:
                h.write(new_tree)
