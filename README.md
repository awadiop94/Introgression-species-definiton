# A workflow for performing core genome analysis, ANI clustering, gene flow inference and biological species classification, and inferring introgression between ANI-species and BSC-species, respectively, using the core genome in a modular and reproducible fashion.

The pipeline is implemented in Snakemake and split into three stages for clarity and modularity. Each stage can be run independently, or all stages can be run sequentially via a bash script (to be created if needed).


## Directory Structure:
```
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
│   └── genomes/   # Input FASTA files (we tested the pipeline with 32 genomes of Campylobacter)
└── README.md
```

## Installation
### Clone the repository
```
git clone https://github.com/awadiop94/Introgression-species-definiton.git
cd Introgression-species-definiton
```
### Install Snakemake and dependencies
Recommended: Install with Conda (or Mamba)

#### Using Conda:
```
conda create -n snakemake -c conda-forge -c bioconda snakemake
conda activate snakemake
```
#### Using Mamba (faster):
```
mamba create -n snakemake -c conda-forge -c bioconda snakemake
mamba activate snakemake
```

## snakemake pipeline main Requirements
```
EMBOSS program distmat (tested successfully with emboss/6.6.0)
python* (must call python ≥ 3.7 from typing 'python')
RAxML tested with version 8.2.12 
RAxML-NG tested with v. 1.2.2-master (used to build the gene trees)
Rscript* https://cran.r-project.org/doc/manuals/r-release/R-admin.html tested with R version 4.1.0
mafft
USEARCH: https://www.drive5.com/usearch/, which is required by CoreCruncher, (please see the CoreCruncher documentation on how to alternatively use `BLAST`)
FasTtree
```	
Additional dependencies needed to run specifically each module of this workflow are described in the README.md file
located within each corresponding module folder

## Input Data
```
GENOMES/genomes/
```
## Running the Pipeline
```
snakemake -s Snakefile_master -j 20
```
(-j 20 specifies 20 threads; adjust for your system.)

### Run a specific stage

Stage 1:
```
snakemake -s Snakefile_stage1 -j 20 --use-conda --latency-wait 240
```
Stage 2:
```
snakemake -s Snakefile_stage2 -j 20 --use-conda --latency-wait 240
```
Stage 3:
```
snakemake -s Snakefile_stage3 -j 20 --use-conda --latency-wait 240
```
	
## Workflow Stages

### Stage 1 → Core Genome, ANI Species clustering and Reference Database
```
Rules:
	•	core_genome_within_genus
	•	GenomeClustering
	•	reference_Database

Output:
	•	configref.yaml
```
	
### Stage 2 → Within-species Gene Flow and Query Database
```
Rules:
	•	core_genome_within_species
	•	gene_flow_refsp
	•	build_QueryDatabase

Output:
	•	configcand.yaml
```
	
### Stage 3 → Between-species Gene Flow and BSC Introgression
```
Rules:
	•	core_genome_between_species
	•	gene_flow_refcandsp
	•	normalize_gene_flow_value
	•	collect_gene_flow_summary
	•	ANI_introgression
	•	BSCCluster
	•	BSC_introgression

Outputs:
	•	GENOMES/Gene_Flow/QueryDatabase/gene_flow_result_summary.txt
	•	GENOMES/core_genome/filtered_introgression.txt"
	•	GENOMES/core_genome/filtered_introgressionBSC.txt
	•	GENOMES/ANI_results/BSCgenome_clusters.csv
```
### Expected Results
At the end of the workflow you will obtain:
```
	•	Core genome within the genus
	•	ANI clustering results and core gene sequences identities
    •	Reference configuration (configref.yaml) and reference database
	•	Candidate configuration (configcand.yaml) and candidate query database
	•	Gene flow results (for Biological species classification (BSC species)) --> ConSpecifix
	•	Final BSC species clusters
	•	Core genome introgression summaries
```
## Notes

### building the gene trees:
In practice, each gene tree was rooted twice using two different species as an outgroup alternatively (please change the outgroup in line 25 in root1/raxml_rooted.py and root2/raxml_rooted.py, if needed based on the species you selected as outgroup (we tested the pipeline using 32 genomes of Campylobacter and we selected cluster3 and cluster4 (ANI-species3 and ANI-species4, respectively)) to build the gene trees

### snakemake issues
If a job is interrupted or incomplete, the output directory need to be unlocked before re-analyze the job again to complete the job/analysis by running:
```
snakemake --unlock -s Snakefile
```
Snakefile shoulde be the specific Snakefile_stage... that was interupted or in which the job was incomplete

	
## Additional issues
If all the genomes analyzed are classified into one ANI-species, all other Snakefile_stages of the pipeline will fail after 
Snakefile_stage1 complete because the introgression events inference require comparing at least two species.

If there is no ANI-species which contains more than 15 genomes in the ReferenceDatabase: all the other Snakefile_stages of the 
pipeline except rule core_genome_within_genus and rule GenomeCluster in Snakefile_stage1 will fail.

It's the same case if there is no Reference ANI-species which contains more than 15 genomes to build the QueryDatabase.
	
## Citation

If you use this workflow, please cite:

Diop A, Douglas GM and Bobay LM. Introgression impacts the evolution of bacteria, but species borders are rarely fuzzy.
Nat Commun 2025

## Workflow Overview

### Stage 1: Core genome & Reference Database
![Stage 1 DAG](workflow_stage1.png)
```
snakemake -s Snakefile_stage1 --dag | dot -Tpng > workflow_stage1.png
```

### Stage 2: Within-species Gene Flow & Query Database
![Stage 2 DAG](workflow_stage2.png)
```
snakemake -s Snakefile_stage2 --dag | dot -Tpng > workflow_stage2.png
```

### Stage 3: Between-species Gene Flow & BSC Introgression
![Stage 3 DAG](workflow_stage3.png)
```
snakemake -s Snakefile_stage3 --dag | dot -Tpng > workflow_stage3.png
```
### Full Workflow
![Master DAG](workflow_master.png)
```
snakemake -s Snakefile_master --dag | dot -Tpng > workflow_master.png
```
This requires Graphviz (dot command). Install it with:
conda install -c conda-forge graphviz
