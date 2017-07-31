#!/usr/bin/python
# -*- coding:utf-8 -*-
import cgi, cgitb
from extract_relation import found_relations
from KB_builder import building_syntagm_graph
from generer_faits import generer_faits
from build_graph import run

cgitb.enable() # Affiche les erreurs.

###### ###### ###### ###### Documentation ###

# TITLE # Suppression d'éléments dans les phrases.

# Description #
	# Permet de supprimer des éléments indésirables dans les phrases.

###### ###### ###### ###### Input(s), Output(s) & Parameters ###
###

form = cgi.FieldStorage()

task = 0
if form.getvalue("task"):
	task = int(cgi.escape(form.getvalue("task")))

###

###### ###### ###### ###### Program ###
###

	
# 1] Recherche des relations selon la requête.
def rechercher_relations(desambiguisation, sujet, predicats, objet):
	found_relations(desambiguisation, sujet, predicats, objet)
	return("1")

# 2] Construction du graphe des syntagmes.
def construction_G_syntagmes(desambiguisation):
	syntagms = []
	f_name = "Data/Relations/rel.txt"
	if desambiguisation == 1:
		f_name = "Data/Relations/rel_des.txt"
		
	with open(f_name, "r") as df:
		f_content = df.readlines()
		for i in range(len(f_content)):
			s = f_content[i].strip().split("\t")
			if len(s) == 3:
				suj = s[1].strip()
				obj = s[2].strip()
				syntagms.append(suj)
				syntagms.append(obj)
	# Prise en compte d'une taxonomie (description des ascendants directs).
	# Ordering = clé:obj1-val:[concept1,concept1.1] --> les ancêtres.
	ordering = {}
	if desambiguisation == 1:
		with open("Data/Wordnet/wordnet_graph.tsv", "r") as df:
			f_content = df.readlines()
			for ligne in f_content:
				spl = ligne.strip().split("\t")
				if len(spl) == 2:
					spl_asc_d = spl[1].split(";")
					ordering[spl[0]] = spl_asc_d
					
		
	building_syntagm_graph(syntagms,ordering)
	
	return("2")
	

# 3] Génération des faits.
def generation_des_faits(desambiguisation):
	ascendants = {}
	descendants = {}
	nb_asc = {}
	racine = "[ROOT_SYNTAGME]"
	name_file = "Data/Graphes/kb.dot"
	with open(name_file, "r") as asc_file:
		for ligne in asc_file.readlines():
			spl = ligne.split("->")
			if len(spl) == 2:
				spl[0] = spl[0].strip().split('"')[1]
				spl[1] = spl[1].strip().split('"')[1]
			
				if descendants.has_key(spl[1]):
					descendants[spl[1]].append(spl[0])
				else:
					descendants[spl[1]] = []
					descendants[spl[1]].append(spl[0])
				
				if nb_asc.has_key(spl[0]):
					nb_asc[spl[0]] += 1
				else:
					nb_asc[spl[0]] = 1
	# Calcul de tous les ascendants.
	ascendants[racine] = set()
	queue = [racine]
	while len(queue) > 0:
		node = queue.pop(0)
		if not ascendants.has_key(node):
			ascendants[node] = set()
		
		if descendants.has_key(node):
			for i_n in descendants[node]:
				nb_asc[i_n] -= 1
				if not ascendants.has_key(i_n):
					ascendants[i_n] = set()
				ascendants[i_n].add(node)
				ascendants[i_n] = ascendants[i_n].union(ascendants[node])
				if nb_asc[i_n] == 0:
					queue.append(i_n)
	
	f_name = "Data/Relations/rel.txt"
	if desambiguisation == 1:
		f_name = "Data/Relations/rel_des.txt"
	
	relations = []
	with open(f_name, "r") as df:
		f_content = df.readlines()
		for ligne in f_content:
			relations.append(ligne.strip())
			
	generer_faits(ascendants, relations)
	
	return("3")

# 4] Construction du graphe de faits.
def construction_du_graphe_de_faits():
	name_file = "Data/Graphes/kb.dot"
	run("Data/Relations/all_rel.txt", name_file)
	
	return("-1")

print("Content-type: text/html; charset=utf-8\n")

# Chargement des paramètres.
sujet = []
predicats = []
objet = []
desambiguisation = 0

with open("Data/Inputs/parameters.txt", "r") as df:
	f_content = df.readlines()
	for ligne in f_content:
		spl = ligne.strip().split(":")
		if len(spl) == 2:
			if spl[0] == "sujet":
				sujet.append(spl[1])
			elif spl[0] == "predicats":
				spl_pred = spl[1].split(",")
				for p in spl_pred:
					predicats.append(p)
			elif spl[0] == "objet":
				objet.append(spl[1])
			elif spl[0] == "desambiguisation":
				desambiguisation = int(spl[1])
			
if task == 0:
	print(rechercher_relations(desambiguisation, sujet, predicats, objet))
elif task == 1:
	print(construction_G_syntagmes(desambiguisation))
elif task == 2:
	print(generation_des_faits(desambiguisation))
elif task == 3:
	print(construction_du_graphe_de_faits())











