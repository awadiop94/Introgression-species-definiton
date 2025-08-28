
import os
import numpy
import sys




REF = "Acidovorax_avenae"

SP = "Acidovorax_citrulli"

tmp = sys.argv

REF = tmp[-2]
SP = tmp[-1]

print(REF,SP)

exclusion=[]

marker={}
f=open("/../" + REF + "/" + SP +  "/names.txt","r")
for l in f:
	a=l.strip("\n").split("\t")
	id,name=a[0],a[1]
	if name not in exclusion:
		marker[id]="y"

f.close()


tmp={}
f=open("/../" + REF + "/" + SP +  "/concat_names.fa","r")
nb=0
for l in f:
	if l[0]==">":
		nb+=1
		id = l.strip("\n").strip(">")
		if id == "out":
			tag=1
		elif id not in marker:
			tag=0
			nb = nb - 1
		if nb > 1000:
			tag=0
		else:
			tag=1
		tmp[id]=[]
	elif tag==1:
		tmp[id].append(l.strip("\n"))


f.close()

strains = list(tmp.keys())

seq={}
for id in strains:
	seq[id] = "".join(tmp[id])
	del tmp[id]

L  = len(seq[id])

strains.remove("out")

alpha = {}
alpha["A"]="y"
alpha["C"]="y"
alpha["G"]="y"
alpha["T"]="y"


dico={}
out={}
i=0
while i < L:
	print(i)
	j = i + 100
	if j > L:
		j = L
	bin=[]
	tag=0
	for st1 in strains:
		tot=0
		nb=0.0
		I = i
		while I < j:	
			N1,O = seq[st1][I],seq["out"][I]
			if N1 in alpha and O in alpha:
				tot+=1
				if N1 == O:
					nb+=1
			I+=1
			if tot >= 75:
				bin.append(nb/tot)
	#print(bin)
	if len(bin) > 0:
		out[i] =  [numpy.mean(bin),numpy.median(bin),min(bin),max(bin)]
		tag=1
	else:
		tag=0
	if tag==1:
		bin = []
		k=0
		while k < len(strains):	
			st1 = strains[k]
			n = k+1
			while n < len(strains):
				st2 = strains[n]
				#print(st1,st2)
				tot=0
				nb=0.0
				I = i
				while I < j:
					N1,N2 = seq[st1][I],seq[st2][I]
					if N1 in alpha and N2 in alpha:
						if N1 == N2:
							nb+=1
						tot+=1
					I+=1
				if tot >= 75:
					bin.append(nb/tot)
				n+=1
			k+=1
		if len(bin)> 0:
			#print(bin)
			dico[i] = [numpy.mean(bin),numpy.median(bin),min(bin),max(bin)]
	i+=100
		

limit = max(list(dico.keys()))
h=open("/../" + REF + "/" + SP +  "/scan.txt","w")
h.write("Index\tPos\tMean_ref\tMedian_ref\tMin_ref\tMax_ref\tMean_out\tMedian_out\tMin_out\tMax_out\n")
nb=0
i=0
while i < limit:
	if i in dico:
		nb+=1
		print(dico[i],out[i])
		h.write(str(nb) + "\t" + str(i) + "\t" + str(dico[i][0]) +  "\t" + str(dico[i][1]) + "\t" + str(dico[i][2]) + "\t" + str(dico[i][3]) + "\t" + str(out[i][0]) + "\t" + str(out[i][1]) + "\t" + str(out[i][2]) + "\t" + str(out[i][3]) + "\n")
	i+=100





