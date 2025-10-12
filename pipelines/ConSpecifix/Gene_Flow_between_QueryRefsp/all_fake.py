#!/usr/bin/env python3
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

# Get species from command line
SP = sys.argv[-1]
sp_dir = project_root / SP

# Load distances
dist_file = sp_dir / "core_genome/distances_fake.dist"
dist = {}
with open(dist_file, "r") as f:
	for l in f:
		a = l.strip().split("\t")
		st1, st2 = a[0].strip().split()[0], a[0].strip().split()[1]
		dist.setdefault(st1, {})[st2] = float(a[1])
		dist.setdefault(st2, {})[st1] = float(a[1])

strains = sorted(dist.keys())
print(strains)

# Load sequences from fake.fa
tmp={}
with open(sp_dir / "core_genome/fake.fa", "r") as f:
	for l in f:
		if l[0] == '>':
			nb=0
			tag=0
			sp = l.strip('>').strip('\n') 
			tmp[sp] = []
		else:
			nb += len(l.strip('\n'))
			tmp[sp].append(l.strip('\n'))

seq = {}
for sp in strains:
	seq[sp] = ''.join(tmp[sp])



def code(number,composition,alpha):
	string = "".join(composition)
	if len(number)==1:
		nickname="one"
		best=0
		for N in alpha:
			nb = composition.count(N)
			if nb > best:
				best=nb
				memo=N
		for N in alpha:
			if N != memo and composition.count(N) > 0:
				last = N
		string=string.replace(memo,"0")
		string=string.replace(last,"1")
	elif len(number) == 2:
		nickname = "two"
		memo=""
		best=0
		for N in alpha:
			nb = composition.count(N)
			if nb > best:
				best=nb
				memo=N
		for N in alpha:
			if N != memo and composition.count(N) > 0:
				last = N
		string=string.replace(memo,"0")
		string=string.replace(last,"1")
	elif len(number) == 3:
		nickname="three"
		memo=""
		best=0
		for N in alpha:
			nb = composition.count(N)
			if nb > best:
				best=nb
				memo=N
		best2,memo2=0,""
		for N in alpha:
			if N != memo:
				nb = composition.count(N)
				if nb > best2:
					best2=nb
					memo2 = N
		for N in alpha:
			if N != memo and N != memo2 and composition.count(N) > 0:
				last = N
		string=string.replace(memo,"0")
		string=string.replace(memo2,"1")
		string=string.replace(last,"2")
	elif len(number) == 4:
		nickname = "four"
		memo=""
		best=0
		for N in alpha:
			nb = composition.count(N)
			if nb > best:
				best=nb
				memo=N
		best2,memo2=0,""
		for N in alpha:
			if N != memo:
				nb = composition.count(N)
				if nb > best2:
					best2=nb
					memo2 = N
		best3,memo3=0,""
		for N in alpha:
			if N != memo and N != memo2:
				nb = composition.count(N)
				if nb > best3:
					best3=nb
					memo3 = N
		for N in alpha:
			if N != memo and N != memo2 and N != memo3 and composition.count(N) > 0:
				last = N
		string=string.replace(memo,"0")
		string=string.replace(memo2,"1")
		string=string.replace(memo3,"2")
		string=string.replace(last,"3")
	return [nickname,string]
	




subsets=[strains]
tmp = list(strains)
tmp.remove("fake")
subsets.append(tmp)

print ('GO')

alpha=['A','C','G','T']


