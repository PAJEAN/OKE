#!/bin/python
# -*- coding: utf-8 -*-
import time

"""
	Creer le graphe de fait a partir des asc du MeSH et de couple de faits.
"""

def build_descendants(asc_file, racine):
	graph = {racine:set()}
	for ligne in asc_file:
		spl = ligne.strip().split("->")
		if len(spl) == 2:
			concept = spl[1].strip()
			specification = spl[0].strip()
			concept = concept[1:-1]
			specification = specification[1:-1]
			if graph.has_key(specification):
				if not concept in graph[specification]:
					graph[specification].add(concept)
			else:
				graph[specification] = set()
				graph[specification].add(concept)

	nb_desc = {}

	leaves = list()

	for n in graph:

		if not n in nb_desc: nb_desc[n] = 0

		for a in graph[n]:
		    if not a in nb_desc: nb_desc[a] = 1
		    else: nb_desc[a] += 1

	for n in nb_desc:
		if nb_desc[n] == 0: leaves.append(n)

	queue = leaves
	descendants = {}

	while(len(queue) != 0):
	
		n = queue.pop()
		if(not n in descendants): descendants[n] = set()
		descendants[n].add(n)
	
		for p in graph[n]:
			nb_desc[p] -= 1
			if(not p in descendants): descendants[p] = set()
		
			descendants[p].update(descendants[n])
			
			if(nb_desc[p] == 0):
				queue.append(p)

	return descendants

def trier_couples(couples, descendants):
	count = {}
	new_couples = []
	for couple in couples:
		nb_des = 0
		for elm in couple:
			if descendants.has_key(elm):
				nb_des += len(descendants[elm])
		str_couple = couple[0]+"\t"+couple[1]
		count[str_couple] = nb_des
		
	trieDecroissant = lambda dico : sorted(dico.items(), lambda a,b: cmp(a[1],b[1]), reverse=True)
	count = trieDecroissant(count)
	
	for key in count:
		spl = key[0].split("\t")
		new_couples.append(spl)

	return new_couples
	
def build_couples(couples_file):
	couples = []
	for ligne in couples_file:
		info = ligne.split("\t")
		if len(info) < 3:
			quit()
		sujet = info[1].strip()
		objet = info[2].strip()
		couples.append( [sujet, objet] )
	return couples

def comparaison_couple(couple1, couple2, descendants):
	rel1_2 = 0
	rel_suj1_2 = 0
	rel_obj1_2 = 0
	if couple1[0] == couple2[0]:
		# Alors sujet1 = sujet2.
		rel_suj1_2 = 1
	# On verifie si descendants a la cle. Si ce n'est pas le cas c'est que c'est une feuille.
	elif descendants.has_key(couple1[0]) and couple2[0] in descendants[couple1[0]]:
		# Alors sujet2 < sujet1.
		rel_suj1_2 = 2
	elif descendants.has_key(couple2[0]) and couple1[0] in descendants[couple2[0]]:
		# Alors sujet1 < sujet2.
		rel_suj1_2 = 3
	else:
		# Sinon sujet1 ! sujet2.
		rel_suj1_2 = 0
		
	if rel_suj1_2 > 0:
		# Alors il y a une relation entre sujet 1 et 2.
		if couple1[1] == couple2[1]:
			# Alors objet1 = objet2.
			rel_obj1_2 = 1
		elif descendants.has_key(couple1[1]) and couple2[1] in descendants[couple1[1]]:
			# Alors objet2 < objet1.
			rel_obj1_2 = 2
		elif descendants.has_key(couple2[1]) and couple1[1] in descendants[couple2[1]]:
			# Alors objet1 < objet2.
			rel_obj1_2 = 3
		else:
			# Sinon objet1 ! objet2.
			rel_obj1_2 = 0
			
		if rel_obj1_2 > 0:
			# Possibilite.
			if rel_suj1_2 == 1:
				if rel_obj1_2 == 1:
					# Egalite.
					rel1_2 = -1
				elif rel_obj1_2 == 2:
					# rel2 < rel1
					rel1_2 = 1
				elif rel_obj1_2 == 3:
					# rel1 < rel2
					rel1_2 = 2
					
			elif rel_suj1_2 == 2:
				if rel_obj1_2 == 1 or rel_obj1_2 == 2:
					# rel2 < rel1
					rel1_2 = 1
			elif rel_suj1_2 == 3:
				if rel_obj1_2 == 1 or rel_obj1_2 == 3:
					# rel1 < rel2
					rel1_2 = 2
	return rel1_2

