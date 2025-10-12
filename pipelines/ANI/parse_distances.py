import sys
import os
from pathlib import Path

# -----------------------
# Dynamically detect project root
# Assuming this script is in pipelines/ANI/
project_root = Path(__file__).resolve().parents[2]
# -----------------------

# Get species from command line
species = [sys.argv[-1]]

for sp in species:
    print(f"Processing species/folder: {sp}")

    ani_dir = project_root / sp / "ANI_results"
    r_script_path = ani_dir / "parse_distances.R"
    ani_distmat = ani_dir / "ani" / "ani.distmat"
    genome_pairs_csv = ani_dir / "genome_pairs.csv"

    # Ensure output directory exists
    ani_dir.mkdir(parents=True, exist_ok=True)

    # Check if input distmat exists
    if not ani_distmat.exists():
        raise FileNotFoundError(f"{ani_distmat} does not exist!")

    # Write the R script
    with open(r_script_path, "w") as h:
        h.write(f"""require('tidyverse')

fin_cnis <- '{ani_distmat}'
fout_pairs <- '{genome_pairs_csv}'

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
    mutate(noise = runif(nrow(.), min = -0.01, max = 0.01)) %>%
    select(- noise)

write_csv(pairs, fout_pairs)
""")

    # Run the R script
    os.system(f"Rscript {r_script_path}")
