import sys
from pathlib import Path
import shutil

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[2]

sp = sys.argv[-1]
species = [sp]

# === Build todo dictionary from genome_clusters.csv ===
todo = {}
genome_csv = project_root / sp / "ANI_results/genome_clusters.csv"
with open(genome_csv, "r") as f:
    for line in f:
        parts = line.strip().split(",")
        if "genome" not in parts[0]:
            file, sp1 = parts[0], parts[1]
            todo.setdefault(sp1, []).append(file)

# === Apply exclusions from ReferenceDatabase ===
ref_db_dir = project_root / sp / "Gene_Flow/ReferenceDatabase"
for sp1_dir in ref_db_dir.iterdir():
    if sp1_dir.is_dir():
        removal_file = sp1_dir / "core_genome/for_removal.txt"
        if removal_file.exists():
            with open(removal_file) as f:
                for line in f:
                    file_to_remove = line.strip()
                    if file_to_remove in todo.get(sp1_dir.name, []):
                        todo[sp1_dir.name].remove(file_to_remove)

# === Create runner.txt and folder structure ===
runner_file = project_root / sp / "runner.txt"
with open(runner_file, "w") as runner_f:
    for sp1, files_sp1 in todo.items():
        for sp2, files_sp2 in todo.items():
            if sp1 == sp2:
                continue
            runner_f.write(f"{sp1}\t{sp2}\t{' '.join(files_sp2)}\n")
            if len(files_sp1) >= 15:
                core_genome_dir = project_root / sp / "Gene_Flow/QueryDatabase" / sp1 / sp2 / "core_genome"
                core_genome_dir.mkdir(parents=True, exist_ok=True)
                path_list_file = core_genome_dir.parent / "path_to_genome_list.txt"
                with open(path_list_file, "w") as f:
                    for file in files_sp1:
                        f.write(file + "\n")

# === Collect folders to copy genomes ===
fa = {}
toto = []
with open(runner_file) as f:
    for line in f:
        sp1, sp2, files_str = line.strip().split("\t")
        folder = f"{sp1}/{sp2}"
        if folder not in toto:
            toto.append(folder)
            fa[sp2] = files_str.split(" ")[0]

# === Copy genome files into QueryDatabase ===
query_db_dir = project_root / sp / "Gene_Flow/QueryDatabase"
for folder in toto:
    sp1, sp2 = folder.split("/")
    dst_dir = query_db_dir / sp1 / sp2
    if dst_dir.parent.exists():
        src_file = project_root / sp / "genomes" / fa[sp2]
        shutil.copy(src_file, dst_dir)
        path_list_file = dst_dir / "path_to_genome_list.txt"
        # Append all .fa files present in the folder
        with open(path_list_file, "a") as f:
            for fa_file in dst_dir.iterdir():
                if fa_file.suffix == ".fa":
                    print(fa_file.name)
                    f.write(fa_file.name + "\n")
