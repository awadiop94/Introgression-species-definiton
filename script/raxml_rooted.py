# wrapper to build gene trees for all the aligned *.fa core gene families
import os

files = os.listdir('../core')
here = os.listdir('.')

root1 = [
    'GCA_002777695.1_ASM277769v1_genomic.prot',
    'GCA_002088675.1_ASM208867v1_genomic.prot'
]  # example of selected genomes for root1 to build the gene trees

for gene in files:
    root = 'NA'
    if gene.endswith('.fa'):
        output = gene + ".tree.raxml.bestTree"  # RAxML-NG naming
        if output not in here:
            os.system(f"rm -f {gene}.tree.*")  # clean old runs
            print(output, "is missing")

            with open('../core/' + gene, 'r') as f, open('../root1/' + gene, 'w') as h:
                for l in f:
                    if l.startswith('>'):
                        ID = l.strip().lstrip('>')
                        ID = ID.replace('&', '___')
                        st = ID.split('___')[0]
                        h.write('>' + st + '\n')
                        if st in root1:
                            root = st
                    else:
                        h.write(l)

            if root != 'NA':
                cmd = (
                    f"raxml-ng --all "
                    f"--msa ../root1/{gene} "
                    f"--model GTR+G "
                    f"--bs-trees 100 "
                    f"--threads 1 "
                    f"--outgroup {root} "
                    f"--prefix {gene}.tree "
                    f"--seed 12345"
                )
                os.system(cmd)

                os.system(f"mv {gene}.tree.raxml.bestTree ../root1/{gene}.tree")
            else:
                print('Root missing for gene', gene)
