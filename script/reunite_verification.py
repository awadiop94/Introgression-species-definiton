
import os
import sys



chain={}
intro={}
not_intro={}
f=open("../root1/verification1.txt","r")
for l in f:
	a=l.strip("\n").split("\t")
	file=a[1]
	sp=a[2]
	if a[0] == "introgression":
		if file not in intro:
			intro[file] = [sp]
			chain[file]={}
			chain[file][sp]=a[-1]
		else:
			intro[file].append(sp)
			chain[file][sp]=a[-1]
	elif a[0] == "not_introgression":
		if file not in not_intro:
			not_intro[file] = [sp]
		else:
			not_intro[file].append(sp)

f.close()


intro2={}
not_intro2={}
f=open("../outgroup2/verification2.txt","r")
for l in f:
	a=l.strip("\n").split("\t")
	file=a[1]
	sp=a[2]
	if a[0] == "introgression":
		if file not in chain:
			chain[file]={}
		tag=0
		if file not in intro2:
			intro2[file] = [sp]
		else:
			intro2[file].append(sp)
		if sp not in chain[file]:
			chain[file][sp]=a[-1]
	elif a[0] == "not_introgression":
		if file not in not_intro2:
			not_intro2[file] = [sp]
		else:
			not_intro2[file].append(sp)


f.close()



problem={}
nb=0
tot=0
seen={}
h=open("../filtered_introgression1.txt","w")
compteur={}
for file in intro:
	for sp in intro[file]:
		tag=0
		if file in not_intro2:
			if sp in not_intro2[file]:
				tag=1
		tot+=1
		if tag == 0:
			resu = file + "_" + sp
			seen[resu] = "y"
			if sp not in compteur:
				compteur[sp]=0
			compteur[sp]+=1
			h.write(file + "\t" + sp + "\n")

			sub = chain[file][sp].split(" ")
			for st in sub:
				if st in problem:
					problem[st]+=1
				else:
					problem[st]=1
			nb+=1


for file in intro2:
	for sp in intro2[file]:
		tag=0
		if file in not_intro:
			if sp in not_intro[file]:
				tag=1
		tot+=1
		if tag == 0:
			resu = file + "_" + sp
			if resu not in seen:
				if sp not in compteur:
					compteur[sp]=0
				compteur[sp]+=1
				print("intro2",file,sp)
				h.write(file + "\t" + sp + "\n")

				sub = chain[file][sp].split(" ")
				for st in sub:
					if st in problem:
						problem[st]+=1
					else:
						problem[st]=1
				nb+=1



h.close()

print(nb,tot)

for st in problem:
	if problem[st] > 300:
		print(st,problem[st])





for sp in compteur:
	print(sp,compteur[sp])
