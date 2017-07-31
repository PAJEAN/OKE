#!/usr/bin/python
# -*- coding:utf-8 -*-
import cgi, cgitb
from html_template import menu_html

cgitb.enable()

form = cgi.FieldStorage()

# On sauvegarde les paramètres dans un fichier de paramètres.
out = open("Data/Inputs/parameters.txt", "w")

desambiguisation = 0
if "desambiguisation" in form:
	desambiguisation = 1

sujet = ""
if "sujet" in form:
	sujet = cgi.escape(form.getvalue("sujet")).strip()

predicats = ""
if "predicats" in form:
	predicats = cgi.escape(form.getvalue("predicats")).strip()	
	
objet = ""
if "objet" in form:
	objet = cgi.escape(form.getvalue("objet")).strip()

out.write("sujet:"+sujet+"\n")
out.write("predicats:"+predicats+"\n")
out.write("objet:"+objet+"\n")
out.write("desambiguisation:"+str(desambiguisation)+"\n")
out.close()

print(menu_html(1))

print """         
<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
	<h1 class="page-header">Loading</h1>
            
    <!-- Content -->
	<table class="table">
		<tr><td> Research of relations </td>  <td id="t0"><div class="loader"></div></td></tr>
		<tr><td> Building of phrases graph </td>  <td id="t1"><div class="loader"></div></td></tr>
		<tr><td> Generating of new facts </td>  <td id="t2"><div class="loader"></div></td></tr>
		<tr><td> Building of facts graph </td>  <td id="t3"><div class="loader"></div></td></tr>
	</table>
            
</div>

<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="CSS/jquery.min.js"></script>
<!-- Include all compiled plugins (below), or include individual files as needed -->
<script src="CSS/js/bootstrap.min.js"></script>

<script>
		
	function task(numero) {
		var xhttp = new XMLHttpRequest(numero);
		
		xhttp.open("GET", "construction_GF.py?task="+numero);
		xhttp.send();
		
		xhttp.onreadystatechange=function() {
			if (this.readyState == 4 && this.status == 200) {
				r = parseInt(this.responseText)
				
				if(r != -1){
					document.getElementById("t"+numero).innerHTML = "OK";
					task(r);
				}
				else{
					window.location = "http://localhost:8888/html_choix_inference.py";
				}
			}
		};
	}
	
	task("0");
	
</script>
	
  </body>
</html>
"""
