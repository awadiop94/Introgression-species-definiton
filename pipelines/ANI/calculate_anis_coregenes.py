import os
import sys
from pathlib import Path

# -----------------------
# Dynamically detect project root
# Assuming this script is in pipelines/ANI/
project_root = Path(__file__).resolve().parents[2]
# -----------------------

# Get the species folder from command line
sp = sys.argv[-1]

# Path to the species folder
species_dir = project_root / sp

# Path to the core genome folder
core_genome_dir = species_dir / "core_genome" / "core"

# Path to output ANI core genes folder
ani_core_dir = species_dir / "core_genome" / "ani_core_genes"
ani_core_dir.mkdir(parents=True, exist_ok=True)

# Iterate over aligned FASTA files
for fasta_file in core_genome_dir.iterdir():
    if fasta_file.suffix == ".align":
        output_file = ani_core_dir / f"cnis_{fasta_file.name}.distmat"
        print(f"Processing {fasta_file.name} → {output_file.name}")
        os.system(f"distmat -sequence {fasta_file} -nucmethod 0 -outfile {output_file}")
