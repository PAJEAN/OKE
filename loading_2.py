#!/usr/bin/python
# -*- coding:utf-8 -*-
import cgi, cgitb
from html_template import menu_html

cgitb.enable()

form = cgi.FieldStorage()

# On sauvegarde les paramètres dans un fichier de paramètres.
out = open("Data/Inputs/parameters.txt", "a+")

modele = 2
if "inference" in form:
	modele = int(cgi.escape(form.getvalue("inference")))
	
valeur_incert = 1.0
if "valIncert" in form:
	valeur_incert = float(cgi.escape(form.getvalue("valIncert")))

out.write("modele:"+str(modele)+"\n")
out.write("incertitude:"+str(valeur_incert)+"\n")
out.close()

print(menu_html(1))

print """         
		<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
			<h1 class="page-header">Loading</h1>
					
			<!-- Content -->
			<table class="table">
				<tr><td> Knowledge inference </td>  <td id="t0"><div class="loader"></div></td></tr>
				<tr><td> Data formatting </td>  <td id="t1"><div class="loader"></div></td></tr>
			</table>
					
		</div>

		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="CSS/jquery.min.js"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="CSS/js/bootstrap.min.js"></script>

		<script>
				
			function task(numero) {
				var xhttp = new XMLHttpRequest(numero);
				
				xhttp.open("GET", "inference.py?task="+numero);
				xhttp.send();
				
				xhttp.onreadystatechange=function() {
					if (this.readyState == 4 && this.status == 200) {
						console.log(this.responseText)
						r = parseInt(this.responseText)
						console.log(r)
						if(r != -1){
							document.getElementById("t"+numero).innerHTML = "OK";
							task(r);
						}
						else{
							window.location = "http://localhost:8888/html_visualisation.py?belief=1&depth=1";
						}
					}
				};
			}
			
			task("0");
			
		</script>
	
	</body>
</html>
"""
