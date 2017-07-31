#!/bin/python
# -*- coding:utf-8 -*-
from lxml import etree

from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize 


###### Description ###
###
# Les classes pour manipuler les fichiers.
# La classe pour l'évaluation.
# Statistiques sur le corpus (tf-idf).
###


############################ Files parser.

class File_parser:
	
	def __init__(self, path):
		self.path = path
		self.file_name = ""
		self.lignes = []
		# Chargement du fichier en mémoire.
		self.load()
	
	def phrases_normalisation(self):
		for ligne in range(len(self.lignes)):
			self.lignes[ligne] = self.normalisation(self.lignes[ligne])
	
	# Pour formater les phrases.
	def normalisation(self,text):
		maj = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split(" ")
		minuscules = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" ")
		num = "0 1 2 3 4 5 6 7 8 9".split(" ")
		phrase = ""
		for s in enumerate(text):
			if ord(s[1]) <= 127 and (s[1] in minuscules or s[1] in maj or s[1] in num or s[1] in [" ", "-", "."]):
				phrase += s[1]
		return phrase
	
	# Chargement du fichier.
	def load(self):
		import os
		
		with open(self.path) as data_file:
			self.file_name = os.path.basename(data_file.name)
			for ligne in data_file.readlines():
				self.lignes.append(ligne.strip())
		print("File "+self.path+" loaded.")
	
	# Permet d'utiliser with (context managers) avec un objet.
	# Ceci a pour effet de fermer la ressource.
	def __enter__(self):
		return self
	
	def close(self):
		pass
	
	def __exit__(self, *err):
		self.close()

# Delimiter-separated values.
class DSV_parser(File_parser):
	
	def __init__(self, path, sep):
		File_parser.__init__(self,path)
		self.sep = sep
		self.outs = {}
	
	# Format: c1(self.sep)c2(sep)c3(sep)c4 !
	def load_outs_twoColSep(self,sep):
		for line in self.lignes:
			spl = line.strip().split(self.sep)
			if len(spl) == 2:
				twoCol = spl[1].split(sep)
				self.outs[spl[0]] = twoCol
	
	# Format: c1(self.sep)c2(self.sep) !
	def load_outs(self):
		for line in self.lignes:
			spl = line.strip().split(self.sep)
			if len(spl) == 2:
				self.outs[spl[0]] = spl[1]
		
class XML_parser(File_parser):
	
	def __init__(self, path):
		File_parser.__init__(self,path)
		self.tree = etree.parse(self.path)
		self.root = self.tree.getroot()
	

class XML_parser_civil_code(XML_parser):
	
	def __init__(self, path):
		XML_parser.__init__(self,path)
	
	# Extraire le contenu de tous les articles.
	#def extraction_articles(self):	
	#	for article in self.root.iter("article"):
	#	print("Articles extraction done.")
		
############################ TF-IDF.

class Tf_idf:
	
	def __init__(self, corpus):
		
		# Corpus --> dict {id:sent}.
		self.corpus = corpus
		# Traitement des données.
		self.tf_id = {}
		self.idf_denominator = {}
		# Données par id et par mot.
		self.tf = {}
		self.idf = {}
		self.tf_idf = {}
		
	def normalisation(self, text):
		text = text.decode("utf-8")
		stemmer = WordNetLemmatizer()
		stoplist = stopwords.words("english")
		texts = [stemmer.lemmatize(word) for word in word_tokenize(text.lower()) if word not in stoplist]
		return texts

	def tf_articles(self, text):
		text = self.normalisation(text)
		return Counter(text)
	
	def number_of_terms(self, text):
		number = 0
		for key in text:
			number += text[key]
		return number
	
	# Traitement des données.
	def corpus_processing(self):
		# TF.
		for key in self.corpus:
			self.tf_id[key] = self.tf_articles(self.corpus[key])
			for mot in self.tf_id[key]:
				if not mot in self.idf_denominator: 
					self.idf_denominator[mot] = set()
					self.idf_denominator[mot].add(key)
				else:
					self.idf_denominator[mot].add(key)
		# IDF.			
		for mot in self.idf_denominator:
			self.idf[mot] = len(self.corpus) / float(len(self.idf_denominator[mot]))
	
		# TF-IDF.
		for id_line in self.tf_id:
			# La variable mot est unique car on utilise la fonction Counter.
			for mot in self.tf_id[id_line]:
				tf = self.tf_id[id_line][mot] / float(self.number_of_terms(self.tf_id[id_line]))
				tf_idf = tf * self.idf[mot]
				
				if not id_line in self.tf:
					self.tf[id_line] = {}
					self.tf[id_line][mot] = tf
				else:
					self.tf[id_line][mot] = tf
				
				if not id_line in self.tf_idf:
					self.tf_idf[id_line] = {}
					self.tf_idf[id_line][mot] = tf_idf
				else:
					self.tf_idf[id_line][mot] = tf_idf
		
					
				



















