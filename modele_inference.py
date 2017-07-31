#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import numpy as np

######
# To compute deepth, belief and plosibility.
######

# u_sent = [id_sent].
def freq_faits(relations, racine, u_sent, val_inc):
	# To compute score about Subjet and Objet.
	score = {racine:0}
	total = 0
	# Les fichiers avec uniquement les faits extraits.
	for ident in relations:
		
		relation = relations[ident][0]
		total += 1
		
		val_rel = 1.0
		if ident in u_sent:
			val_rel = val_inc
		
		if relation in score:
			score[relation] += val_rel * float(relations[ident][1])
		else:
			score[relation] = val_rel * float(relations[ident][1])
			
	return score

def build_direct_ascendants(desc_file, racine):
	graph = {racine:set()}
	for ligne in open(desc_file, "r").readlines():
		spl = ligne.strip().split("->")
		if len(spl) == 2:
			specification = spl[0].strip()
			concept = spl[1].strip()
			concept = concept[1:-1]
			specification = specification[1:-1]
			# Transformation en ascendant.
			if graph.has_key(specification):
				if not concept in graph[specification]:
					graph[specification].add(concept)
			else:
				graph[specification] = set()
				graph[specification].add(concept)
	return graph

# Graph is the direct ascendants.
def build_descendants(graph, racine):
	nb_desc = {}
	# Compute number of descendants after the construction of graph.
	# Because we use set() so we do not have double.
	for n in graph:
		if not n in nb_desc: 
			nb_desc[n] = 0
		
		for a in graph[n]:
		    if not a in nb_desc: 
		    	nb_desc[a] = 1
		    else: 
		    	nb_desc[a] += 1
		    	
	leaves = list()
	for n in nb_desc:
		if nb_desc[n] == 0:
			leaves.append(n)

	queue = leaves
	descendants = {}
	while(len(queue) != 0):
		n = queue.pop()
		if(not n in descendants):
			descendants[n] = set()
			
		descendants[n].add(n)
	
		for p in graph[n]:
			nb_desc[p] -= 1
			
			if(not p in descendants): 
				descendants[p] = set()
			descendants[p].update(descendants[n])
			
			if(nb_desc[p] == 0):
				queue.append(p)

	return descendants

def propagation(descendances, score, racine):
	# Tous les descendants.
	#file_desc = open(graphe_faits, "r").readlines()
	#descendances = build_descendants(file_desc, racine)
	# Chaque noeud dans descendances possède sa propre feuille.
	nb_desc = {}
	for i in descendances.keys():
		nb_desc[i] = len(descendances[i])
	
	# On veut traiter dans un premier temps le noeud avec le plus de descendants (racine) puis descendre.
	trieDecroissant = lambda dico : sorted(dico.items(), lambda a,b: cmp(a[1],b[1]), reverse=True)
	nb_desc_tri = trieDecroissant(nb_desc)
	
	# Calcul de la croyance.
	
	# Traces.
	traces = {}
	propagation = {}
	for key in nb_desc_tri:
		# C'est possible que score n'est pas la clé.
		# On a généré des faits nouveaux.		
		if not propagation.has_key(key[0]):
			traces[key[0]] = set()
			if score.has_key(key[0]):
				propagation[key[0]] = score[key[0]]
				traces[key[0]].add(key[0])
			else:
				propagation[key[0]] = 0.0

		for desc in descendances[key[0]]:			
			# Dans la liste des descendants le noeud actuel apparait.
			if score.has_key(desc) and desc != key[0]:
				propagation[key[0]] += score[desc]
				# Possible pour les phrases incertaines, selon le paramétrage.
				if score[desc] > 0.0:
					traces[key[0]].add(desc)
	
	# End (croyance).
	
	out = open("Data/Resultats/propagation.txt", "w")
	out_traces = open("Data/Resultats/traces.txt", "w")
	for key in propagation.keys():
		out.write(key+"_"+str(propagation[key])+"\n")
	for key in traces.keys():	
		out_traces.write(key+"_")
		for val in range(len(list(traces[key]))):
			out_traces.write(list(traces[key])[val])
			if val + 1 < len(traces[key]):
				out_traces.write(";")
		out_traces.write("\n")
	
	return propagation

def build_profondeur(name_file, racine):
	desc_file = open(name_file, "r").readlines()

	nb_desc = {}
	leaves = list()
	graph = {racine:set()}
	for ligne in desc_file:
		spl = ligne.strip().split("->")
		if len(spl) == 2:
			specification = spl[0].strip()
			concept = spl[1].strip()
			concept = concept[1:-1]
			specification = specification[1:-1]
			
			if graph.has_key(concept):
				graph[concept].add(specification)
			else:
				graph[concept] = set()
				graph[concept].add(specification)
		
			# Recherche des feuilles.	
			if not concept in nb_desc: 
				nb_desc[concept] = 1
			else:
				nb_desc[concept] += 1
		
			if not specification in nb_desc: 
				nb_desc[specification] = 0
	
	for n in nb_desc:
		if nb_desc[n] == 0: 
			leaves.append(n)

	node_depth = {racine:0}
	depth_max = 0
	node_max = ""

	visited = {}

	for n in graph[racine]:
		depth = 1
		queue = [n]
		while len(queue) > 0:
			
			node = queue.pop()

			if not visited.has_key(node):
				visited[node] = 1
			
			if not node_depth.has_key(node):
				node_depth[node] = depth
			
			if nb_desc[node] > 0:
				for fils in graph[node]:
					
					if not visited.has_key(fils) or (node_depth.has_key(fils) and node_depth[fils] < node_depth[node]+1):
						queue.append(fils)							
							
					if not node_depth.has_key(fils):
						node_depth[fils] = node_depth[node]+1
					else:
						# Profondeur maximale.
						if node_depth[fils] < node_depth[node]+1:
							node_depth[fils] = node_depth[node]+1
			else:
				if node_depth[node] > depth_max:
					depth_max = node_depth[node]
					node_max = node
				
	out = open("Data/Resultats/profondeur.txt", "w")
	for key in node_depth.keys():
		out.write(key+"_"+str(node_depth[key])+"\n")
	return node_depth, depth_max
	