# Construction du graphe.
# Si sup à 0 alors ils sont relié.
# Si = à 1 alors couple2 < couple1 donc f'(couple_fp) < f.
# Si = à 2 alors couple1 < couple2 donc f < f'.
def build_graph(couples, descendants):
	# Pour annoter les liens de descendances.
	graph_d = {"ROOT":[]}
	nb_couple = 0
	
	# Memoire pour éviter de passer plusieurs fois par le même noeud.
	
	for couple_f in couples:
		queue = [["ROOT"]]
		colored = set()
		str_couple_f = couple_f[0]+"\t"+couple_f[1]
		
		nb_couple += 1
		#print "\n-------------------------------- \n"+str(nb_couple)+" / "+str(len(couples))+"\n--------------------------------"
		#print "## Couple a placer: "+str_couple_f
		
		# On ajoute le nouveau fait dans le graphe.
		graph_d[str_couple_f] = []
		while len(queue) > 0:
			couple_fp = queue.pop()
			racine = 0

			if couple_fp[0] == "ROOT":
				racine = 1
				
			if racine == 0:
				str_couple_fp = couple_fp[0]+"\t"+couple_fp[1]
			else:
				str_couple_fp = "ROOT"
							
			colored.add(str_couple_fp)
			match = 0
			
			if graph_d.has_key(str_couple_fp):
			
				if len(graph_d[str_couple_fp]) > 0:
				
				
					for str_fils_fp in graph_d[str_couple_fp]:
				
						fils_fp = str_fils_fp.split("\t")
					
						# Actualisation de la racine.
						if not str_fils_fp == "ROOT":
							racine = 0
						
						if racine == 0:
							rel_1_2 = comparaison_couple(couple_f, fils_fp, descendants)
						else:
							# La racine est supérieur à tous les faits.
							rel_1_2 = 2
					
						if rel_1_2 > 0:
							match = 1
						
							if rel_1_2 == 2:
								# On créer le lien f' <- f.
								if not str_fils_fp in colored:
									colored.add(str_fils_fp)
									queue.append(fils_fp)
									
							elif rel_1_2 == 1:
								# On créer le lien f <- f'.
								# Inutile car faits ordonnées.
								print "Erreur 1! Comparaison : "+str_couple_f+" ET : "+str_fils_fp
								quit()
				else:
					#print "FEUILLE"
					# Pas d'enfant.
					# Soit notre fait prend le(s) père(s) de f' soit il se met en dessous.
					
					# On recompare de nouveau des noeuds qui ont été comparé dans rel_1_2 == 2.
					
					if racine == 0:
						rel_1_2 = comparaison_couple(couple_f, couple_fp, descendants)
					else:
						# La racine est supérieur à tous les faits.
						rel_1_2 = 2

					if rel_1_2 > 0:
						match = 1
						if rel_1_2 == 1:
							# Inutile car faits ordonnées.
							print "Erreur 2! Comparaison : "+str_couple_f+" avec : "+str_couple_fp
							quit()

						elif rel_1_2 == 2:
							#print "create "+str_couple_fp + "--->" + str_couple_f
							graph_d[str_couple_fp].append(str_couple_f)
			else:
				print "Noeud manquant :"+str_couple_fp
						
			# Aucun des fils ne match.
			if match == 0:
				
				# On creer le noeud à partir de couple_fp.
				if not graph_d.has_key(str_couple_fp):
					graph_d[str_couple_fp] = []
				graph_d[str_couple_fp].append(str_couple_f)
				
				
	return graph_d

def run(file_couple, file_descendants):
	couples_file = open(file_couple, "r").readlines()
	descendants_file = open(file_descendants, "r").readlines()
	
	racine = "[ROOT_SYNTAGME]"
	
	# Build couples.
	couples = build_couples(couples_file)
	# Build descendants.
	descendants = build_descendants(descendants_file, racine)
	# Build order on couples.
	couples = trier_couples(couples, descendants)

	adjacences = build_graph(couples, descendants)
	# Build graph 
	# command dot -Tpdf graph_file -o graph_file.pdf
	
	#graph_file = "graph_random_f.dot"
	graph_file = "Data/Graphes/facts.dot"
	with open(graph_file,"w") as output :
		output.write("digraph word_graph {\n \t rankdir=BT\n")
		for node in adjacences.keys():
			for adj in adjacences[node]:
				output.write( "\t\""+adj+"\" -> \""+node+"\""+"\n")
		output.write("}\n")


				
				
				
				
				
				
				
				
				
				
				
				
				
				
