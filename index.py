#!/usr/bin/python
# -*- coding:utf-8 -*-
import cgi, cgitb
from html_template import menu_html

cgitb.enable()

print(menu_html(0))

print """         
<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
	<h1 class="page-header">Request</h1>
            
            
	<form class="form-inline" action="html_sujet_objet.py">
		<div class="form-group">
			<label class="sr-only" for="suj">Subject</label>
			<input type="text" class="form-control" id="suj" name="sujet" placeholder="Subject">
		</div>
		<div class="form-group">
			<label class="sr-only" for="pred">Predicates</label>
			<input type="text" class="form-control" id="pred" name="predicats" placeholder="Predicates">
		</div>
		<div class="form-group">
			<label class="sr-only" for="obj">Object</label>
			<input type="text" class="form-control" id="obj" name="objet" placeholder="Object">
		</div>
		<div class="checkbox">
			<label>
			  <input type="checkbox" name="desambiguisation"> Disambiguate (wsd).
			</label>
		</div>
		<button type="submit" class="btn btn-default">Sign in</button>
	</form>
            
</div>

<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="CSS/jquery.min.js"></script>
<!-- Include all compiled plugins (below), or include individual files as needed -->
<script src="CSS/js/bootstrap.min.js"></script>

<script>
  function hide_links(){
	if(document.getElementById("links").style.display == "none"){
	  document.getElementById("links").style.display = "block";
	}
	else{
	  document.getElementById("links").style.display = "none";
	}
  }
</script>
	
  </body>
</html>
"""
