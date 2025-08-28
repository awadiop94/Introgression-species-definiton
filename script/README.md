# script used for the Introgression Analysis!

Requires:
Python* tested with  version 3.5.1 
RAxML tested with version 8.2.12 and RAxML-NG tested with v. 1.2.2-master 
Rscript* https://cran.r-project.org/doc/manuals/r-release/R-admin.html
tested with R version 4.1.0

library(ape)
library(MASS)

* must be executable and in /usr/local/bin
other programs should be copied/moved in /usr/local/bin Or the path to the program should be specified

the different steps:

1. raxml_rooted.py : build gene trees for each aligned core gene family (nucleotide sequence) with RAxML by seleting root1 and root2 based on the core genome tree
					(gene trees wrere build twice based on root1 and root2)
2. extract_names.py
3. branch_length.py
4. cophenetic.R : calculates the cophenetic distance for each pair of original observations in a hierarchical cluster tree
5. identify.py : produces verification1.txt and verification2.txt which containing the introgressed genes shared between species within the same genus
6. reunite_verification.py : summarize the introgressed genes for each introgresed species


# To analyze the introgression fragments along the introgressed gene sequences
1. scan.py


* names.txt : liste of the genomes

* concat_names.fa : core genome alignment file between the reference genomes and the candidate genome
