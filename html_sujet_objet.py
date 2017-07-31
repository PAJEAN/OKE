#!/usr/bin/python
# -*- coding:utf-8 -*-
import cgi, cgitb
from html_template import menu_html

cgitb.enable() # Affiche les erreurs.

###### ###### ###### ###### Documentation ###

# TITLE # Suppression d'éléments dans les phrases.

# Description #
	# Permet de supprimer des éléments indésirables dans les phrases.

###### ###### ###### ###### Input(s), Output(s) & Parameters ###
###

form = cgi.FieldStorage()

desambiguisation = 0
without_des = 1
if "desambiguisation" in form:
	desambiguisation = 1
	without_des = 0

predicats = []
if "predicats" in form:
	predicats = cgi.escape(form.getvalue("predicats"))

sujet = ""
if "sujet" in form:
	sujet = cgi.escape(form.getvalue("sujet")).strip()
	
objet = ""
if "objet" in form:
	objet = cgi.escape(form.getvalue("objet")).strip()

###

###### ###### ###### ###### Functions ###
###

def multiple_forme_surfaces(so, used, definition):
	stop = 0
	rels = {}
	if so != "":
		s_spl = so.strip().split(" ")
		for i in reversed(range(len(s_spl))):
			for j in range(0,(i+1)):
				
				entity = " ".join(s_spl[j:(i+1)])
				entity = entity.lower()
				
				# Si multiples sens.
				if entity in used:
					if len(used[entity]) > 0:
						for u_e in used[entity]:

							entity_des = " ".join(s_spl[0:j])

							if len(entity_des) > 0:
								entity_des += " "
							
							entity_des += str(u_e)
							
							fin = " ".join(s_spl[(i+1):len(s_spl)])
							if len(fin) > 0:
								entity_des += " "
								entity_des += fin
							
							if u_e in definition:
								rels[entity_des] = definition[u_e]+" (id: "+str(u_e)+")."
							else:
								rels[entity_des] = "No definition for the entity ["+u_e+"]."
					
					# Break car on désambiguise uniquement une entité.
					stop = 1
					break
			# Break the second loop.	
			if stop == 1:
				break
	# Si len(rels) > 0 alors il y au moins une ambiguité.
	return rels



###

# On recherche dans le fichier words_id_used.txt si l'entité est présente.
# Si plusieurs fois alors on propose les alternatives.
if desambiguisation == 1:
	
	definition = {}
	with open("Data/Wordnet/wordnet_offset_definition.tsv", "r") as df:
		for ligne in df.readlines():
			spl = ligne.strip().split("\t")
			if len(spl) == 2:
				definition[spl[0]] = spl[1]
				
	
	used = {}
	with open("Data/Wordnet/wordnet_words_id.tsv", "r") as df:
		for ligne in df.readlines():
			spl = ligne.strip().split("\t")
			if len(spl) == 2:
				if spl[0] in used:
					used[spl[0]].add(spl[1])
				else:
					used[spl[0]] = set([spl[1]])
	
	suj_rels = multiple_forme_surfaces(sujet, used, definition)
	obj_rels = multiple_forme_surfaces(objet, used, definition)
				
	if len(suj_rels) > 0 or len(obj_rels) > 0:
	
		print(menu_html(0))
		print """         
		<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
			<h1 class="page-header">Polysemy</h1>

			<form action="loading_1.py" method="post">
		"""
		if len(suj_rels) > 0:
			print """
				<label>What do you mean with your subject: %s ?</label>				
				<div class="radio">	
			""" % (sujet)
			for s in suj_rels:
				print('<label><input type="radio" name="sujet" value="'+s+'">'+suj_rels[s]+'</label><br/>')
	
			print """
				</div>
			"""
		else:
			print('<input type="text" style="display:none" name="sujet" value="'+sujet+'">')
		
		print('<input type="text" style="display:none" name="predicats" value="'+predicats+'">')
		
		if len(obj_rels) > 0:
			print """
				<label>What do you mean with your object: %s ?</label>		
				<div class="radio">			
			""" % (objet)
			for s in obj_rels:
				print('<label><input type="radio" name="objet" value="'+s+'">'+obj_rels[s]+'</label><br/>')
	
			print """
				</div>
			"""
		else:
			print('<input type="text" style="display:none" name="objet" value="'+objet+'">')
			
		print('<input type="text" style="display:none" name="desambiguisation" value="1">')
		
		print """
		<button type="submit" class="btn btn-default">Submit</button>
		</form>
		</div>

		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="CSS/jquery.min.js"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="CSS/js/bootstrap.min.js"></script>

		</body>
		</html>
		"""
	else:
		without_des = 1

# On ne désambiguise pas donc on renvoie la page vers la construction du graphe.
if without_des == 1:
	print("Content-type: text/html; charset=utf-8\n")

	print """
	<!DOCTYPE html>
		<html>
			<head>
			</head>
			<body>
	"""
	
	print """
				<form id="form" action="loading_1.py" method="post">
	"""
	print('<input type="text" style="display:none" id="suj" name="sujet" value="'+sujet+'">')
	print('<input type="text" style="display:none" id="pred" name="predicats" value="'+predicats+'">')
	print('<input type="text" style="display:none" id="obj" name="objet" value="'+objet+'">')
	print """
				</form>

				<script>
					document.getElementById('form').submit();
				</script>

			</body>
		</html>
	"""
	
