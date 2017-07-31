#!/usr/bin/python
# -*- coding:utf-8 -*-
import cgi, cgitb
from lxml import etree
from html_template import menu_html

cgitb.enable()

form = cgi.FieldStorage()

croyance = "60.0"
if "belief" in form:
	croyance = float(cgi.escape(form.getvalue("belief")))
	
profondeur = "60.0"
if "depth" in form:
	profondeur = float(cgi.escape(form.getvalue("depth")))


tree = etree.parse("Data/Resultats/resultats.xml")
root = tree.getroot()

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

meta_data = {"croyance": 50, "profondeur": 50}
with open("Data/Resultats/meta_information.tsv", "r") as df:
	for ligne in df.readlines():
		spl = ligne.strip().split("\t")
		if len(spl) == 2:
			if spl[0] == "profondeur":
				meta_data["profondeur"] = spl[1]
			elif spl[0] == "croyance":
				meta_data["croyance"] = spl[1]

print(menu_html(2))

print """         
<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
<h1 class="page-header">Visualisation</h1>

<form action="html_visualisation.py" method="post">
	<div class="form-group">
		<label for="bel">Belief</label>
"""
print('<input type="range" id="bel" name="belief" oninput="textBelief.value = belief.value" value="'+str(croyance)+'" max="'+meta_data["croyance"]+'" min="1" step="1">')
print('<output class="text-center" id="textBelief">'+str(croyance)+'</output>')

print """
	</div>
	<br/>
	<div class="form-group">
		<label for="dep">Depth</label>
"""
print('<input type="range" id="dep" name="depth" oninput="textDepth.value = depth.value" value="'+str(profondeur)+'" max="'+meta_data["profondeur"]+'" min="1" step="1">')
print('<output class="text-center" id="textDepth">'+str(profondeur)+'</output>')

print """
	</div>
	<br/>
	<button type="submit" class="btn btn-default">Submit</button>
</form>

<br/>
<div class='row' style='margin-bottom:5px;border-bottom: 1px solid #eee;'>
	<div class='col-md-12'></div>
</div>
"""


print("<div class='row'>")
print("<div class='col-md-1'><b>BELIEF</b></div>")
print("<div class='col-md-1'><b>DEPTH</b></div>")
print("<div class='col-md-5'><b>SUBJECT</b></div>")
print("<div class='col-md-5'><b>OBJECT</b></div>")
print("</div>")

for rel in root.iter("relation"):
	numero = rel.attrib["numero"]
	for label in rel:
		if label.tag == "label":
			relation = label.text.strip().split("\t")
			
			ecrire = 1
			if len(relation) <= 1:
				ecrire = 0

			if ecrire == 1:
				#print label.attrib["support"], croyance, label.attrib["profondeur"], profondeur
				if float(label.attrib["support"]) >= croyance and float(label.attrib["profondeur"]) >= profondeur:
				
					print("<div class='row'>")
					print("<div class='col-md-1'>"+label.attrib["support"]+"</div>")
					print("<div class='col-md-1'>"+label.attrib["profondeur"]+"</div>")
					print("<div class='col-md-5'>"+replace_id(relation[0], index)+"</div>")
					print("<div class='col-md-5'>"+replace_id(relation[1], index)+"</div>")
					print("</div>")
				
					print("<div id='divSeeAlso"+str(numero)+"'><a href='#' id='aSeeAlso"+str(numero)+"' onclick='loadSeeAlso(\""+str(numero)+"\",\""+str(profondeur)+"\")'>See Also</a></div>")
					print("<p id='seeAlso"+str(numero)+"'></p>")
					print("<div id='divSupport"+str(numero)+"'><a href='#' id='aSupport"+str(numero)+"' onclick='loadSupport(\""+str(numero)+"\")'>Support</a></div>")
					print("<p id='support"+str(numero)+"'></p>")
					
					# Ligne.
					print("<div class='row' style='margin-bottom:5px;border-bottom: 1px solid #eee;'>")
					print("<div class='col-md-12'></div>")
					print("</div>")
				
			"""
			if len(relation) > 1:
				print("<div class='row'>")
				print("<div class='col-md-1'>"+label.attrib["support"]+"</div>")
				print("<div class='col-md-1'>"+label.attrib["profondeur"]+"</div>")
				print("<div class='col-md-5'>"+replace_id(relation[0], index)+"</div>")
				print("<div class='col-md-5'>"+replace_id(relation[1], index)+"</div>")
				print("</div>")
			else:
				print(label.text+"<br />")
			
			print("<div id='divSeeAlso"+str(numero)+"'><a href='#' id='aSeeAlso"+str(numero)+"' onclick='loadSeeAlso(\""+str(numero)+"\")'>See Also</a></div>")
			print("<p id='seeAlso"+str(numero)+"'></p>")
			print("<div id='divSupport"+str(numero)+"'><a href='#' id='aSupport"+str(numero)+"' onclick='loadSupport(\""+str(numero)+"\")'>Support</a></div>")
			print("<p id='support"+str(numero)+"'></p>")
			
			# Ligne.
			print("<div class='row' style='margin-bottom:5px;border-bottom: 1px solid #eee;'>")
			print("<div class='col-md-12'></div>")
			print("</div>")
			"""