######

def inference(graphe_faits, couples_faits_extraits, racine, u_sent, choix_modele, val_inc):
	# Frequences.
	score = freq_faits(couples_faits_extraits, racine, u_sent, val_inc)
	# Ascendants directs.
	direct_asc = build_direct_ascendants(graphe_faits, racine)
	# Tous les descendants.
	descendances = build_descendants(direct_asc, racine)
	# Propagation.
	propa = propagation(descendances, score, racine)
	# Pronfondeur.
	profondeur,profondeur_max = build_profondeur(graphe_faits, racine)


	profondeur_dic = {}
	# key = all faits.
	for key in propa:
		if key != racine:
			x_i = int(propa[key])/float(propa[racine])
			y_i = int(profondeur[key])
			if profondeur_dic.has_key(y_i):
				profondeur_dic[y_i].append(x_i)
			else:
				profondeur_dic[y_i] = [x_i]

	keys = profondeur_dic.keys()
	prof_med = {}
	prof_quart = {}
	prof_3quart = {}
	moyenne = {}
	for key in keys:
		moyenne[key] = np.mean(profondeur_dic[key])
		prof_med[key] = np.median(profondeur_dic[key])
		prof_quart[key] = np.percentile(profondeur_dic[key],25)
		prof_3quart[key] = np.percentile(profondeur_dic[key],75)
	
	a_noter = set()

	nb_desc = {}
	
	for key in descendances.keys():
		nb_desc[key] = len(descendances[key])

	# On veut traiter dans un premier temps les feuilles.
	trieCroissant = lambda dico : sorted(dico.items(), lambda a,b: cmp(a[1],b[1]), reverse=False)
	nb_desc_tri = trieCroissant(nb_desc)
	keys = [r[0] for r in nb_desc_tri]

	for key in keys:
		check = 1
		#for desc in descendances[key]:
		#	if desc in a_noter and key != racine and key != desc:
		#		a_noter.add(key)
		#		check = 0
		#		autres += 1
		#		break
		p_n = propa[key]/float(propa[racine])
		# Croyance supérieure à la moyenne des croyances ou croyance non nulle et plausibilité supérieure à la croyance.
		if check == 1 and key != racine:
			if choix_modele == 2:		
				# M_2.
				if p_n >= moyenne[profondeur[key]]:
					a_noter.add(key)
			elif choix_modele == 3:
				# M3.
				if p_n >= prof_med[profondeur[key]]: #and pl_n > p_n:
					a_noter.add(key)
			else:
				# M_4.
				if (p_n >= prof_3quart[profondeur[key]]): #or (p_n > prof_quart[profondeur[key]] and pl_n > p_n)):
					a_noter.add(key)
				
				elif p_n > prof_quart[profondeur[key]]:
					for d_asc in direct_asc[key]:
						p_d_asc = propa[d_asc]/float(propa[racine])
						if p_d_asc > p_n and d_asc != key:
							a_noter.add(key)

	out = open("Data/Resultats/modele.xml", "w")
	out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<zooms>\n")
	out.write("\t<zoom numero=\"\" nbRelations=\"\">\n")
	for a_n in a_noter:
		out.write("\t\t<relation>"+a_n+"</relation>\n")
		
	out.write("\t</zoom>\n")
	out.write("</zooms>")
	out.close()

######

'''
f_name = "Data/Phrases/sources.reverb"
sources = {}
with open(f_name, "r") as df:
	for ligne in df.readlines():
		spl = ligne.strip().split("\t")
		if len(spl) == 2:
			spl_sources = spl[1].split("|")
			sources[spl[0]] = len(spl_sources)

f_name = "Data/Relations/rel_des.txt"
relations = {}
with open(f_name, "r") as df:
	for ligne in df.readlines():
		spl = ligne.strip().split("\t")
		if len(spl) == 3:
			relation = spl[1]+"\t"+spl[2]
			relations[spl[0]] = [relation, sources[spl[0]]]

racine = "ROOT"
graphe_faits = "Data/Graphes/facts.dot"
# Couples observés et désambiguïsés.
couples_faits_extraits = relations

print "Phrases incertaines."
u_sent_file = "Data/Phrases/uncertainty_sentences.txt"
id_u_phrases = []
"""
with open(u_sent_file, "r") as f:
	for ligne in f.readlines():
		spl = ligne.strip().split("\t")
		if len(spl) == 2:
			id_u_phrases.append(spl[0])
"""
inference(graphe_faits, couples_faits_extraits, racine, id_u_phrases, 2, 1.0)
'''	
	
