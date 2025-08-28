
import os
import sys


classification={}
ANI = {}
f=open("../genome_clusters.csv","r")
for l in f:
	a=l.strip("\n").strip("\r").split(",")
	st = a[0]
	sp = a[1]
	#print(st,sp)
	classification[st]=sp
	if sp in ANI:	
		ANI[sp].append(st)
	else:
		ANI[sp]=[st]

f.close()

names = {}
files = os.listdir("../root1/")

print("Read Trees")








real_name = {}
for TREE in files:
	if TREE.endswith(".tree") and TREE.startswith("fam"):
		name = "names" + TREE.split("fam")[1] + '.txt'
		f=open("../root1/" + name,"r")
		for l in f:
			a=l.strip("\n").split("\t")
			file = a[1]
			file =  "renamed" +  TREE.split("fam")[1] 
			file = file.split(".tree")[0] + ".txt"
			if file in names:
				pass
			else:
				names[file]={}
				real_name[file]={}
			st = a[-1]
			short=a[2]
			names[file][st] = short
			real_name[file][short]=st
			#print(st,short)

		f.close()

print("names is built")



print("loading distances")
dist={}
for matrix in files:
	if matrix.startswith("distance_"):
		print(matrix)
		tree = matrix.split("distance_")[1].split(".tree")[0] + ".txt"
		dist[tree]={}
		f=open("../root1/" + matrix ,"r")
		l=f.readline()
		vector=l.strip("\n").split(" ")
		i=0
		for l in f:
			
			short1 = vector[i]
			if short1 not in dist[tree]:
				dist[tree][short1]={}
			a=l.strip("\n").split(" ")
			j=0
			while j < len(a):
				short2 = vector[j]
				dist[tree][short1][short2] = float(a[j])
				if short2 not in dist[tree]:
					dist[tree][short2]={}
				dist[tree][short2][short1] = float(a[j])
				j+=1
			i+=1
		f.close()
			
				


print("distances loaded")
			
			

		




h=open("../root1/verification1.txt","w")
for file in names:
	print(file)
	tmp={}
	number={}
	for sp in ANI:
		tmp[sp]=[]
		number[sp]=0
		for st in ANI[sp]:
			if st in names[file]:
				tmp[sp].append(names[file][st])
				parent = classification[st]
				number[parent] += 1
	string=""
	for sp in number:
		#print(sp," = ",number[sp])
		string += str(number[sp]) + " "
	#print(file,string)	
	
	

		
	
	MIN,MAX={},{}

	storage={}
	for spi in number:
		storage[spi]=""
		MIN[spi],MAX[spi]=1000000,0
		f=open("../root1/" + file,"r")
		for l in f:
			a=l.strip("\n").split("\t")
			if 1==1:
				#print(sp1,MAX[spi],MIN[spi])
				chain = a[1]
				#if chain in reverse:
				if 1==1:
					compteur={}
					for sp in number:
						compteur[sp]=0
					#print(chain)
					b=chain.split("-")
					for short in b:
						st = real_name[file][short]
						sp = classification[st]
						compteur[sp]+=1
					if compteur[spi] > MAX[spi]:
						MAX[spi] = int(compteur[spi])
						MIN[spi] = 1000000
					elif compteur[spi] == MAX[spi]:
						if len(b) < MIN[spi]:
							MAX[spi] = int(compteur[spi])
							MIN[spi] = int(len(b))
							storage[spi]=b
					string=""
					for sp in number:
						string += str(compteur[sp]) + " "
					#print("chain",string)
					
				
		f.close()

	roots=[]
	f=open("../root1/" + "roots_" + file.split(".tree")[0] ,"r" )
	for l in f:
		st = l.strip("\n")
		for sp in tmp:
			if st in tmp[sp]:
				if sp not in roots:
					roots.append(sp)
					#print("root",st,sp,len(tmp[sp]))
	f.close()

	for spi in storage:
		#if MAX[spi] > number[spi]:
		
		box = storage[spi]
		strain_tank,tank=[],[]
		for short in box:
			st = real_name[file][short]
			sp = classification[st]		
			if sp != spi:
				tank.append(sp)
				strain_tank.append(st)
		if len(tank) > 0 and spi not in roots:
			#print("intro",spi,number[spi],len(tank),list(set(tank)))
			small_in,small_out=[],[]
			if file in dist:
				for short1 in box:
					st1= real_name[file][short1]
					sp1= classification[st1]
					for short2 in box:
						st2= real_name[file][short2]
						sp2= classification[st2]
						if sp1 == spi or sp2 == spi:
							if sp1==sp2:
								small_in.append(dist[file][short1][short2])
							else:
								small_out.append(dist[file][short1][short2])
						#print(sp1,sp2,dist[file][short1][short2])
				if len(small_in) > 0:
					if max(small_in) <= min(small_out):
						result="not_introgression"
					else:
						result="introgression"
				
					print(result,file,spi,len(tank),list(set(tank)),max(small_in),"<",min(small_out),"?")
					h.write(result + "\t" + file + "\t" + spi + "\t" + str(len(tank)) + "\t" + "_".join(tank) + "\t" + " ".join(strain_tank) + "\n")
				else:
					print("EMPTY",file,spi,len(tank),list(set(tank)),small_in,"<",small_out,"?")
			else:
				print(file, "MISSING")







h.close()


