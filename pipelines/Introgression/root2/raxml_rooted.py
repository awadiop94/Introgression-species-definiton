import sys
from pathlib import Path
from joblib import Parallel, delayed
import shutil
import glob
import os

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

# Species argument
sp = sys.argv[-1]
species = [sp]

# Define directories
core_dir = project_root / sp / 'core_genome/core'
outgroup_dir = project_root / sp / 'core_genome/outgroup2'
outgroup_dir.mkdir(parents=True, exist_ok=True)

# Collect outgroup strains from genome_clusters.csv
outgroup2 = []
with open(project_root / sp / "ANI_results/genome_clusters.csv") as f:
    for line in f:
        strain, cluster = line.strip().split(",")
        if cluster == "cluster4":
            outgroup2.append(strain)

# Function to process each gene
def process_gene(gene_file):
    if not gene_file.endswith('.fa.align'):
        return None

    outgroup_file = outgroup_dir / gene_file

    if Path(f"{outgroup_file}.tree").exists() or Path(f"{outgroup_file}.raxml.bestTree").exists():
        return f"Skipped {gene_file} (already done)"

    root = 'NA'
    with open(core_dir / gene_file, 'r') as fin, open(outgroup_file, 'w') as fout:
        for line in fin:
            if line.startswith('>'):
                strain = line.strip().lstrip('>').split('&')[0].split(".prot")[0]
                fout.write(f">{strain}\n")
                if strain in outgroup2:
                    root = strain
            else:
                fout.write(line)

    if root == 'NA':
        return f"No root found for {gene_file}"

    # Run RAxML-NG with 4 threads and 100 bootstraps (modify as needed)
    cmd = (
        f"/nas/longleaf/home/adiop2/raxml-ng --all "
        f"--msa {outgroup_file} "
        f"--model GTR+G "
        f"--bs-trees 100 "
        f"--threads 1 "
        f"--prefix {gene_file} "
        f"--outgroup {root}"
    )
    os.system(cmd)

    # Move all RAxML output files to outgroup_dir
    raxml_outputs = glob.glob(f"{gene_file}.raxml.*") + [f"{gene_file}.raxml.bestTree"]
    for out_file in raxml_outputs:
        out_file_path = Path(out_file)
        if out_file_path.exists():
            shutil.move(str(out_file_path), str(outgroup_dir / out_file_path.name))

    # Keep a renamed copy of the best tree
    final_tree = outgroup_dir / f"{gene_file}.raxml.bestTree"
    if final_tree.exists():
        shutil.copy(final_tree, f"{outgroup_file}.tree")

# Run in parallel with 8 workers
files = os.listdir(core_dir)
results = Parallel(n_jobs=8)(delayed(process_gene)(gene) for gene in files)

# Print results
for res in results:
    if res:
        print(res)
