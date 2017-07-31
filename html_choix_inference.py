#!/usr/bin/python
# -*- coding:utf-8 -*-
import os, cgi, cgitb
from html_template import menu_html

cgitb.enable()

nb_lignes = os.popen("wc -l Data/Relations/rel.txt").read().split(" ")

print(menu_html(1))

if int(nb_lignes[0]) > 0:
	print """
	<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
	<h1 class="page-header">Inference parameters</h1>
		<form action="loading_2.py" method="post">
			<div class="form-group">
				<label for="model">Model</label>
				<select class="form-control" id="model" name="inference">
					<option>2</option>
					<option>3</option>
					<option>4</option>
				</select>
			</div>
			<div class="form-group">
				<label for="certainty">Incertainty value</label>
				<input type="text" class="form-control" id="certainty" name="valIncert" value="1.0">
			</div>
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
	print """         
	<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
		<h1 class="page-header">Any relations found</h1>

		<a href="index.py">Return to request page</a>
		
	</div>

	<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
	<script src="CSS/jquery.min.js"></script>
	<!-- Include all compiled plugins (below), or include individual files as needed -->
	<script src="CSS/js/bootstrap.min.js"></script>

	</body>
	</html>
	"""
