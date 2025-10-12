#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

sp = sys.argv[-1]
species = [sp]

for sp in species:
    r_script_path = project_root / sp / "core_genome" / "make_kmean_graph.R"
    kmeans_file = project_root / sp / "core_genome" / "kmeans.txt"
    hmgraph_file = project_root / sp / "core_genome" / "hmGraph.png"
    removal_file = project_root / sp / "core_genome" / "for_removal.txt"

    with open(r_script_path, "w") as h:
        h.write(f"""require('outliers')

tab=read.table('{kmeans_file}')
listOfValues= tab$V3

maxVal <- round(max(listOfValues))+1
if ( maxVal > 100){{
    maxVal <- 100
}}
minVal <- round(min(listOfValues))-1
if (minVal < 0){{
    minVal <- 0
}}

#calculate our breaks specifically because after removing outliers, breaks will change if defaults are used
ourBreaks <- seq(minVal, maxVal, (maxVal - minVal)/20 )

png('{hmgraph_file}' ,width = 6,
  height    = 6,
  units     = "in",
  res       = 200)
#graph of everything. Will be red since the "good ones" will be kept later on and be printed over
p1 <- hist(tab$V3,breaks = ourBreaks,plot = FALSE)

if  (chisq.out.test(listOfValues)[3][1]$p.value == "NaN"){{
write("",ncol=1,file='{removal_file}')
}}

#remove all outliers identified with pvalues of <.0001
flag = TRUE
while ( chisq.out.test(listOfValues)[3][1]$p.value < .0001 && flag==TRUE)
{{
    oldlistOfValues = listOfValues
    listOfValues = rm.outlier(listOfValues, fill = FALSE)
    if(min(oldlistOfValues) != min(listOfValues)){{
        flag = FALSE
        listOfValues = oldlistOfValues
    }}
}}

maxAfterOutliers <- max(listOfValues)
strainsForRemoval <- tab$V1[which(tab$V3 > maxAfterOutliers)]
strainsForRemoval = as.character(strainsForRemoval)
print(strainsForRemoval)
write(strainsForRemoval,ncol=1,file='{removal_file}')

#these are just the ones that are members of the species. They get green
p2 <- hist(listOfValues,breaks = ourBreaks,plot = FALSE)

#actually plot the data
plot( p1, col='firebrick1',main = 'Outliers', xlab="frequency of appearance in lower mode",ylab="numb strains")  # first histogram
plot( p2, col='darkolivegreen3', add=T) 

dev.off()
""")

# Run the R script
os.system(f"Rscript {r_script_path}")
