script used for the Introgression Analysis!

Requires: Python* tested with  version 3.5.1
RAxML-NG tested with v. 1.2.2-master 
Rscript* https://cran.r-project.org/doc/manuals/r-release/R-admin.html tested with R version 4.1.0

library(ape)
library(MASS)

* must be executable and in /usr/local/bin other programs should be copied/moved in /usr/local/bin Or the path to the program should be specified

the different steps:

1. raxml_rooted.py : build gene trees for each aligned core gene family (nucleotide sequence) with RAxML-NG by seleting root1 and root2 based on 
the core genome tree (gene trees wrere build twice based on root1 and root2)
2. extract_names.py
3. branch_length.py
4. cophenetic.R : calculates the cophenetic distance for each pair of original observations in a hierarchical cluster tree
5. identify.py : produces verification_1.txt/verificationBSC_1.txt and verification_2.txt/verificationBSC_2.txt which containing
the introgressed genes shared between species within the same genus
6. reunite_verification.py : summarize the introgressed genes for each introgresed species
