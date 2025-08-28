import sys
import os




files = os.listdir("../root1/")


for TREE in files:
	if TREE.endswith(".tree") and TREE.startswith("fam"):
		

		name = "names" + TREE.split("fam")[1] + '.txt'
		g=open("../root1/" + name,"w")
		f=open("../root1/" + TREE,"r")
		l=f.readline()

		symbols=[",","(",")",":",";"]



		link={}
		bag=[]
		tag=0
		l=l.strip("\n")
		i=1
		while i < len(l):
			j=i-1
			if l[i] in symbols:
				if tag == 1:
					bag.append(taxa)
					link[taxa] = souvenir + taxa
					tag=0
			else:
				if l[j] == "(" or l[j] == ",":
					souvenir=l[j]
					taxa = l[i]
					tag=1
				else:
					taxa+=l[i]
			i+=1


		print(bag)


		memo=l


		
		nb=0
		for stuff in bag:
			if 1==1:
				if 2==2:
					taxa = stuff
					#print(taxa)
					nb+=1
					if nb < 10:
						new = "BOZO000" + str(nb) + ":"
					elif nb < 100:
						new = "BOZO00" + str(nb)  + ":"
					elif nb < 1000:
						new = "BOZO0" + str(nb)  + ":"
					elif nb < 10000:
						new = "BOZO" + str(nb)  + ":"
					g.write("../root1/" + "\t" + TREE + "\t" + new.strip(":") + "\t" + taxa + "\n")
					taxa = taxa + ":"
					new = link[taxa.strip(":")][0] + new 
					thingy = link[taxa.strip(":")] + ":"
					memo = memo.replace(thingy,new)


		print("Found ",nb,"taxa in the tree")


		new=""
		tmp=""
		tag=0
		for L in memo:
			if L == ")":
				tag=1
				tmp+=L
			if tag==0:
				new+=L
			elif tag==1:
				if L==":":
					tmp+=L
					new+=tmp
					tag=0
					tmp=""

		new += tmp 
		new+=";"
		
		renamed_tree = "renamed" +  TREE.split("fam")[1]
		
		h=open("../root1/" + renamed_tree,"w")
		h.write(new)
		h.close()

		g.close()
