import os
import sys
from pathlib import Path

# -----------------------
# Dynamically detect project root
# Assuming this script is in pipelines/ANI/
project_root = Path(__file__).resolve().parents[2]
# -----------------------

species = [sys.argv[-1]]

for sp in species:
    print(f"Processing species/folder: {sp}")

    ani_dir = project_root / sp / "ANI_results"
    script_path = ani_dir / "cluster_genomes.R"
    genome_pairs_csv = ani_dir / "genome_pairs.csv"
    genome_clusters_csv = ani_dir / "genome_clusters.csv"

    # Make sure ANI_results folder exists
    ani_dir.mkdir(parents=True, exist_ok=True)

    # Check if input CSV exists
    if not genome_pairs_csv.exists():
        raise FileNotFoundError(f"{genome_pairs_csv} does not exist!")

    # Write R script
    with open(script_path, "w") as h:
        h.write(f"""require('tidyverse')
require('glue')

fin_pairs <- '{genome_pairs_csv}'
dout_clusters <- '{ani_dir}'
fout_genomes_clusters <- '{genome_clusters_csv}'

cutoff_cni <- 0.95

cluster_genomes_sl <- function(pairs, similarity, cutoff) {{
  similarity <- enexpr(similarity)
  genomes <- unique(c(pairs$genome_1, pairs$genome_2))
  clusters <- structure(1:length(genomes), names = genomes)
  pairs_same_cluster <- filter(pairs, !! similarity > !! cutoff)
  for (row in 1:nrow(pairs_same_cluster)) {{
    genome_1 <- pairs_same_cluster$genome_1[row]
    genome_2 <- pairs_same_cluster$genome_2[row]
    cluster_1 <- clusters[[genome_1]]
    cluster_2 <- clusters[[genome_2]]
    if (cluster_1 != cluster_2) {{
      clusters[clusters == cluster_2] <- cluster_1
    }}
  }}
  tibble(genome = names(clusters), cluster_temp = unname(clusters)) %>%
    mutate(cluster = as.numeric(factor(cluster_temp))) %>%
    mutate(cluster = str_c("cluster", cluster)) %>%
    select(- cluster_temp)
}}

pairs <- read_csv(fin_pairs)
genomes_clusters <- cluster_genomes_sl(pairs, similarity = cni, cutoff = cutoff_cni)
write_csv(genomes_clusters, fout_genomes_clusters)
""")

    # Run the R script
    os.system(f"Rscript {script_path}")