del index

print """

		  </div>
	</div>
</div>


<script>
	function loadSeeAlso(identifiant, profondeur) {
		var xhttp = new XMLHttpRequest(identifiant);
		xhttp.onreadystatechange=function() {
			if (this.readyState == 4 && this.status == 200) {
				document.getElementById("seeAlso"+identifiant).innerHTML = this.responseText;
				var str = '<a href="#" id="aSeeAlso'+identifiant+'" onclick="hide_links(';
				str += "\'"+identifiant+"\', \'see Also\')";
				str += '">Hide (see Also)</a>';
				document.getElementById("divSeeAlso"+identifiant).innerHTML = str;
			}
		};
	xhttp.open("GET", "requete_xml.py?method=1&depth="+profondeur+"&id="+identifiant+"", true);
	xhttp.send();
}

function loadSupport(identifiant) {
	var xhttp = new XMLHttpRequest(identifiant);
	xhttp.onreadystatechange=function() {
		if (this.readyState == 4 && this.status == 200) {
			document.getElementById("support"+identifiant).innerHTML = this.responseText;
			var str = '<a href="#" id="aSupport'+identifiant+'" onclick="hide_support(';
			str += "\'"+identifiant+"\', \'support\')";
			str += '">Hide (support)</a>';
			document.getElementById("divSupport"+identifiant).innerHTML = str;
		}
	};
	xhttp.open("GET", "requete_xml.py?method=2&id="+identifiant+"", true);
	xhttp.send();
}

</script>

<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="CSS/jquery.min.js"></script>
<!-- Include all compiled plugins (below), or include individual files as needed -->
<script src="CSS/js/bootstrap.min.js"></script>

<script>
	$(document).ready(function() {
		$("body").tooltip({ selector: '[data-toggle=tooltip]' });
	});

	function hide_links(id, txt){
		if(document.getElementById("seeAlso"+id).style.display == "none"){
		  document.getElementById("seeAlso"+id).style.display = "block";
		  document.getElementById("aSeeAlso"+id).innerHTML = "Hide ("+txt+")";
		}
		else{
		  document.getElementById("seeAlso"+id).style.display = "none";
		  document.getElementById("aSeeAlso"+id).innerHTML = "Show ("+txt+")";
		}
	}
  
    function hide_support(id, txt){
		if(document.getElementById("support"+id).style.display == "none"){
		  document.getElementById("support"+id).style.display = "block";
		  document.getElementById("aSupport"+id).innerHTML = "Hide ("+txt+")";
		}
		else{
		  document.getElementById("support"+id).style.display = "none";
		  document.getElementById("aSupport"+id).innerHTML = "Show ("+txt+")";
		}
	}
  
</script>

</body>
</html>
"""