# Open result file
fichier=0
with open(sp_dir / "core_genome/result_fake.txt", "w") as g:
	LONGUEUR=len(seq[sp])
	for truc in subsets:
		fichier+=1
		if fichier== 1:
			h=open(sp_dir / "core_genome/all_fake_position.txt", "w")
		elif fichier ==2:
			h=open(sp_dir / "core_genome/all_within_position.txt", "w")
		strains = truc
		bip=[]
		singleton,more=0,0
		i = 0
		r,m=0,0
		while i < LONGUEUR:
			composition=[]
			tmp=[]
			memo=[]
			for sp in strains:
				N = seq[sp][i]
				composition.append(N)
				if N in alpha:
					tmp.append(N)
					memo.append(sp)
			tot = len(tmp)
			all = list(set(tmp))
			unique,duplicate,number=[],[],[]
			for N in all:
				number.append(tmp.count(N))
				if tmp.count(N) >1:
					unique.append(N)
				if tmp.count(N) >0:
					duplicate.append(N)
			gaps=composition.count("-")
			#### CALL function code here
			if len(number) > 1 and float(gaps)/len(strains)<= 0.5:
				string = code(number,composition,alpha)
				while 1 in number:
					number.remove(1)
					singleton+=1
					m+=1
					h.write(str(i) + "\t" + str("m") + "\t" + string[0] + "\t" + string[1] + "\n")
				if len(number) == 2:																		##### 2 #####
					more += 1
					N1,N2 = unique[0],unique[1]
					nt1,nt2 = tmp.count(N1),tmp.count(N2)
					if nt1 <= nt2:
						minor = N1
					elif nt1 > nt2:
						minor = N2
					sac,other=[],[]
					j=0
					while j < len(tmp):
						N,sp = tmp[j],memo[j]
						if N == minor:
							sac.append(sp)
						else:
							other.append(sp)
						j+=1
					INTRA,INTER=[],[]
					for st1 in sac:
						for st2 in sac:
							if st1 != st2:
								INTRA.append(dist[st1][st2])
						for st2 in other:
							INTER.append(dist[st1][st2])
					if max(INTRA) > min(INTER):
						r+=1
						toto='r'
						h.write(str(i) + "\t" + str("h") + "\t" + string[0] + "\t" + string[1]  + "\n")
					else:
						toto='m'
						m+=1
						h.write(str(i) + "\t" + str("m") + "\t" + string[0] + "\t" + string[1]  + "\n")
					bip.append(toto)
				elif len(number) == 3:																		##### 3 #####
					N1,N2,N3 = unique[0],unique[1],unique[2]
					check,check2=0,0
					done=[]
					k=0
					while k < 3:
						N,nt = unique[k],number[k]
						if nt == min(number):
							if check == 0:
								minor1 =  N
								done.append(N)
								check=1
						elif nt == max(number):
							if check2==0:
								major = N
								done.append(N)
								check2=1
						k+=1
					for N in unique:
						if N not in done:
							minor2 = N
					sac1,sac2,other=[],[],[]
					j=0
					while j < len(tmp):
						N,sp = tmp[j],memo[j]
						if N == minor1:
							sac1.append(sp)
						elif N == minor2:
							sac2.append(sp)
						else:
							other.append(sp)
						j+=1
					INTRA,INTER=[],[]
					for st1 in sac1:
						for st2 in sac1:
							if st1 != st2:
								INTRA.append(dist[st1][st2])
						for st2 in other:
							INTER.append(dist[st1][st2])
					if max(INTRA) > min(INTER):
						r+=1
						toto='r'
						h.write(str(i) + "\t" + str("h") + "\t" + string[0] + "\t" + string[1] + "\n")
					else:
						toto='m'
						m+=1
						h.write(str(i) + "\t" + str("m") + "\t" + string[0] + "\t" + string[1] + "\n")
					bip.append(toto)
					INTRA,INTER=[],[]
					for st1 in sac2:
						for st2 in sac2:
							if st1 != st2:
								INTRA.append(dist[st1][st2])
						for st2 in other:
							INTER.append(dist[st1][st2])
					if max(INTRA) > min(INTER):
						r+=1
						toto='r'
						h.write(str(i) + "\t" + str("h") + "\t" + string[0] + "\t" + string[1] + "\n")
					else:
						toto='m'
						m+=1
						h.write(str(i) + "\t" + str("m") + "\t" + string[0] + "\t" + string[1] + "\n")
					bip.append(toto)
				elif len(number) == 4:																		##### 4 #####
					N1,N2,N3,N4 = unique[0],unique[1],unique[2],unique[3]
					done=[]
					check,check2=0,0
					k=0
					while k < 4:
						N,nt = unique[k],number[k]
						if nt == min(number):
							if check==0:
								minor1 =  N
								done.append(N)
								check=1
						elif nt == max(number):
							if check2==0:
								major = N
								done.append(N)
								check2=1
						k+=1
					left=[]
					for N in unique:
						if N not in done:
							left.append(N)
					souvenir=[]
					k=0
					while k < 4:
						N,nt = unique[k],number[k]
						if N in left:
							souvenir.append(nt)
						k+=1
					if souvenir[0] <= souvenir[1]:
						minor2,minor3 = left[0],left[1]
					else:
						minor2,minor3 = left[1],left[0]
					sac1,sac2,sac3,other=[],[],[],[]
					j=0
					while j < len(tmp):
						N,sp = tmp[j],memo[j]
						if N == minor1:
							sac1.append(sp)
						elif N == minor2:
							sac2.append(sp)
						elif N == minor3:
							sac3.append(sp)
						else:
							other.append(sp)
						j+=1
					INTRA,INTER=[],[]
					for st1 in sac1:
						for st2 in sac1:
							if st1 != st2:
								INTRA.append(dist[st1][st2])
						for st2 in other:
							INTER.append(dist[st1][st2])
					if max(INTRA) > min(INTER):
						r+=1
						toto='r'
						h.write(str(i) + "\t" + str("h") + "\t" + string[0] + "\t" + string[1] + "\n")
					else:
						toto='m'
						m+=1
						h.write(str(i) + "\t" + str("m") + "\t" + string[0] + "\t" + string[1] + "\n")
					bip.append(toto)
					INTRA,INTER=[],[]
					for st1 in sac2:
						for st2 in sac2:
							if st1 != st2:
								INTRA.append(dist[st1][st2])
						for st2 in other:
							INTER.append(dist[st1][st2])
					if max(INTRA) > min(INTER):
						r+=1
						toto='r'
						h.write(str(i) + "\t" + str("h") + "\t" + string[0] + "\t" + string[1] + "\n")
					else:
						toto='m'
						m+=1
						h.write(str(i) + "\t" + str("m") + "\t" + string[0] + "\t" + string[1] + "\n")
					bip.append(toto)
					INTRA,INTER=[],[]
					for st1 in sac3:
						for st2 in sac3:
							if st1 != st2:
								INTRA.append(dist[st1][st2])
						for st2 in other:
							INTER.append(dist[st1][st2])
					if max(INTRA) > min(INTER):
						r+=1
						toto='r'
						h.write(str(i) + "\t" + str("h") + "\t" + string[0] + "\t" + string[1] + "\n")
					else:
						toto='m'
						m+=1
						h.write(str(i) + "\t" + str("m") + "\t" + string[0] + "\t" + string[1] + "\n")
					bip.append(toto)

			i+=1		
		try:
			rm = float(r)/m
		except ZeroDivisionError:
			rm = 'NA'
		print  (len(strains),' h/m= ', rm)      #,' r= ',r,' m= ',m	, '   Bips:  r= ',bip.count('r'),'  m= ',bip.count('m'),' |  for ',singleton,' singleton'
		g.write("-".join(truc) + "\t" + str(rm) + "\n")


	h.close()
