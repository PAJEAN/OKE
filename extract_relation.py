#!/usr/bin/python
# -*- coding: utf-8 -*-
import re, os
from nltk.corpus import wordnet as wn

###### ###### ###### ###### Documentation ###

# TITLE # Extraction des relations selon la requête.

# Description #
	# Extrait les relations selon une requête.

###### ###### ###### ###### Input(s), Output(s) &  Parameters ###
###
###

###### ###### ###### ###### Functions ###
###

# Root est un synset.
def found_descendants(root, table):
	seen = set()
	seen.add(root)
	queue = []
	queue.append(root)
	while len(queue) > 0:
		n = queue.pop(0)
		hyponyms = n.hyponyms()
		if len(hyponyms) > 0:
			for h in hyponyms:
				if not h in seen:
					queue.append(h)
					seen.add(h)
					table.append(str(h.offset()))
	return table

def generer_motifs(table):
	pattern = ""
	for p in range(len(table)):
		if len(table[p]) > 1:
			table[p] = table[p].lower()
			# Milieu.
			pattern += " "+table[p]+" "
			# Debut.
			pattern += "|^"+table[p]+" "
			# Fin.
			pattern += "| "+table[p]+"$"
			# Unique.
			pattern += "|^"+table[p]+"$"
			if p != (len(table)-1):
				pattern += "|"
	
	return pattern

def found_relations(desambiguisation, sujet, predicats, objet):
	out_rel = open("Data/Relations/rel.txt", "w")
	out_rel_des = open("Data/Relations/rel_des.txt", "w")
	
	relations = []
	
	# Predicats utilisés.
	out_predicats = open("Data/predicats.txt", "w")
	
	# On doit considérer également les descendants des sujets et des objets que l'on considère.
	
	sujets = []
	objets = []
	
	motif = re.compile("[0-9]+")
	recherche = []
	recherche = motif.findall(" ".join(sujet))
	# 1 seule entitée possible.
	if len(recherche) == 1:
		sujets.append(recherche[0])
	recherche = []	
	recherche = motif.findall(" ".join(objet))
	if len(recherche) == 1:
		objets.append(recherche[0])
	
	if len(sujets) > 0 or len(objets) > 0:
		senseIdToSynset = {}
		with open("Data/Wordnet/wordnet_synset_id.txt", "r") as df:
			for ligne in df.readlines():
				spl = ligne.strip().split("\t")
				if len(spl) == 2:
					senseIdToSynset[spl[1]] = wn.synset(spl[0])
	
		if len(sujets) > 0 and sujets[0] in senseIdToSynset:
			sujet += found_descendants(senseIdToSynset[sujets[0]], sujets)
		if len(objets) > 0 and objets[0] in senseIdToSynset:
			objet += found_descendants(senseIdToSynset[objets[0]], objets)
			
	
	
	# Exemple: predicats = [have_to, eat, be_born].
	pattern = "'"
	pattern += generer_motifs(predicats)
	pattern += "'"
	
	motif_sujet = generer_motifs(sujet)
	motif_objet = generer_motifs(objet)
	
	if len(predicats) > 0 and (len(sujet) > 0 or len(objet) > 0):
		f_name = "Data/Relations/Predicats"
		os.system("rm "+f_name+"/*~")
		files = os.popen("ls "+f_name+" | grep -P "+pattern)
		
		for lien in files:
			# Recherche predicat.
			lien = lien.strip()
			#print lien
			# Éviter les prédicats négatifs.
			if "like" in predicats: 
				motif = re.compile("^no | no |^never | never |^cannot | cannot |^not | not |^dont ")
			else: 
				motif = re.compile("^no | no |^never | never |^cannot | cannot |^not | not |^dont |like")
			recherche = motif.search(lien)
			if recherche is None:
			#if len(recherche) == 0:
				out_predicats.write(lien+"\n")
				
				with open(f_name+"/"+lien, "r") as df:
					for ligne in df.readlines():
						spl = ligne.strip().split("\t")
						if len(spl) == 5:
							s_ok = 0
							if len(sujet) > 0:
								motif = re.compile(motif_sujet)
								recherche = []
								recherche = motif.search(spl[1].lower())
								if recherche is None:
									recherche = motif.search(spl[3].lower())
								if not recherche is None:
									s_ok = 1
							else:
								s_ok = 1
							
							o_ok = 0
							if len(objet) > 0:
								motif = re.compile(motif_objet)
								recherche = []
								recherche = motif.search(spl[2].lower())
								if recherche is None:
									recherche = motif.search(spl[4].lower())
								if not recherche is None:
									o_ok = 1
							else:
								o_ok = 1
									
							if s_ok == 1 and o_ok == 1:
								
								rel = ""
								if desambiguisation == 1:
									rel = spl[0]+"\t"+spl[1]+"\t"+spl[2]
									out_rel_des.write(rel+"\n")
									out_rel.write(spl[0]+"\t"+spl[3]+"\t"+spl[4]+"\n")
								else:
									rel = spl[0]+"\t"+spl[3]+"\t"+spl[4]
									out_rel.write(rel+"\n")
									out_rel_des.write(rel+"\n")
									
								if rel != "":
									relations.append(rel)
						
	out_rel.close()
	out_rel_des.close()
	out_predicats.close()
	return relations


#found_relations(1, ["15388"], ["eat"], [])
