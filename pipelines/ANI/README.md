# Average nucleotide identity (ANI) of core genes and ANI clustering
Requires the EMBOSS program distmat (tested successfully with emboss/6.6.0)

IMPORTANT:copy or move emboss distmat into /usr/local/bin/
Or the path to the program "distmat" should be specified: in rule GenomeCluster (Snakefile_stage1)) and in the 
script "calculate_anis_coregenes.py " inside the module ANI

###########################################################################

Python (tested with python v3.5.1, must be on your local path))
	pathlib
Rscript https://cran.r-project.org/doc/manuals/r-release/R-admin.html
Requires the R package (tested with R version 4.1.0, must be on your local path)
tidyverses packages, installed by running install.packages('tidyverse') in R.
glue package, installed by running install.packages('glue') in R.

