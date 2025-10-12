import sys
from pathlib import Path

# --------------------------
# Dynamic project root
project_root = Path(__file__).resolve().parents[2]

# Species from command line
SP = sys.argv[-1]
species_dir = project_root / SP
core_dir = species_dir / "core_genome"

# --------------------------
# Read verification1.txt (outgroup1)
chain = {}
intro = {}
not_intro = {}

verification1_file = core_dir / "outgroup1" / "verificationBSC_1.txt"
with verification1_file.open("r") as f:
    for l in f:
        a = l.strip().split("\t")
        file, sp = a[1], a[2]
        if a[0] == "introgression":
            intro.setdefault(file, []).append(sp)
            chain.setdefault(file, {})[sp] = a[-1]
        elif a[0] == "not_introgression":
            not_intro.setdefault(file, []).append(sp)

# --------------------------
# Read verification2.txt (outgroup2)
intro2 = {}
not_intro2 = {}

verification2_file = core_dir / "outgroup2" / "verificationBSC_2.txt"
with verification2_file.open("r") as f:
    for l in f:
        a = l.strip().split("\t")
        file, sp = a[1], a[2]
        if a[0] == "introgression":
            intro2.setdefault(file, []).append(sp)
            chain.setdefault(file, {})[sp] = a[-1]
        elif a[0] == "not_introgression":
            not_intro2.setdefault(file, []).append(sp)

# --------------------------
# Filter introgressions
problem = {}
nb = 0
tot = 0
seen = {}
compteur = {}

filtered_file = core_dir / "filtered_introgressionBSC.txt"
with filtered_file.open("w") as h:

    # From intro (outgroup1)
    for file in intro:
        for sp in intro[file]:
            tag = 0
            if file in not_intro2 and sp in not_intro2[file]:
                tag = 1
            tot += 1
            if tag == 0:
                resu = file + "_" + sp
                seen[resu] = "y"
                compteur[sp] = compteur.get(sp, 0) + 1
                h.write(f"{file}\t{sp}\n")

                for st in chain[file][sp].split(" "):
                    problem[st] = problem.get(st, 0) + 1
                nb += 1

    # From intro2 (outgroup2)
    for file in intro2:
        for sp in intro2[file]:
            tag = 0
            if file in not_intro and sp in not_intro[file]:
                tag = 1
            tot += 1
            if tag == 0:
                resu = file + "_" + sp
                if resu not in seen:
                    compteur[sp] = compteur.get(sp, 0) + 1
                    print("intro2", file, sp)
                    h.write(f"{file}\t{sp}\n")

                    for st in chain[file][sp].split(" "):
                        problem[st] = problem.get(st, 0) + 1
                    nb += 1

# --------------------------
# Print summary
print(nb, tot)
for st, count in problem.items():
    if count > 300:
        print(st, count)

for sp, count in compteur.items():
    print(sp, count)
