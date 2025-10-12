import os
import sys

path = "/nas/longleaf/home/adiop2/Bioinformatic_tool_awa/"

species=[]

sp = sys.argv[-1]

species = [sp]






todo={}
for sp in species:
	f=open(path + sp + "/ANI_results/genome_clusters.csv", "r" )
	for l in f:
		a=l.strip("\n").split(",")
		if "genome" not in a[0]:
			file = a[0]
			sp1 = a[1]
			if sp1 not in todo:
				todo[sp1] = [file]
			else:
				todo[sp1].append(file)

	f.close()
	
	f = open(path + "configref.yaml", "w")
	f.write("dirname" + ":" + "\n")
	for sp1 in todo:
		print(sp1)
		if len(todo[sp1]) >= 15:
			f.write(" " + "-" + " " + sp1 + "\n")
			for file in  todo[sp1]:
				print(file)
				try:
					os.mkdir(path + sp + "/Gene_Flow/ReferenceDatabase/" + sp1 )
				except OSError:
					pass
				try:
					h=open(path + sp + "/Gene_Flow/ReferenceDatabase/" + sp1 + "/" + "path_to_genome_list.txt", "w" )
					for file in  todo[sp1]:
						h.write(file + "\n")
				except OSError:
					pass
f.close()
h.close()
g.close()
