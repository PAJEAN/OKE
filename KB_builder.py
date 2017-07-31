#!/bin/python
# -*- coding:utf-8 -*-
import re

###### ###### ###### ###### Documentation ###

# TITLE # Structuration des syntagmes.

# Description #
	# Structuration des syntagmes.

###### ###### ###### ###### Input(s), Output(s) & Parameters ###
###
graph_file = "Data/Graphes/kb.dot"
###

###### ###### ###### ###### Functions ###
###

def getGeneralForms(ordering, w):
	s = set()
	s.add(w)
	if(w in ordering):
		s.update(ordering[w])
	return s

def abstract(ordering,syntagm):
	
	grams = syntagm.split()
	abstracted = []
	
	generalForms = []
	for w in grams:
		generalForms.append(getGeneralForms(ordering, w))
		
	queue = []
	for w in generalForms[0]:
		l = list()
		l.append((0,w))
		queue.append(l)
	
	
	while(len(queue) != 0):
		w = queue.pop(0)
		
		depth = w[-1][0]
		if(depth+1 < len(grams)):
			for n in generalForms[depth+1]:
				wn = list(w)
				wn.append((depth+1,n))
				queue.append(wn)
		
		if(len(w) == len(generalForms)):
			form = w[0][1]
			for i in range(1,len(w)):
				form += " "+w[i][1]
			abstracted.append(form)
			
	return abstracted
				
		
def getDirectGeneralForm(grams):
	if(len(grams) == 1): 
		return None
	grams.pop(0)
	return " ".join(grams)

###

###### ###### ###### ###### Program ###
###

# Construction des syntagmes.
# Exemple : syntagms = ["Liver_Cancer", "Hepatite", "Quick Development"]

def building_syntagm_graph(syntagms,ordering):
	graph = {}

	graph["[ROOT_SYNTAGME]"] = set()

	for syntagm in syntagms:
		
		syntagm = syntagm.strip()
		grams = syntagm.split()

		node_queue = [syntagm]

		graph[syntagm] = set()
		graph[syntagm].add("[ROOT_SYNTAGME]")

		while(len(node_queue) != 0):
			
			node = node_queue.pop(0)
			syntagm_node_grams = node.split()
			
			
			
			general_nodes = abstract(ordering,node)
			
			for general_node in general_nodes:
				
				if(node != general_node):
					graph[node].add(general_node)
					
					if(general_node not in graph): 
						node_queue.append(general_node)
						graph[general_node] = set()
						graph[general_node].add("[ROOT_SYNTAGME]")
					
			direct_general_form = getDirectGeneralForm(syntagm_node_grams)
			
			if(direct_general_form != None):
				graph[node].add(direct_general_form)
				
				if(direct_general_form not in graph): 
					node_queue.append(direct_general_form)
					graph[direct_general_form] = set()
					graph[direct_general_form].add("[ROOT_SYNTAGME]")


	# Transitive reduction to remove useless edges

	nb_desc = {}

	leaves = list()

	for n in graph:

		if not n in nb_desc:
			nb_desc[n] = 0

		for a in graph[n]:
			if not a in nb_desc:
				nb_desc[a] = 1
			else:
				nb_desc[a] += 1

	for n in nb_desc:
		if nb_desc[n] == 0:
			leaves.append(n)

	#print "leaves", len(leaves)

	queue = leaves
	propagated = {}
	while(len(queue) != 0):
		n = queue.pop()
		if(not n in propagated):
			propagated[n] = set()
		propagated[n].add(n)
		toRemove = []
		#if(n not in graph): continue
		for p in graph[n]:
			nb_desc[p] -= 1
			if(not p in propagated):
				propagated[p] = set()
			
			inter = propagated[n].intersection(propagated[p])
			
			for i in inter:
				if(i in graph and p in graph[i]):
					graph[i].remove(p)
				
			propagated[p].update(propagated[n])
				
			if(nb_desc[p] == 0):
				queue.append(p)

	# Build graph 
	# command dot -Tpdf graph_file -o graph_file.pdf 
	with open(graph_file,"w") as output :
		output.write("digraph word_graph {\n \t rankdir=BT\n")
		for node in graph:
			for adj in graph[node]:
				output.write( "\t\""+node+"\" -> \""+adj+"\""+"\n")
		output.write("}\n")
	
###

