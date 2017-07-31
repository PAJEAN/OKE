#!/usr/bin/python
# -*- coding:utf-8 -*-
import cgi, cgitb
from modele_inference import inference
from formatage import formatage

cgitb.enable()

form = cgi.FieldStorage()

task = 0
if form.getvalue("task"):
	task = int(cgi.escape(form.getvalue("task")))

	
# 1] Modeles d'inférence.
def run_inference(modele, valeur_incert):

	f_name = "Data/Phrases/sources.tsv"
	sources = {}
	with open(f_name, "r") as df:
		for ligne in df.readlines():
			spl = ligne.strip().split("\t")
			if len(spl) == 2:
				sources[spl[0]] = int(spl[1])
	
	# Les relations extraites désambiguisées et la prise en compte des ids.
	out = open("Data/Relations/sources.tsv", "w")
	f_name = "Data/Relations/rel_des.txt"
	o_so = {}
	relations = {}
	with open(f_name, "r") as df:
		for ligne in df.readlines():
			spl = ligne.strip().split("\t")
			if len(spl) == 3:
				relation = spl[1]+"\t"+spl[2]
				relations[spl[0]] = [relation, sources[spl[0]]]
				out.write(spl[0]+"\t"+str(sources[spl[0]])+"\n")
	
	out.close()
	del sources
	
	racine = "ROOT"
	graphe_faits = "Data/Graphes/facts.dot"
	# Couples observés et désambiguïsés.
	couples_faits_extraits = relations

	# Chargement des phrases incertaines.
	u_sent_file = "Data/Phrases/uncertainty_sentences.txt"
	id_u_phrases = []
	"""
	with open(u_sent_file, "r") as f:
		for ligne in f.readlines():
			spl = ligne.strip().split("\t")
			if len(spl) == 2:
				id_u_phrases.append(spl[0])
	"""
	
	inference(graphe_faits, couples_faits_extraits, racine, id_u_phrases, modele, valeur_incert)

	return("1")


# 8] Formatage des résultats.	
def formatage_resultats():
	
	# Les relation extraite désambiguisées.
	f_name = "Data/Relations/rel_des.txt"
	o_so = {}
	relations = {}
	with open(f_name, "r") as df:
		for ligne in df.readlines():
			spl = ligne.strip().split("\t")
			if len(spl) == 3:
				relation = spl[1]+"\t"+spl[2]
				if o_so.has_key(relation):
					o_so[relation].append(spl[0])
				else:
					o_so[relation] = [spl[0]]
	
	# Les relation extraite non désambiguisées.
	f_name = "Data/Relations/rel.txt"
	o_so_inversed = {}
	with open(f_name, "r") as df:
		for ligne in df.readlines():
			spl = ligne.strip().split("\t")
			if len(spl) == 3:
				relation = spl[1]+"\t"+spl[2]
				o_so_inversed[spl[0]] = relation

	# On stock les traces du support.
	# Calculé par modele_inference.py.
	f_name = "Data/Resultats/traces.txt"
	traces = {}
	with open(f_name, "r") as df:
		for ligne in df.readlines():
			spl = ligne.strip().split("_")
			if len(spl) == 2:
				traces[spl[0]] = set(spl[1].strip().split(";"))

	# On stock le support.
	f_name = "Data/Resultats/propagation.txt"
	support = {}
	with open(f_name, "r") as df:
		for ligne in df.readlines():
			spl = ligne.strip().split("_")
			if len(spl) == 2:
				support[spl[0]] = float(spl[1])

	# On stock le profondeur.
	f_name = "Data/Resultats/profondeur.txt"
	profondeur = {}
	with open(f_name, "r") as df:
		for ligne in df.readlines():
			spl = ligne.strip().split("_")
			if len(spl) == 2:
				profondeur[spl[0]] = int(spl[1])
	
	f_name = "Data/Relations/sources.tsv"
	sources = {}
	with open(f_name, "r") as df:
		for ligne in df.readlines():
			spl = ligne.strip().split("\t")
			if len(spl) == 2:
				sources[spl[0]] = int(spl[1])

	# On recherche les phrases associées aux relations.	
	f_name = "Data/Phrases/id_phrases.txt"
	id_phrases = {}
	with open(f_name, "r") as df:
		for ligne in df.readlines():
			spl = ligne.strip().split("\t")
			if len(spl) == 2:
				id_phrases[spl[0]] = spl[1]
		
	# Chargement des phrases incertaines.
	u_sent_file = "Data/Phrases/uncertainty_sentences.txt"
	id_u_phrases = []
	"""
	with open(u_sent_file, "r") as f:
		for ligne in f.readlines():
			spl = ligne.strip().split("\t")
			if len(spl) == 2:
				id_u_phrases.append(spl[0])
	"""

	formatage(o_so, o_so_inversed, traces, support, profondeur, id_phrases, id_u_phrases, sources)

	return("-1")

print("Content-type: text/html; charset=utf-8\n")

# Chargement des paramètres.
modele = 2
valeur_incert = 1.0

with open("Data/Inputs/parameters.txt", "r") as df:
	f_content = df.readlines()
	for ligne in f_content:
		spl = ligne.strip().split(":")
		if len(spl) == 2:
			if spl[0] == "modele":
				modele = int(spl[1])
			elif spl[0] == "incertitude":
				valeur_incert = float(spl[1])

if task == 0:
	print(run_inference(modele, valeur_incert))
elif task == 1:
	print(formatage_resultats())










