#!/usr/bin/python
# -*- coding:utf-8 -*-
import cgi, cgitb

cgitb.enable()

def menu_html(li):
	menu = """
	
	<!DOCTYPE html>
	<html lang="en">
		<head>
			<meta charset="utf-8">
			<meta http-equiv="X-UA-Compatible" content="IE=edge">
			<meta name="viewport" content="width=device-width, initial-scale=1">
			<!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
			
			<title>O.K.E</title>

			<!-- Bootstrap -->
			<link href="CSS/css/bootstrap.min.css" rel="stylesheet">
			
			<!-- Custom styles for this template -->
			<link href="CSS/dashboard.css" rel="stylesheet">

		</head>
		<body>

			<nav class="navbar navbar-inverse navbar-fixed-top">
				<div class="container-fluid">
					<div class="navbar-header">
						<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
							<span class="sr-only">Toggle navigation</span>
							<span class="icon-bar"></span>
							<span class="icon-bar"></span>
							<span class="icon-bar"></span>
						</button>
						<a class="navbar-brand" href="index.py">Open Knowledge Extraction</a>
					</div>
					<div id="navbar" class="navbar-collapse collapse">
						<ul class="nav navbar-nav navbar-right">
							<li><a href="#">Publication</a></li>
							<li><a href="#">Credits</a></li>
						</ul>
					</div>
				</div>
			</nav>

			<div class="container-fluid">
				<div class="row">
					<div class="col-sm-3 col-md-2 sidebar">
						<ul class="nav nav-sidebar">
	"""
	
	labels = [("index.py","Request"), ("html_choix_inference.py","Paramaters"), ("html_visualisation.py","Visualisation")]
	
	for l in range(len(labels)):
		if (l) == li:	 
			menu +=  '<li class="active"><a href="'+labels[l][0]+'">'+labels[l][1]+' <span class="sr-only">(current)</span></a></li>'
		else:
			menu +=  '<li><a href="'+labels[l][0]+'">'+labels[l][1]+'</a></li>'
	
	menu += """
						</ul>
					</div>
				</div>
			</div>
	"""
	
	return menu
