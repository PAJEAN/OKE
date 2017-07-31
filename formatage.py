#!/bin/python
# -*- coding:utf-8 -*-
from lxml import etree
import re

# o_so : relations extraites désambiguisées.
# o_so_inversed : retrouver la relation non désambiguisée à partir de son identifiant.
# traces : les relations supportant une relation donnée.
# support : valeur de propagation.
# profondeur : dans le graphe de faits.
def formatage(o_so, o_so_inversed, traces, support, profondeur, id_phrases, id_u_phrases, sources):
	
	trieDecroissant = lambda dico : sorted(dico.items(), lambda a,b: cmp(a[1],b[1]), reverse=True)
	trieCroissant = lambda dico : sorted(dico.items(), lambda a,b: cmp(a[1],b[1]), reverse=False)
	
	zooms_root = etree.Element("relations")

	# Observer les relations non utilisées.
	# Modèle issu soit de stat_pareto.py soit de modele_inference.py.
	tree = etree.parse("Data/Resultats/modele.xml")
	root = tree.getroot()
	i = 0
	
	infered_rels = set()

	for rel in root.iter("relation"):
		infered_rels.add(rel.text)
		
	# On trie les relations selon leur croyance et leur profondeur.
	support_decroissant = trieDecroissant(support)
	profondeur_decroissant = trieDecroissant(profondeur)
	
	#keys_support = [r[0] for r in support_decroissant]
	#keys_profondeur = [r[0] for r in profondeur_decroissant]
	keys_ordre = [r[0] for r in profondeur_decroissant]
	
	# Pour sauvegarder la profondeur maximale.
	out = open("Data/Resultats/meta_information.tsv", "w")
	out.write("profondeur\t"+str(profondeur_decroissant[0][1])+"\n")
	out.write("croyance\t"+str(support_decroissant[0][1]))
	out.close()
	
	"""
	ordre = {}
	for rel in support_decroissant:
		ordre[rel[0]] = keys_support.index(rel[0])
		ordre[rel[0]] += keys_profondeur.index(rel[0])
	
	del support_decroissant
	del profondeur_decroissant
	del keys_support
	del keys_profondeur
	
	ordre_trier = trieCroissant(ordre)
	keys_ordre = [r[0] for r in ordre_trier]
	"""
	
	rels_seen = {}
	cmpt = 1
	# On affiche la relation la plus pertinente en fonction de sa croyance et de sa profondeur et on regarde si elle est présente dans les relations inférées.
	for rel in keys_ordre:
		if rel in infered_rels and not rel in rels_seen:
			rels_seen[rel] = 1
			niv_1 = etree.SubElement(zooms_root, "relation")
			niv_1.set("numero", str(cmpt))
			
			niv_2 = etree.SubElement(niv_1, "label")
			niv_2.text = rel
			niv_2.set("support", str(support[rel]))
			niv_2.set("profondeur", str(profondeur[rel]))
			
			cmpt += 1
			
			rel_support = set()
			
			ids = set()
			seeAlso = {}
			for rel_tra in traces:
				if rel_tra != rel and traces[rel] == traces[rel_tra]:
					seeAlso[rel_tra] = keys_ordre.index(rel_tra)
					rels_seen[rel_tra] = 1
			for rel_sup_tra in traces[rel]:
				for id_rel in o_so[rel_sup_tra]:
					ids.add(id_rel)
			
			seeAlso_tri = trieCroissant(seeAlso)
			keys_seeAlso = [r[0] for r in seeAlso_tri]
			
			del seeAlso
			del seeAlso_tri
			
			if len(keys_seeAlso) > 0:
				niv_3 = etree.SubElement(niv_1, "seeAlso")
				for sa_rel in keys_seeAlso:
					niv_4 = etree.SubElement(niv_3, "seeAlsoRel")
					niv_4.text = sa_rel
					niv_4.set("profondeur", str(profondeur[sa_rel]))
			
			niv_5 = etree.SubElement(niv_1, "support")
			for id in ids:
				niv_6 = etree.SubElement(niv_5, "supportRel")
				niv_6.set("id", id)
				if id in id_u_phrases:
					niv_6.set("certainty", "uncertain")
				else:
					niv_6.set("certainty", "certain")
				
				if id in sources:
					niv_6.set("seen", str(sources[id]))
				else:
					niv_6.set("seen", "?")
				
				niv_7 = etree.SubElement(niv_6, "labelRel")
				niv_7.text = o_so_inversed[id]
				niv_7 = etree.SubElement(niv_6, "labelPhrase")
				niv_7.text = id_phrases[id]
	
	out = open("Data/Resultats/resultats.xml", "w")
	for i in etree.tostring(zooms_root, pretty_print=True):
		out.write(i)
	out.close()	
	
	
	
	
	
	
	
	
	
	
	
	
