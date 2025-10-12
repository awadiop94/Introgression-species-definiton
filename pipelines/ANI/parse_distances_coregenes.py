import sys
from pathlib import Path
import os

# -----------------------
# Dynamically detect project root
# Assuming this script is in pipelines/ANI/
project_root = Path(__file__).resolve().parents[2]
# -----------------------

# Get species from command line
species = [sys.argv[-1]]

for sp in species:
    print(f"Processing species/folder: {sp}")

    # Paths
    ani_dir = project_root / sp / "ANI_results"
    r_script_path = ani_dir / "parse_distances_coregenes.R"
    core_ani_dir = project_root / sp / "core_genome" / "ani_core_genes"

    # Ensure output directory exists
    ani_dir.mkdir(parents=True, exist_ok=True)

    # Write the R script
    with open(r_script_path, "w") as h:
        h.write(f"""require('tidyverse')

folder <- '{core_ani_dir}/'
file_list <- list.files(path=folder, pattern=".distmat")
for (f in file_list) {{
    fin_cnis <- paste0('{core_ani_dir}/', f)
    fout_pairs <- paste0('{core_ani_dir}/', gsub('cnis', 'genome_pairs', gsub('.distmat', '.csv', f)))

    gca_regex <- "GC[AF]_[0-9]+\\\.[0-9]"

    read_phylip_distmat <- function(path, skip = 8, include_diagonal = T) {{
        distances_raw <- readr::read_tsv(path, col_names = F, skip = skip) %>%
            separate(ncol(.), into = c("name", "number"), sep = " ")
        names <- distances_raw$name
        n <- length(names)
        distances <- distances_raw %>%
            select_if(~ ! all(is.na(.))) %>%
            select(1:(!! n)) %>%
            `names<-`(names) %>%
            mutate(sequence_1 = !! names) %>%
            gather(key = "sequence_2", value = "distance", - sequence_1, na.rm = T) %>%
            mutate_at("distance", as.double)
        distances_1 <- filter(distances, sequence_1 >= sequence_2)
        distances_2 <- distances %>%
            filter(sequence_1 < sequence_2) %>%
            mutate(sequence_1_temp = sequence_2, sequence_2_temp = sequence_1) %>%
            select(sequence_1 = sequence_1_temp, sequence_2 = sequence_2_temp, distance)
        distances <- bind_rows(distances_1, distances_2)
        if (! include_diagonal) {{
            distances <- filter(distances, sequence_1 != sequence_2)
        }}
        distances
    }}

    cnis_unique <- read_phylip_distmat(fin_cnis, include_diagonal = F, skip = 8)
    cnis_unique <- cnis_unique %>%
        rename(genome_1 = sequence_1, genome_2 = sequence_2) %>%
        mutate(cni = 1 - distance / 100) %>%
        select(genome_1, genome_2, cni)

    pairs <- cnis_unique %>%
        mutate(noise = runif(nrow(.), min = - 0.01, max = 0.01)) %>%
        select(- noise)

    write_csv(pairs, fout_pairs)
}}
""")

    # Run the R script
    os.system(f"Rscript {r_script_path}")
