A workflow form performing core genome analysis, ANI clustering, gene flow inference and biological species classification,
and inferring introgression between ANI-species and BSC-species, respectively, using the core genome in a modular and reproducible fashion.

The pipeline is implemented in Snakemake and split into three stages for clarity
and modularity. Each stage can be run independently, or all stages can be run sequentially
via a master Snakefile.

📂 Directory Structure
Introgression-species-definiton/
├── Snakefile_stage1
├── Snakefile_stage2
├── Snakefile_stage3
├── pipelines/
│   ├── CoreCruncher/
│   ├── ANI/
│   ├── ConSpecifix/
│   └── Introgression/
├── GENOMES/
│   └── genomes/   # Input FASTA files
└── README.md


