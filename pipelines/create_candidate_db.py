import os
import sys

path = "/nas/longleaf/home/adiop2/Bioinformatic_tool_awa/"

species=[]

sp = sys.argv[-1]

species = [sp]



todo={}
for sp in species:
	print(sp)
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

for sp in species:
	exclusion = []
	tmp = os.listdir(path + sp +  "/Gene_Flow/ReferenceDatabase/")
	for sp1 in tmp:
		try:
			removal = open(path + sp + "/Gene_Flow/ReferenceDatabase/" + sp1 + "/core_genome/for_removal.txt","r")
			for l in removal:
				exclusion.append(l.strip('\n'))
				for file in exclusion:
					if file in todo[sp1]:
						todo[sp1].remove(file)
		except Exception as e:
			print (str(e))
			continue



for sp in species:
	h=open(path + sp + "/runner.txt", "w" )
	for sp1 in todo:
		for sp2 in todo:
			if sp1 != sp2:
				h.write(sp1 + "\t" + sp2 + "\t" + " ".join(todo[sp2]) + "\n")
				for file in  todo[sp1]:
					if len(todo[sp1]) >= 15:
						try:
							os.mkdir(path + sp + "/Gene_Flow/QueryDatabase/" + sp1 )
						except OSError:
							pass
						try:
							os.mkdir(path + sp + "/Gene_Flow/QueryDatabase/" + sp1 + "/" + sp2 )
						except OSError:
							pass
						try:
							os.mkdir(path + sp + "/Gene_Flow/QueryDatabase/" + sp1 + "/" + sp2 + "/core_genome" )
						except OSError:
							pass

						try:
							tmp = os.listdir(path + sp + "/Gene_Flow/QueryDatabase/" )
							if sp1 in tmp:
								g=open(path + sp + "/Gene_Flow/QueryDatabase/" + sp1 + "/" + sp2 + "/" + "path_to_genome_list.txt", "w" )
								for file in  todo[sp1]:
									g.write(file + "\n")
						except OSError:
							pass

	h.close()
	g.close()
	f.close()

done=[]
fa={}
toto=[]
f = open(path + sp + "/runner.txt", "r")
for l in f:
	a=l.strip("\n").split("\t")
	folder = a[0] + "/" + a[1]
	if folder in done:
		pass
	else:
		toto.append(folder)
		fa[a[1]] = a[2].split(" ")[0]
f.close()


for folder in toto:
	sp1 = folder.split("/")[0]
	sp2 = folder.split("/")[1]
	tmp = os.listdir(path + sp + "/Gene_Flow/QueryDatabase/" )
	if sp1 in tmp:
		file = fa[sp2]
		os.system("cp  " + path + sp + "/genomes/" + file + " " + path + sp +  "/Gene_Flow/QueryDatabase/" + sp1 + "/" + sp2 )
		files = os.listdir(path + sp +  "/Gene_Flow/QueryDatabase/" + sp1 + "/" + sp2)
		h=open(path + sp +  "/Gene_Flow/QueryDatabase/" + sp1 + "/" + sp2 + "/path_to_genome_list.txt","a")
		for file in files:
			if file.endswith(".fa"):
				print(file)
				h.write(file + "\n")
f.close()
h.close()
