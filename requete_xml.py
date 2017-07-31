#!/usr/bin/python
# -*- coding:utf-8 -*-
import cgi 
import cgitb
from lxml import etree

cgitb.enable()

tree = etree.parse("Data/Resultats/resultats.xml")
root = tree.getroot()


form = cgi.FieldStorage()
identifiant = "1"
if "id" in form:
	identifiant = cgi.escape(form.getvalue("id"))
	
method = "1"
if "method" in form:
	method = cgi.escape(form.getvalue("method"))
	
profondeur = 100
if "depth" in form:
	profondeur = float(cgi.escape(form.getvalue("depth")))

index = {}
with open("Data/Wordnet/wordnet_id_words.tsv", "r") as df:
	for ligne in df.readlines():
		spl = ligne.strip().split("\t")
		if len(spl) == 2:
			index[spl[0]] = spl[1]

def replace_id(relation, index):
	spl = relation.strip().split(" ")
	relation = ""
	for s in range(len(spl)):
		if spl[s] in index:
			relation += index[spl[s]]
		else:
			relation += spl[s]
		if s+1 < len(spl):
			relation += " "
	return relation

def seeAlso(identifiant, profondeur):
	relations = ""
	rels = root.findall("relation")
	find = 0
	for label in rels:
		if label.attrib["numero"] == identifiant:			
			find = 1
			for seeAlso in label:
				if seeAlso.tag == "seeAlso":
					for seeAlsoRel in seeAlso:
						spl_rel = seeAlsoRel.text.strip().split("\t")
						if len(spl_rel) > 1:
							if float(seeAlsoRel.attrib["profondeur"]) >= profondeur:
								relations += "<div class='row'>"
								relations += "<div class='col-md-1'></div>"
								relations += "<div class='col-md-1'></div>"
								relations += "<div class='col-md-5'>"+replace_id(spl_rel[0], index)+"</div>"
								relations += "<div class='col-md-5'>"+replace_id(spl_rel[1], index)+"</div>"
								relations += "</div>"
						#else:
						#	relations += seeAlsoRel.text+"<br />"
		if find == 1:
			break
				
	if relations == "":
		relations = "Any relations with."
	return relations


def support(identifiant):
	relations = ""
	relations += "<div class='row'>"
	relations += "<div class='col-md-1'><b>ID</b></div>"
	relations += "<div class='col-md-1'><b>Seen</b></div>"
	relations += "<div class='col-md-1'><b>Certainty</b></div>"
	relations += "<div class='col-md-9'><b>Sentence</b></div></div>"
	
	rels = root.findall("relation")
	
	find = 0
	for label in rels:
		if label.attrib["numero"] == identifiant:
			find = 1
			for support in label:
				if support.tag == "support":
					for supportRel in support:
						id_phrase = supportRel.attrib["id"]
						seen = supportRel.attrib["seen"]
						certainty = supportRel.attrib["certainty"]
						
						relations += "<div class='row'>"
						relations += "<div class='col-md-1'>"+id_phrase+"</div>"
						relations += "<div class='col-md-1'>"+seen+"</div>"
						relations += "<div class='col-md-1'>"+certainty+"</div>"
						
						labelRel = ""
						for elmt in supportRel:
							if elmt.tag == "labelRel":
								
								spl_rel = elmt.text.strip().split("\t")
								if len(spl_rel) > 1:
									labelRel = "<"+replace_id(spl_rel[0], index)+", "+replace_id(spl_rel[1], index)+">"
							else:
								relations += '<div class="col-md-9" data-toggle="tooltip" data-placement="left" title="'+labelRel+'">'+elmt.text+'</div>'
								relations += "</div>"
		if find == 1:
			break
				
	if find == 0:
		relations = "Any relations with."
	return relations

print("Content-type: text/html; charset=utf-8\n")

if method == "1":
	print(seeAlso(identifiant, profondeur))
else:
	print(support(identifiant))









