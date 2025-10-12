
import sys
from pathlib import Path

# Dynamically detect project root (two levels up from this script)
project_root = Path(__file__).resolve().parents[2]

# Species folder from command line
SP = sys.argv[-1]
species_dir = project_root / SP
core_dir = species_dir / "core_genome"

# List of outgroups to process
outgroups = ["outgroup1", "outgroup2"]

for outgroup in outgroups:
	outgroup_dir = core_dir / outgroup
	forest = [f for f in outgroup_dir.iterdir() if f.suffix == ".tree" and f.name.startswith("renamed")]
	print(f"{outgroup} trees found:", forest)

	for file_path in forest:
		base_name = file_path.stem
		unique = []
	
		print("Processing:", file_path.name)
		new_file = outgroup_dir / f"{base_name}.txt"
	
		# Read tree
		with open(file_path, "r") as f:
			l=f.readline()
			l = l.strip("\n")
			l = l.strip(";")
			f.close()

			numbers=["0","1","2","3","4","5","6","7","8","9"]
			resu=""
			i=0
			while i < len(l):
				L = l[i]
				if l[i] in numbers:
					if i ==0:
						resu+=l[i]	
					elif l[i-1] == ")" or l[i-2] == ")" or l[i-3] == ")":
						pass
					else:
						resu+=l[i]
				else:
					resu+= l[i]
				i+=1
		
		
			resu = l
		
		
			I = 1
			
			dico={}
			detail={}
			arbre={}
			arbre[I]=resu
			first={}
			level={}
			length={}
			node=0
			while arbre[I].count("(") > 1:
				groupe=[]
				memo=[]
				resu=str(arbre[I])
				resu2 = resu
				#node=0
				i=0
				mark=0
				while i < len(resu):
					k = resu[i]
					if k == "B" or k == "n":
						name=k
						mark=0
					elif k != "," and k !="("  and k !=")" and k !=":":
						if mark == 0:
							name += k
						elif mark == 1:
							branch += k
					elif k == ':':
						branch = ''
						mark=1
					else:
						if k=="," or k ==')': 
							length[name] = branch
							if 'B' in name:
								if name not in unique:
									with open(new_file, "a") as h:
										h.write(f"{name}\t{name}\t{abs(float(branch))}\ttip\n")
									unique.append(name)
							mark=0
						if k==",":
							if resu[i+1] == "B" or  resu[i+1] =="n":
								if name not in memo:
									groupe=[name]
								else:
									groupe=[]
						if k == ")":
							if name not in groupe:
								if name not in memo:
									if len(groupe) == 1:
										groupe.append(name)
										memo.extend(groupe)
										node += 1
										NODE = "n" + str(I) + "_" + str(node)
										mono = "(" + groupe[0] + ':' + length[groupe[0]] + "," + groupe[1] + ':' + length[groupe[1]] + ")" 
										if mono in resu2:
											level[NODE] = I
											resu2 = resu2.replace(mono,NODE)
											I+=1
											dico[NODE] = [groupe[0] , groupe[1]]
											if "B" not in groupe[0]:
												detail[NODE] = list(detail[groupe[0]])
											else:
												detail[NODE] =[groupe[0]]
											if "B" not in groupe[1]:
												for stuff in detail[groupe[1]]:
													detail[NODE].append(stuff)
											else:
												detail[NODE].append(groupe[1])
											i=0
											break
										else:
											node = node - 1
					i+=1
				arbre[I] = resu2

		
			MAX_I = int(I)
		
			print ("MAX_I ", arbre[MAX_I])
			
			ROOTS=[]
			nb=0
			if ":" in arbre[MAX_I]:
				a=arbre[MAX_I].strip("(").strip(")").split(",")
				for truc in a:
					nb+=1
					#if "B" in truc:
					sub_a = truc.split(":")
					name=sub_a[0]
					print (file_path.name," root" + str(nb) + ": ",name)
					if name not in unique:
						out = truc
						detail["root" + str(nb)] = [name]
						length[name] = sub_a[1].strip("(").strip(")")
						ROOTS.append(name)
						if name.startswith("B"):
							with open(new_file, "a") as h:
								h.write(f"{name}\t{name}\t{length[name]}\ttip\n")
					else:
						ROOTS.append(name)
			
			
			
			parent={}
			for NODE in detail:
				detail[NODE].sort()
				composit = NODE.split("_")[0] + "_" + "-".join(detail[NODE])
				try:
					LENGTH= length[NODE] 
				except KeyError:
					LENGTH='root'
				if "-".join(detail[NODE]) not in unique:
					if LENGTH=="root":
						if ":" in "-".join(detail[NODE]):
							finish = "-".join(detail[NODE]).split(":")[0]
							print ("Finish= ",finish)
							if NODE in  ROOTS:
								tag="root"
							else:
								tag="branch"
							with open(new_file, "a") as h:
								h.write(f"{NODE}\t{finish}\t{LENGTH}\t{tag}\n")
					else:
						if NODE in  ROOTS:
							tag="root"
						else:
							tag="branch"
						with open(new_file, "a") as h:
							h.write(f"{NODE.split("_")[0]}\t{"-".join(detail[NODE])}\t{LENGTH}\t{tag}\n")
					unique.append("-".join(detail[NODE]))
				for st in detail[NODE]:
					if st in parent:
						parent[st].append(NODE)
					else:
						parent[st] = [NODE]
		
		
			print ("ROOTS= ",ROOTS)
			
			# Write dichotomies file
			dich_file = outgroup_dir / f"dichotomies_{base_name}.txt"
			with open(dich_file, "w") as h:
				for st in dico:
					resu1,resu2,resu3=st,dico[st][0],dico[st][1]
					resu1,resu2,resu3=resu1.split("_")[0],resu2.split("_")[0],resu3.split("_")[0]
					h.write(f"{resu1}\t{resu2}\t{resu3}\n")

			# Write roots file
			roots_file = outgroup_dir / f"roots_{base_name}.txt"
			with open(roots_file, "w") as h:			
				for root in ROOTS:
					h.write(root.split("_")[0] + "\n")
