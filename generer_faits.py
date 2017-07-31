#!/bin/python
# -*- coding: utf-8 -*-	

def generer_faits(ascendants, faits):
	out = open("Data/Relations/all_rel.txt", "w")
	racine = "[ROOT_SYNTAGME]"
	count = 0
	check = set()
	for ligne in faits:
		count += 1
		info = ligne.strip().split("\t")
		if len(info) == 3:
			info[0] = info[0].strip() # ID.
			info[1] = info[1].strip()
			info[2] = info[2].strip()
			relation = info[1]+"\t"+info[2]
			if not relation in check:
				check.add(relation)
				if ascendants.has_key(info[1]) and ascendants.has_key(info[2]):
					# On ajoute le propre noeud pour faciliter le produit cartesien.
					ascendants[info[1]].add(info[1])
					ascendants[info[2]].add(info[2])
					for asc_1 in ascendants[info[1]]:
						if asc_1 != racine:
							for asc_2 in ascendants[info[2]]:
								if asc_2 != racine:
									out.write(info[0]+"\t"+asc_1+"\t"+asc_2+"\n")
				else:
					print "Non comptabilisée : "+ligne
	out.close()





					
	






















	
