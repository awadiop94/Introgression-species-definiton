#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

# Get species name from command line
sp = sys.argv[-1]
species = [sp]

for sp in species:
    r_file = project_root / sp / "core_genome/make_distrib_curvegraph.R"
    
    with open(r_file, "w") as h:
        h.write(f"""
tab = read.table('{project_root}/{sp}/core_genome/topcand.txt')
vector_cand = tab$V2

tabe2 = read.table('{project_root}/{sp}/core_genome/topref.txt')
vector_ref = tabe2$V2

tabe3 = read.table('{project_root}/{sp}/core_genome/result_fake.txt')
fake = tabe3$V2[1]

all_values = c(vector_cand, vector_ref)

pdf('{project_root}/{sp}/core_genome/cand_refdistrib.pdf')

plot(density(vector_cand), col='black', type='l', xlim=c(0,max(all_values)), xlab='h/m', ylab='density', main='{sp} hmdistribution')
lines(density(vector_ref), col='green', type='l', xlim=c(0,max(all_values)))
abline(v=fake, lty=2, col='red')

legend(x='topleft', legend=c('genome candidat', 'genome reference', 'fake'),
       col=c('black', 'green', 'red'), lty=1, cex=0.8)

pv1 = wilcox.test(vector_cand, mu=mean(vector_ref))[3]$p.value
pv2 = wilcox.test(vector_cand, mu=fake)[3]$p.value

write(c(pv1, pv2), ncol=2, file='{project_root}/{sp}/core_genome/double_test.txt')

dev.off()
""")
    
    # Execute the R script
    os.system(f"Rscript {r_file}")
